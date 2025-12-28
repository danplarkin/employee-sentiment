# Terraform outputs

output "s3_bucket_name" {
  description = "Name of the S3 bucket for feedback uploads"
  value       = aws_s3_bucket.feedback_bucket.id
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table for sentiment results"
  value       = aws_dynamodb_table.sentiment_results.name
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.sentiment_analyzer.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.sentiment_analyzer.arn
}
