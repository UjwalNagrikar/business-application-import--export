# UN Enterprises - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture](#architecture)
4. [Project Structure](#project-structure)
5. [Prerequisites](#prerequisites)
6. [Setup Instructions](#setup-instructions)
7. [Deployment Guide](#deployment-guide)
8. [Features](#features)
9. [Configuration](#configuration)
10. [Troubleshooting](#troubleshooting)
11. [Maintenance](#maintenance)

## Project Overview

**UN Enterprises** is a modern, responsive web application for a global import-export business. The application features a professional landing page with contact form functionality, built using Flask as the backend framework and deployed on AWS infrastructure.

### Key Features:
- Responsive landing page with modern UI/UX
- Contact form with database storage
- Admin panel for viewing submissions
- AWS RDS MySQL database integration
- Dockerized application
- Infrastructure as Code (Terraform)
- Error handling (404/500 pages)

## Technology Stack

### Backend
- **Python 3.10** - Programming language
- **Flask 2.3.2** - Web framework
- **MySQL Connector Python 8.0.33** - Database driver
- **Gunicorn 21.2.0** - WSGI HTTP Server

### Frontend
- **HTML5** - Markup language
- **CSS3** - Styling with modern animations
- **JavaScript (ES6)** - Client-side functionality
- **Responsive Design** - Mobile-first approach

### Infrastructure
- **AWS EC2** - Application hosting
- **AWS RDS MySQL** - Database service
- **AWS VPC** - Network isolation
- **Terraform** - Infrastructure as Code
- **Docker** - Containerization
- **Nginx** - Static file serving (optional)

### Development Tools
- **Git** - Version control
- **Docker Compose** - Local development
- **Python Virtual Environment** - Dependency isolation

## Architecture

### High-Level Architecture
```
Internet
    ↓
AWS VPC (10.0.0.0/16)
    ↓
Internet Gateway
    ↓
Public Subnet (10.0.1.0/24)
    ↓
EC2 Instance (Flask App)
    ↓
Private Subnet (10.0.2.0/24)
    ↓
RDS MySQL Database
```

### Application Architecture
```
User Browser
    ↓
Flask Application (Port 5000)
    ↓
MySQL RDS Database
    ↓
Contact Form Data Storage
```

## Project Structure

```
project-root/
├── .gitignore                 # Git ignore rules
├── docker-compose.yml         # Docker composition for local dev
├── app-layer/                 # Application code
│   ├── app.py                # Main Flask application
│   ├── Dockerfile            # Docker configuration
│   └── requirements.txt      # Python dependencies
├── Template/                  # HTML templates
│   ├── 404.html             # Not found error page
│   ├── 500.html             # Server error page
│   ├── admin.html           # Admin dashboard
│   └── contact.html         # Contact page (404 template)
├── static/                   # Static assets
│   ├── index.html           # Main landing page
│   ├── styles.css           # CSS styling
│   ├── script.js            # JavaScript functionality
│   └── Dockerfile           # Docker config for static files
└── infrastructure/           # Terraform IaC
    ├── vpc.tf               # VPC and networking
    ├── ec2.tf               # EC2 instance
    ├── rds.tf               # RDS database
    ├── security-groups.tf   # Security groups
    ├── alb.tf               # Application Load Balancer (empty)
    └── output.tf            # Terraform outputs
```

## Prerequisites

### Software Requirements
- **Python 3.10+**
- **Node.js & npm** (for frontend development)
- **Docker & Docker Compose**
- **Terraform 1.0+**
- **AWS CLI**
- **Git**

### AWS Requirements
- AWS Account with appropriate permissions
- AWS CLI configured with credentials
- Key pair for EC2 access (create `Ujwal-DevOps-SRE.pem`)

### System Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space
- **OS**: Linux, macOS, or Windows with WSL2

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd un-enterprises-project
```

### 2. Local Development Setup

#### Option A: Using Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
cd app-layer
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Run the application
flask run --host=0.0.0.0
```

#### Option B: Using Docker Compose
```bash
# Build and run containers
docker-compose up --build

# Access application
# Frontend: http://localhost:80
# Backend: http://localhost:5000
```

### 3. Database Configuration

The application is configured to use AWS RDS MySQL. For local development, you can either:
- Use the existing RDS instance (requires AWS credentials)
- Set up a local MySQL database

#### Local MySQL Setup:
```bash
# Install MySQL (Ubuntu/Debian)
sudo apt update
sudo apt install mysql-server

# Create database and user
sudo mysql -u root -p
CREATE DATABASE `un_enterprises`;
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON un_enterprises.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Update `app.py` with local database credentials:
```python
rds_host = "localhost"
rds_user = "app_user"
rds_password = "your_password"
database = "un_enterprises"
```

## Deployment Guide

### 1. Infrastructure Deployment (AWS)

#### Step 1: Configure AWS CLI
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (ap-south-1)
# Enter output format (json)
```

#### Step 2: Deploy Infrastructure
```bash
cd infrastructure

# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Deploy infrastructure
terraform apply
```

#### Step 3: Note the Outputs
```bash
# Get RDS endpoint and EC2 IP
terraform output rds_endpoint
terraform output ec2_public_ip
```

### 2. Application Deployment

#### Step 1: Connect to EC2 Instance
```bash
# Make sure your key file has correct permissions
chmod 400 Ujwal-DevOps-SRE.pem

# Connect to EC2
ssh -i Ujwal-DevOps-SRE.pem ec2-user@<EC2_PUBLIC_IP>
```

#### Step 2: Install Dependencies on EC2
```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo yum install git -y

# Install Python and pip
sudo yum install python3 python3-pip -y
```

#### Step 3: Deploy Application
```bash
# Clone repository
git clone <your-repository-url>
cd un-enterprises-project

# Update database configuration in app.py with RDS endpoint
vi app-layer/app.py
# Update rds_host with the actual RDS endpoint from Terraform output

# Build and run with Docker
docker-compose up -d --build
```

### 3. Production Configuration

#### Step 1: Use Production WSGI Server
Update `app-layer/Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Use Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "app:app"]
```

#### Step 2: Environment Variables
Create `.env` file:
```bash
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
RDS_HOST=your-rds-endpoint
RDS_USER=admin
RDS_PASSWORD=Ujwal9494
DATABASE_NAME=database-1
```

#### Step 3: Nginx Configuration (Optional)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/static/files;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## Features

### 1. Landing Page (`static/index.html`)
- **Hero Section**: Eye-catching introduction with call-to-action
- **Services Section**: Grid layout showcasing import/export services
- **About Section**: Company information and values
- **Contact Section**: Contact form and business information
- **Responsive Design**: Works on all device sizes
- **Smooth Animations**: CSS animations and JavaScript interactions

### 2. Contact Form
- **Form Fields**: Name, email, phone, message
- **Validation**: Client-side and server-side validation
- **Database Storage**: All submissions stored in MySQL
- **Flash Messages**: Success/error feedback
- **Email Validation**: Proper email format checking

### 3. Admin Panel (`/admin`)
- **View Submissions**: Table view of all contact form submissions
- **Data Display**: Name, email, phone, and message
- **Ordered by Date**: Most recent submissions first

### 4. Error Handling
- **404 Page**: Custom not found page
- **500 Page**: Custom server error page
- **Graceful Degradation**: Fallback for JavaScript disabled

## Configuration

### Environment Variables
```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key

# Database Configuration
RDS_HOST=your-rds-endpoint
RDS_USER=admin
RDS_PASSWORD=your-password
DATABASE_NAME=database-1

# AWS Configuration (if using AWS services)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=ap-south-1
```

### Database Configuration
The application automatically:
1. Connects to RDS MySQL
2. Creates database if it doesn't exist
3. Creates required tables
4. Sets up proper indexes

### Security Configuration
- **Secret Key**: Change the default secret key
- **Database Credentials**: Use strong passwords
- **Security Groups**: Limit access to required ports only
- **SSL/HTTPS**: Consider adding SSL certificate for production

## Troubleshooting

### Common Issues

#### 1. Database Connection Failed
```bash
# Check RDS endpoint
terraform output rds_endpoint

# Verify security groups allow connection
# Check app.py database configuration
```

#### 2. Application Not Loading
```bash
# Check if Flask is running
ps aux | grep flask

# Check port availability
netstat -tlnp | grep 5000

# Check Docker containers
docker ps
docker logs <container-id>
```

#### 3. Static Files Not Loading
```bash
# Verify file paths in HTML templates
# Check Flask static file configuration
# Ensure proper permissions
```

#### 4. Form Submission Errors
```bash
# Check database connectivity
# Verify table exists
# Check form field names match backend
```

### Debugging Steps

1. **Check Logs**:
```bash
# Docker logs
docker-compose logs -f

# Application logs
tail -f /var/log/flask/app.log
```

2. **Database Connectivity**:
```bash
# Test MySQL connection
mysql -h <rds-endpoint> -u admin -p
```

3. **Network Issues**:
```bash
# Check security groups
# Verify VPC configuration
# Test port connectivity
telnet <ec2-ip> 5000
```

## Maintenance

### Regular Tasks

1. **Database Backups**:
```bash
# RDS automated backups are enabled
# Manual backup if needed
mysqldump -h <rds-endpoint> -u admin -p database-1 > backup.sql
```

2. **Application Updates**:
```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose up -d --build
```

3. **Security Updates**:
```bash
# Update dependencies
pip list --outdated
pip install --upgrade package-name

# Update system packages
sudo yum update -y
```

4. **Monitoring**:
```bash
# Check application health
curl http://localhost:5000/

# Monitor system resources
htop
df -h
```

### Performance Optimization

1. **Database Optimization**:
- Add indexes for frequently queried columns
- Optimize database queries
- Consider connection pooling

2. **Application Optimization**:
- Use Redis for session storage
- Implement caching
- Optimize static file delivery

3. **Infrastructure Optimization**:
- Use CDN for static files
- Implement load balancing
- Set up auto-scaling

### Backup Strategy

1. **Database Backups**:
- Automated RDS backups (7-day retention)
- Weekly full backups to S3
- Point-in-time recovery enabled

2. **Application Backups**:
- Git repository serves as code backup
- Container images stored in registry
- Configuration files backed up

3. **Infrastructure Backups**:
- Terraform state file backup
- EC2 AMI snapshots
- VPC configuration documentation


