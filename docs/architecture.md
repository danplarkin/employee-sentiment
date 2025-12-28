# Architecture Documentation

## System Architecture

The Employee Sentiment Dashboard follows a serverless, event-driven architecture on AWS.

### Components

1. **S3 Bucket**: Stores incoming employee feedback CSV files
2. **Lambda Function**: Processes feedback and analyzes sentiment
3. **AWS Comprehend**: Provides AI-powered sentiment analysis
4. **DynamoDB**: Stores sentiment analysis results
5. **Athena**: Enables SQL queries on DynamoDB data
6. **QuickSight**: Visualizes sentiment trends

### Data Flow

```
1. Upload CSV → S3
2. S3 triggers → Lambda
3. Lambda reads CSV → parses data
4. Lambda calls → Comprehend API
5. Comprehend returns → sentiment scores
6. Lambda stores → DynamoDB
7. Athena queries → DynamoDB
8. QuickSight visualizes → query results
```

### Security

- IAM roles with least privilege access
- S3 bucket encryption at rest
- DynamoDB encryption enabled
- VPC endpoints for private communication (optional)

### Scalability

- Serverless architecture scales automatically
- Lambda concurrency: up to 1000 concurrent executions
- DynamoDB: on-demand capacity mode
- S3: unlimited storage

### Cost Optimization

- Pay-per-use pricing model
- No idle resources
- DynamoDB on-demand billing
- S3 lifecycle policies for archiving

## Deployment

See [deployment guide](../scripts/deploy.py) for instructions.
