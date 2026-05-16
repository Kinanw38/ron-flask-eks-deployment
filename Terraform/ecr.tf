resource "aws_ecr_repository" "repo" {
  name                 = "${var.project_name}-repo"
  image_tag_mutability = "MUTABLE"
  force_delete         = true # מאפשר מחיקה של ה-ECR גם אם יש בתוכו אימג'ים

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.project_name}-ecr"
  }
}