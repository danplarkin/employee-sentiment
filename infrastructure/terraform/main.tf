# Main Terraform configuration for Employee Sentiment Dashboard
# Provisions S3, Lambda, DynamoDB, Athena, and QuickSight resources

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 bucket for employee feedback uploads
resource "aws_s3_bucket" "feedback_bucket" {
  bucket = "${var.project_name}-feedback-${var.environment}"
  
  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# DynamoDB table for sentiment results
resource "aws_dynamodb_table" "sentiment_results" {
  name           = "${var.project_name}-results-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "feedback_id"
  range_key      = "timestamp"

  attribute {
    name = "feedback_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# Lambda function for sentiment analysis
resource "aws_lambda_function" "sentiment_analyzer" {
  filename         = "../lambda/sentiment_analyzer.zip"
  function_name    = "${var.project_name}-analyzer-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "handler.lambda_handler"
  runtime         = "python3.11"
  timeout         = 300
  memory_size     = 512

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.sentiment_results.name
    }
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# S3 trigger for Lambda
resource "aws_s3_bucket_notification" "feedback_notification" {
  bucket = aws_s3_bucket.feedback_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.sentiment_analyzer.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".csv"
  }
}

# Lambda permission for S3 trigger
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.sentiment_analyzer.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.feedback_bucket.arn
}
