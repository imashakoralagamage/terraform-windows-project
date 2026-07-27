import boto3
import json
import requests

REGION = "ap-southeast-1"

client = boto3.client(
    "secretsmanager",
    region_name=REGION
)

secret = client.get_secret_value(
    SecretId="terraform/servicenow"
)

snow = json.loads(secret["SecretString"])

username = snow["username"]
password = snow["password"]
instance = snow["instance"]

import os

ritm_number = os.environ["RITM_NUMBER"]

ritm_url = (
    f"{instance}/api/now/table/sc_req_item"
    f"?sysparm_query=number={ritm_number}"
    "&sysparm_display_value=true"
)

ritm_response = requests.get(
    ritm_url,
    auth=(username, password),
    headers={"Accept": "application/json"}
)

ritm_response.raise_for_status()

ritm = ritm_response.json()["result"][0]

variables_url = (
    f"{instance}/api/now/table/sc_item_option_mtom"
    f"?sysparm_query=request_item={ritm['sys_id']}"
)

variables_response = requests.get(
    variables_url,
    auth=(username, password),
    headers={"Accept": "application/json"}
)

variables_response.raise_for_status()

variable_records = variables_response.json()["result"]

tfvars = {}

mapping = {
    "Server Name": "server_name",
    "Environment": "environment",
    "Subnet ID": "subnet_id",
    "VPC ID": "vpc_id",
    "Instance Type": "instance_type",
    "Owner": "owner",
    "Windows AMI ID": "ami_id"
}

for record in variable_records:

    option_id = record["sc_item_option"]["value"]

    option_url = (
        f"{instance}/api/now/table/sc_item_option/{option_id}"
        "?sysparm_display_value=true"
    )

    option_response = requests.get(
        option_url,
        auth=(username, password),
        headers={"Accept": "application/json"}
    )

    option_response.raise_for_status()

    option = option_response.json()["result"]

    question = option["item_option_new"]["display_value"]
    value = option["value"]

    if question in mapping:
        tfvars[mapping[question]] = value

with open("terraform.auto.tfvars.json", "w") as f:
    json.dump(tfvars, f, indent=2)

print("\nCreated terraform.auto.tfvars.json\n")
print(json.dumps(tfvars, indent=2))