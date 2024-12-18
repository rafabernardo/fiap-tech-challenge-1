resource "aws_ecr_repository" "my_ecr_repo" {
  name                 = "ecr-fiap-image"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}
