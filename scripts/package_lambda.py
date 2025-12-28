#!/usr/bin/env python3
"""Script to package Lambda function for deployment."""

import os
import shutil
import zipfile
from pathlib import Path


def package_lambda(source_dir: str, output_file: str, requirements_file: str = None):
    """
    Package Lambda function with dependencies.
    
    Args:
        source_dir: Directory containing Lambda code
        output_file: Output zip file path
        requirements_file: Path to requirements.txt (optional)
    """
    print(f"Packaging Lambda function from {source_dir}...")
    
    # Create temp directory for packaging
    temp_dir = Path("temp_package")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Copy source code
        for file in Path(source_dir).glob("*.py"):
            shutil.copy(file, temp_dir)
        
        # Install dependencies if requirements file exists
        if requirements_file and Path(requirements_file).exists():
            print("Installing dependencies...")
            os.system(f"pip install -r {requirements_file} -t {temp_dir} --upgrade")
        
        # Create zip file
        print(f"Creating {output_file}...")
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                # Skip __pycache__ directories
                dirs[:] = [d for d in dirs if d != '__pycache__']
                
                for file in files:
                    if not file.endswith('.pyc'):
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(temp_dir)
                        zipf.write(file_path, arcname)
        
        print(f"Successfully created {output_file}")
        print(f"Package size: {Path(output_file).stat().st_size / 1024:.2f} KB")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    package_lambda(
        source_dir="src/lambda_functions",
        output_file="sentiment_analyzer.zip",
        requirements_file="requirements.txt"
    )
