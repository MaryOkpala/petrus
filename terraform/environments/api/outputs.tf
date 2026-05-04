output "vpc_id"          { value = module.networking.vpc_id }
output "public_subnet"   { value = module.networking.public_subnet_id }
output "private_subnet"  { value = module.networking.private_subnet_id }
output "app_sg_id"       { value = module.security.app_sg_id }
