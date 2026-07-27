module "windows_server" {

  source = "./modules/windows_ec2"

  server_name   = var.server_name
  instance_type = var.instance_type
  ami_id        = var.ami_id
  subnet_id     = var.subnet_id
  vpc_id        = var.vpc_id
  owner         = var.owner
  environment   = var.environment
}