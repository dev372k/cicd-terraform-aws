resource "aws_instance" "sample_backend" {
  ami           = var.ami
  instance_type = var.instance_type
  key_name      = var.key_name

  vpc_security_group_ids = [var.security_group_id]

  user_data = <<-EOF
              #!/bin/bash

              apt-get update -y

              # Install Docker
              apt-get install -y docker.io

              # Start Docker
              systemctl start docker
              systemctl enable docker

              # Add ubuntu user to docker group
              usermod -aG docker ubuntu

              # Create env file
              cat > .env <<EOL
              APP_NAME=sample backend server
              VERSION=1.0.6
              ENVIRONMENT=DEV
              LOG_LEVEL=INFO
              EOL

              chown ubuntu:ubuntu .env
              EOF

  tags = {
    Name = "sample-backend-server"
  }
}