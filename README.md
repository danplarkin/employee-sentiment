# AI-Powered Employee Sentiment Dashboard

An end-to-end serverless application that analyzes employee feedback using AWS AI services and visualizes sentiment trends in real-time.

## Architecture Diagram

```
Employee Feedback → S3 Bucket → Lambda → AWS Comprehend → DynamoDB → Athena → QuickSight Dashboard
```

## Tech Stack

- **AWS Services:** S3, Lambda, Comprehend, DynamoDB, Athena, QuickSight
- **IaC:** Terraform or AWS CDK
- **Language:** Python for Lambda
- **Visualization:** QuickSight dashboard

## Project Overview

This project demonstrates expertise in:
- Serverless architecture design
- AWS AI/ML services (Comprehend)
- Event-driven processing
- Infrastructure as Code
- Data analytics and visualization
- HR Tech domain knowledge

## Step-by-Step Implementation

1. **Provision infrastructure** with Terraform/CDK (S3, Lambda, DynamoDB, Athena, QuickSight)
2. **Upload sample HR feedback CSV** to S3
3. **Lambda triggers** on S3 upload → calls Comprehend for sentiment analysis
4. **Store results** in DynamoDB
5. **Configure Athena** to query DynamoDB data
6. **Build QuickSight dashboard** for sentiment trends
7. **Automate everything** via IaC

## Repository Structure

```
/sentiment-dashboard
├── terraform/       # IaC scripts
├── lambda/          # Python code for sentiment analysis
├── data/            # Sample HR feedback
├── quicksight/      # Dashboard config
└── README.md        # Setup guide
```

## Getting Started

### Prerequisites

- AWS Account with appropriate permissions
- Terraform or AWS CDK installed
- Python 3.9+
- AWS CLI configured

### Installation

```bash
# Clone the repository
git clone https://github.com/danplarkin/employee-sentiment.git
cd employee-sentiment

# Deploy infrastructure
cd terraform
terraform init
terraform plan
terraform apply

# Upload sample data
aws s3 cp data/sample_feedback.csv s3://your-bucket-name/
```

## Features

- Real-time sentiment analysis of employee feedback
- Automated processing pipeline
- Scalable serverless architecture
- Interactive QuickSight dashboards
- Cost-efficient pay-per-use model

## Future Enhancements

- Add trend prediction using SageMaker
- Implement email alerts for negative sentiment spikes
- Multi-language support via Comprehend
- Integration with HR ticketing systems

## License

MIT

---

**Project Status:** In Development  
**Author:** Dan Larkin  
**Date:** December 2025
