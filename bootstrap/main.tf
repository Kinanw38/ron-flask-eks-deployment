provider "aws" {
  region = "us-east-1"
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "terraform_state" {
  # השם יהיה למשל: ron-devops-state-a1b2c3d4
  bucket = "ron-devops-state-${random_id.suffix.hex}"

  lifecycle {
    prevent_destroy = true # חשוב מאוד לראיונות: הגנה על ה-State
  }
}

resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

output "state_bucket_name" {
  value = aws_s3_bucket.terraform_state.bucket
}
