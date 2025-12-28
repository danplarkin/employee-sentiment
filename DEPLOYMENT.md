# Deployment Guide - Employee Sentiment Dashboard

Complete guide for running this project locally and deploying to AWS.

---

## 📋 Prerequisites

### Required Tools
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **AWS CLI** - [Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- **Terraform 1.0+** - [Download](https://www.terraform.io/downloads)
- **Git** - Already installed ✓

### AWS Account Setup
1. Create or use existing AWS account
2. Create IAM user with these permissions:
   - S3 (full)
   - Lambda (full)
   - DynamoDB (full)
   - Comprehend (read/analyze)
   - Athena (full)
   - IAM (create roles)
   - CloudWatch Logs

3. Get Access Keys: IAM Console → Users → Security credentials → Create access key

---

## 🏠 Local Development

### 1. Setup Environment

```powershell
# Navigate to project
cd C:\Users\danpl\projects\utilities\employee-sentiment

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Run Tests Locally

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_sentiment_analyzer.py -v

# View coverage report
start htmlcov/index.html
```

### 3. Local Code Quality Checks

```powershell
# Format code
black src tests

# Lint code
flake8 src tests --max-line-length=100

# Type checking
mypy src --ignore-missing-imports
```

### 4. Test Lambda Function Locally

```powershell
# Create test event
$testEvent = @{
    Records = @(
        @{
            s3 = @{
                bucket = @{ name = "test-bucket" }
                object = @{ key = "test-feedback.csv" }
            }
        }
    )
} | ConvertTo-Json -Depth 10

# Save to file
$testEvent | Out-File -FilePath test_event.json

# Test with Python
python -c "
import json
from src.lambda_functions.sentiment_analyzer import lambda_handler

with open('test_event.json', 'r') as f:
    event = json.load(f)
    
# Note: Will fail without AWS resources, but validates code structure
print('Lambda handler is valid and importable')
"
```

### 5. Test Individual Functions

```powershell
# Test data processing
python -c "
from src.utils.data_processing import parse_csv_from_string

csv_data = '''feedback_id,feedback_text,employee_id
fb_001,Great work environment,emp_123
fb_002,Need better benefits,emp_456'''

result = parse_csv_from_string(csv_data)
print(f'Parsed {len(result)} records')
for record in result:
    print(f'  - {record}')
"

# Test AWS clients (requires AWS credentials)
python -c "
from src.utils.aws_clients import get_s3_client, get_comprehend_client
print('Testing AWS client creation...')
s3 = get_s3_client()
print(f'S3 client: {s3.meta.service_model.service_name}')
comprehend = get_comprehend_client()
print(f'Comprehend client: {comprehend.meta.service_model.service_name}')
"
```

---

## ☁️ AWS Deployment

### Step 1: Configure AWS Credentials

```powershell
# Configure AWS CLI (one-time setup)
aws configure

# Enter when prompted:
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region: us-east-1
# Default output format: json

# Verify configuration
aws sts get-caller-identity
```

### Step 2: Deploy Infrastructure with Terraform

```powershell
# Navigate to Terraform directory
cd infrastructure/terraform

# Initialize Terraform (first time only)
terraform init

# Preview changes
terraform plan

# Review the plan, then deploy
terraform apply

# Type 'yes' when prompted

# Save outputs (bucket names, table names, etc.)
terraform output
```

**Resources Created:**
- S3 bucket for feedback CSV files
- Lambda function for sentiment analysis
- DynamoDB table for results
- Athena database and tables
- IAM roles and policies
- CloudWatch log groups

### Step 3: Upload Sample Data

```powershell
# Get bucket name from Terraform output
$bucketName = terraform output -raw feedback_bucket_name

# Upload sample data
aws s3 cp ../../data/sample_feedback.csv s3://$bucketName/feedback/sample_feedback.csv

# Verify upload
aws s3 ls s3://$bucketName/feedback/
```

### Step 4: Monitor Execution

```powershell
# View Lambda logs
aws logs tail /aws/lambda/sentiment-analyzer --follow

# Check DynamoDB table
$tableName = terraform output -raw dynamodb_table_name
aws dynamodb scan --table-name $tableName --max-items 5

# Query Athena
aws athena start-query-execution `
    --query-string "SELECT * FROM sentiment_results LIMIT 10" `
    --result-configuration "OutputLocation=s3://$bucketName/athena-results/"
```

### Step 5: Setup QuickSight Dashboard (Optional)

1. **Enable QuickSight**:
   - Go to AWS Console → QuickSight
   - Sign up for QuickSight (30-day free trial)
   - Choose Standard Edition

2. **Connect to Athena**:
   - Create new dataset
   - Select Athena as source
   - Choose `sentiment_analysis` database
   - Select `sentiment_results` table

3. **Create Visualizations**:
   - Sentiment distribution (pie chart)
   - Sentiment by department (bar chart)
   - Sentiment over time (line chart)
   - Negative feedback word cloud

Full instructions: [quicksight/README.md](quicksight/README.md)

---

## 🔄 Development Workflow

### Making Changes

```powershell
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make code changes
# Edit files in src/

# 3. Run tests
pytest

# 4. Format and lint
black src tests
flake8 src tests

# 5. Commit changes
git add .
git commit -m "Description of changes"

# 6. Push to GitHub
git push origin feature/your-feature-name

# 7. Create Pull Request on GitHub
# GitHub Actions will run tests automatically
```

### Updating AWS Deployment

```powershell
# After making code changes
cd infrastructure/terraform

# Update Lambda function code
terraform apply -auto-approve

# Or redeploy specific resource
terraform taint aws_lambda_function.sentiment_analyzer
terraform apply
```

---

## 🧪 Testing in AWS

### Upload Test File

Create a test CSV file:
```csv
feedback_id,feedback_text,employee_id,department
fb_test_001,I love working here!,emp_999,Engineering
fb_test_002,Very disappointed with management,emp_998,HR
fb_test_003,Great team collaboration,emp_997,Marketing
```

Upload and test:
```powershell
# Upload test file
aws s3 cp test_feedback.csv s3://$bucketName/feedback/test_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv

# Watch logs in real-time
aws logs tail /aws/lambda/sentiment-analyzer --follow --since 1m

# Check results in DynamoDB
aws dynamodb scan --table-name $tableName --max-items 10 --query 'Items[?feedback_id==`fb_test_001`]'
```

---

## 📊 Monitoring & Troubleshooting

### Check Lambda Function Status

```powershell
# Get function info
aws lambda get-function --function-name sentiment-analyzer

# View recent invocations
aws lambda get-function --function-name sentiment-analyzer --query 'Configuration.[LastModified,State,StateReason]'

# Check CloudWatch metrics
aws cloudwatch get-metric-statistics `
    --namespace AWS/Lambda `
    --metric-name Invocations `
    --dimensions Name=FunctionName,Value=sentiment-analyzer `
    --start-time (Get-Date).AddHours(-1) `
    --end-time (Get-Date) `
    --period 3600 `
    --statistics Sum
```

### Common Issues

**Issue: Lambda timeout**
```powershell
# Increase timeout in main.tf
# Change timeout from 60 to 300 seconds
cd infrastructure/terraform
terraform apply
```

**Issue: Permission errors**
- Check IAM roles in [infrastructure/terraform/iam.tf](infrastructure/terraform/iam.tf)
- Verify Lambda has permissions for S3, DynamoDB, Comprehend

**Issue: No data in DynamoDB**
- Check Lambda logs: `aws logs tail /aws/lambda/sentiment-analyzer --follow`
- Verify S3 event trigger is configured
- Check CSV format matches expected schema

### View Costs

```powershell
# Get cost estimates
aws ce get-cost-and-usage `
    --time-period Start=2025-12-01,End=2025-12-28 `
    --granularity MONTHLY `
    --metrics UnblendedCost `
    --group-by Type=SERVICE
```

---

## 🗑️ Cleanup / Destroy Resources

### Destroy AWS Resources

```powershell
cd infrastructure/terraform

# Preview what will be destroyed
terraform plan -destroy

# Destroy all resources
terraform destroy

# Type 'yes' when prompted
```

**Important**: Empty S3 bucket first if you have data you want to keep:
```powershell
# Backup data
aws s3 sync s3://$bucketName ./backup/

# Empty bucket
aws s3 rm s3://$bucketName --recursive

# Then destroy
terraform destroy
```

---

## 📝 Configuration Options

### Environment Variables (Optional)

Create `.env` file for local development:
```bash
AWS_REGION=us-east-1
AWS_PROFILE=default
DYNAMODB_TABLE_NAME=sentiment-results
S3_BUCKET_NAME=your-bucket-name
```

### Terraform Variables

Edit [infrastructure/terraform/variables.tf](infrastructure/terraform/variables.tf):
- `project_name`: Change project prefix
- `environment`: dev/staging/prod
- `aws_region`: Change AWS region
- `lambda_timeout`: Adjust timeout
- `lambda_memory`: Adjust memory allocation

---

## 🚀 Quick Start Commands

```powershell
# Complete local setup
cd C:\Users\danpl\projects\utilities\employee-sentiment
pip install -r requirements.txt -r requirements-dev.txt
pytest

# Complete AWS deployment
aws configure
cd infrastructure/terraform
terraform init
terraform apply
$bucketName = terraform output -raw feedback_bucket_name
aws s3 cp ../../data/sample_feedback.csv s3://$bucketName/feedback/sample.csv
aws logs tail /aws/lambda/sentiment-analyzer --follow
```

---

## 📚 Additional Resources

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Amazon Comprehend](https://docs.aws.amazon.com/comprehend/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Project README](README.md)

---

## 🆘 Getting Help

**Local Development Issues**: Check [tests/unit/](tests/unit/) for examples

**AWS Issues**: Review [infrastructure/terraform/](infrastructure/terraform/) configs

**CI/CD Issues**: Check [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)
