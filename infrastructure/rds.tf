# MySQL RDS Instance

resource "aws_db_instance" "mysql_db" {
  identifier         = "ujwal-mysql-db"
  allocated_storage  = 20               
  engine             = "mysql"
  engine_version     = "8.0"
  instance_class     = "db.t2.micro"   
  db_name            = "ujwal-db"
  username           = "ujwal"
  password           = "ujwal9494"
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot = true
  publicly_accessible = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  deletion_protection   = false
}
