output "public_ips" {
  value = aws_instance.sample_backend.public_ip
}

output "private_ips" {
  value = aws_instance.sample_backend.private_ip
}