"""
Lambda function for employee sentiment analysis using AWS Comprehend.
Triggered by S3 uploads, processes feedback CSV, and stores results in DynamoDB.
"""

import json
import csv
import boto3
import os
from datetime import datetime
from io import StringIO
from typing import Dict, List

# Initialize AWS clients
s3_client = boto3.client('s3')
comprehend_client = boto3.client('comprehend')
dynamodb = boto3.resource('dynamodb')

# Get DynamoDB table name from environment variable
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
table = dynamodb.Table(DYNAMODB_TABLE)


def lambda_handler(event, context):
    """
    Main Lambda handler function.
    
    Args:
        event: S3 event notification
        context: Lambda context
    
    Returns:
        dict: Response with status and results
    """
    try:
        # Extract S3 bucket and key from event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        print(f"Processing file: s3://{bucket}/{key}")
        
        # Download and parse CSV from S3
        feedback_data = get_feedback_from_s3(bucket, key)
        
        # Analyze sentiment for each feedback entry
        results = analyze_sentiment_batch(feedback_data)
        
        # Store results in DynamoDB
        store_results_in_dynamodb(results)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully processed {len(results)} feedback entries',
                'processed_count': len(results)
            })
        }
        
    except Exception as e:
        print(f"Error processing feedback: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }


def get_feedback_from_s3(bucket: str, key: str) -> List[Dict]:
    """
    Download and parse CSV file from S3.
    
    Args:
        bucket: S3 bucket name
        key: S3 object key
    
    Returns:
        list: List of feedback dictionaries
    """
    # Download file from S3
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    
    # Parse CSV
    csv_reader = csv.DictReader(StringIO(content))
    feedback_list = list(csv_reader)
    
    print(f"Loaded {len(feedback_list)} feedback entries")
    return feedback_list


def analyze_sentiment_batch(feedback_data: List[Dict]) -> List[Dict]:
    """
    Analyze sentiment for a batch of feedback entries.
    
    Args:
        feedback_data: List of feedback dictionaries
    
    Returns:
        list: List of results with sentiment analysis
    """
    results = []
    
    # Process in batches of 25 (Comprehend limit)
    batch_size = 25
    for i in range(0, len(feedback_data), batch_size):
        batch = feedback_data[i:i + batch_size]
        
        # Extract text for sentiment analysis
        texts = [entry.get('feedback_text', '') for entry in batch]
        
        # Call Comprehend batch sentiment analysis
        comprehend_response = comprehend_client.batch_detect_sentiment(
            TextList=texts,
            LanguageCode='en'
        )
        
        # Combine results with original data
        for j, entry in enumerate(batch):
            sentiment_result = comprehend_response['ResultList'][j]
            
            result = {
                'feedback_id': entry.get('feedback_id', f'fb_{i+j}'),
                'employee_id': entry.get('employee_id', 'unknown'),
                'department': entry.get('department', 'unknown'),
                'feedback_text': entry.get('feedback_text', ''),
                'timestamp': int(datetime.now().timestamp()),
                'sentiment': sentiment_result['Sentiment'],
                'sentiment_scores': {
                    'positive': float(sentiment_result['SentimentScore']['Positive']),
                    'negative': float(sentiment_result['SentimentScore']['Negative']),
                    'neutral': float(sentiment_result['SentimentScore']['Neutral']),
                    'mixed': float(sentiment_result['SentimentScore']['Mixed'])
                }
            }
            results.append(result)
    
    return results


def store_results_in_dynamodb(results: List[Dict]):
    """
    Store sentiment analysis results in DynamoDB.
    
    Args:
        results: List of sentiment analysis results
    """
    with table.batch_writer() as batch:
        for result in results:
            batch.put_item(Item=result)
    
    print(f"Stored {len(results)} results in DynamoDB")
