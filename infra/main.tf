resource "aws_s3_bucket" "main_bucket" {
  bucket = "tanayseven.com-simple-bucket"
  acl    = "private"

  tags = {
    Name        = "Simple bucket"
    Environment = "Dev"
  }
}

