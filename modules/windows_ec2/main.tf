resource "aws_instance" "windows" {

  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id

  associate_public_ip_address = true

  tags = {
    Name        = var.server_name
    Environment = var.environment
    Owner       = var.owner
    VPC         = var.vpc_id
    ManagedBy   = "Terraform"
    Project     = "ServiceNow-Windows"
  }
}