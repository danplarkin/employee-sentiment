"""Unit tests for AWS client utilities."""

import pytest
from src.utils.aws_clients import get_s3_client, get_comprehend_client, get_dynamodb_resource


def test_get_s3_client():
    """Test S3 client creation."""
    client = get_s3_client()
    assert client is not None
    assert client.meta.service_model.service_name == "s3"


def test_get_comprehend_client():
    """Test Comprehend client creation."""
    client = get_comprehend_client()
    assert client is not None
    assert client.meta.service_model.service_name == "comprehend"


def test_get_dynamodb_resource():
    """Test DynamoDB resource creation."""
    resource = get_dynamodb_resource()
    assert resource is not None
