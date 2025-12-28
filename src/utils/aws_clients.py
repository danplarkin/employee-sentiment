"""AWS client utilities."""

import boto3
from typing import Optional


def get_s3_client(region: str = "us-east-1") -> boto3.client:
    """Get S3 client."""
    return boto3.client("s3", region_name=region)


def get_comprehend_client(region: str = "us-east-1") -> boto3.client:
    """Get Comprehend client."""
    return boto3.client("comprehend", region_name=region)


def get_dynamodb_resource(region: str = "us-east-1") -> boto3.resource:
    """Get DynamoDB resource."""
    return boto3.resource("dynamodb", region_name=region)
