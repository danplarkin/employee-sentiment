"""Data processing utilities."""

import csv
from io import StringIO
from typing import List, Dict


def parse_csv_from_string(content: str) -> List[Dict]:
    """
    Parse CSV content from string.
    
    Args:
        content: CSV content as string
        
    Returns:
        List of dictionaries representing CSV rows
    """
    csv_reader = csv.DictReader(StringIO(content))
    return list(csv_reader)


def validate_feedback_entry(entry: Dict) -> bool:
    """
    Validate feedback entry has required fields.
    
    Args:
        entry: Feedback dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["feedback_id", "feedback_text"]
    return all(field in entry for field in required_fields)
