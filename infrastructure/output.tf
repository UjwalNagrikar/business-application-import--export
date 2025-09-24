output "rds_endpoint" {
  value = aws_db_instance.mysql_db.endpoint
}

output "ec2_public_ip" {
  value = aws_instance.my-server.public_ip
}