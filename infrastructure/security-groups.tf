provider "aws" {
  region = "ap-south-1"  # Change to your desired region
}

resource "aws_security_group" "my-security-group" {
  name        = "my-security-group"
  description = "Security group allowing all inbound and outbound traffic"
  vpc_id      = aws_vpc.my-vpc.id

  # Inbound rules: allow all
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # -1 means all protocols
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound rules: allow all
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_all_sg"
  }
}
