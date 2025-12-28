"""Unit tests for data processing utilities."""

import pytest
from src.utils.data_processing import parse_csv_from_string, validate_feedback_entry


def test_parse_csv_from_string():
    """Test CSV parsing from string."""
    csv_content = """feedback_id,feedback_text
fb_001,Great work environment
fb_002,Need better tools"""
    
    result = parse_csv_from_string(csv_content)
    
    assert len(result) == 2
    assert result[0]["feedback_id"] == "fb_001"
    assert result[1]["feedback_text"] == "Need better tools"


def test_parse_empty_csv():
    """Test parsing empty CSV."""
    csv_content = """feedback_id,feedback_text"""
    
    result = parse_csv_from_string(csv_content)
    
    assert len(result) == 0


def test_validate_feedback_entry_valid():
    """Test validation of valid feedback entry."""
    entry = {
        "feedback_id": "fb_001",
        "feedback_text": "Great work environment",
        "employee_id": "emp_123"
    }
    
    assert validate_feedback_entry(entry) is True


def test_validate_feedback_entry_missing_id():
    """Test validation with missing feedback_id."""
    entry = {
        "feedback_text": "Great work environment",
        "employee_id": "emp_123"
    }
    
    assert validate_feedback_entry(entry) is False


def test_validate_feedback_entry_missing_text():
    """Test validation with missing feedback_text."""
    entry = {
        "feedback_id": "fb_001",
        "employee_id": "emp_123"
    }
    
    assert validate_feedback_entry(entry) is False
