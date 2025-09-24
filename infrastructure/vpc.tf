#vpc

resource "aws_vpc" "my-vpc" {
  cidr_block = "10.0.0.0/16"
  instance_tenancy = "default"
    tags = {
        Name = "my-vpc"
    }
  
}

#internet gateway

resource "aws_internet_gateway" "my-gateway" {
  vpc_id = aws_vpc.my-vpc.id

  tags = {
    Name = "my-gateway"
  }
}

#public subnet

resource "aws_subnet" "my-public-subnet" {
  vpc_id = aws_vpc.my-vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "ap-south-1a"

  tags = {
    Name = "my-public-subnet"
  }
}

#private subnet

resource "aws_subnet" "my-private-subnet" {
  vpc_id = aws_vpc.my-vpc.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "ap-south-1a"

  tags = {
    Name = "my-private-subnet"
  }
}

# route table 

resource "aws_route_table" "my-route-table" {
  vpc_id = aws_vpc.my-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.my-gateway.id
  }

  tags = {
    Name = "my-route-table"
  }
}

# route table association

resource "aws_route_table_association" "my-public-subnet-association" {
  subnet_id      = aws_subnet.my-public-subnet.id
  route_table_id = aws_route_table.my-route-table.id
}

resource "aws_route_table_association" "my-private-subnet-association" {
  subnet_id      = aws_subnet.my-private-subnet.id
  route_table_id = aws_route_table.my-route-table.id
}