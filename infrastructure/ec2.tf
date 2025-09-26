#ec2 instance

resource "aws_instance" "my-server" {
    ami =  "ami-02d26659fd82cf299"
    instance_type = "t2.medium"
    key_name = "Ujwal-DevOps-SRE"
    subnet_id = aws_subnet.my-public-subnet.id
    security_groups = [aws_security_group.my-security-group.id]
    tags = {
        Name = "my-server"
    }
}
