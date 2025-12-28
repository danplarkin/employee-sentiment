"""Unit tests for sentiment analyzer Lambda function."""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from moto import mock_s3, mock_dynamodb
import boto3


@pytest.fixture
def mock_s3_event():
    """Create mock S3 event."""
    return {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "test-bucket"},
                    "object": {"key": "test-file.csv"}
                }
            }
        ]
    }


@pytest.fixture
def sample_csv_content():
    """Sample CSV content for testing."""
    return """feedback_id,employee_id,department,feedback_text
fb_001,emp_123,Engineering,Great work environment
fb_002,emp_456,Marketing,Need better tools"""


@mock_s3
@mock_dynamodb
def test_lambda_handler_success(mock_s3_event, sample_csv_content):
    """Test successful Lambda execution."""
    # Setup mocks
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="test-bucket")
    s3.put_object(Bucket="test-bucket", Key="test-file.csv", Body=sample_csv_content)
    
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.create_table(
        TableName="test-table",
        KeySchema=[
            {"AttributeName": "feedback_id", "KeyType": "HASH"},
            {"AttributeName": "timestamp", "KeyType": "RANGE"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "feedback_id", "AttributeType": "S"},
            {"AttributeName": "timestamp", "AttributeType": "N"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )
    
    # Mock the Comprehend client to avoid actual API calls
    with patch('boto3.client') as mock_boto_client:
        mock_comprehend = MagicMock()
        mock_comprehend.batch_detect_sentiment.return_value = {
            'ResultList': [
                {'Index': 0, 'Sentiment': 'POSITIVE', 'SentimentScore': {'Positive': 0.95}},
                {'Index': 1, 'Sentiment': 'NEGATIVE', 'SentimentScore': {'Negative': 0.85}}
            ]
        }
        
        def client_selector(service_name, **kwargs):
            if service_name == 's3':
                return s3
            elif service_name == 'dynamodb':
                return boto3.client('dynamodb', region_name='us-east-1')
            elif service_name == 'comprehend':
                return mock_comprehend
            return MagicMock()
        
        mock_boto_client.side_effect = client_selector
        
        # Import here to use mocked clients
        from src.lambda_functions.sentiment_analyzer import lambda_handler
        
        # Execute
        response = lambda_handler(mock_s3_event, None)
        
        # Verify
        assert response['statusCode'] == 200
        assert 'Successfully processed' in response['body']


def test_csv_parsing():
    """Test CSV parsing functionality."""
    from src.utils.data_processing import parse_csv
    
    csv_content = """feedback_id,employee_id,department,feedback_text
fb_001,emp_123,Engineering,Great work"""
    
    result = parse_csv(csv_content)
    assert len(result) == 1
    assert result[0]['feedback_id'] == 'fb_001'
