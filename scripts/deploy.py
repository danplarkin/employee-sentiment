#!/usr/bin/env python3
"""Script to deploy infrastructure using Terraform."""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command: list, cwd: str = None):
    """Run shell command and handle errors."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    
    print(result.stdout)
    return result


def deploy():
    """Deploy infrastructure with Terraform."""
    terraform_dir = Path("infrastructure/terraform")
    
    if not terraform_dir.exists():
        print(f"Error: {terraform_dir} does not exist")
        sys.exit(1)
    
    print("=" * 50)
    print("Deploying Employee Sentiment Dashboard")
    print("=" * 50)
    
    # Initialize Terraform
    print("\n1. Initializing Terraform...")
    run_command(["terraform", "init"], cwd=str(terraform_dir))
    
    # Validate configuration
    print("\n2. Validating Terraform configuration...")
    run_command(["terraform", "validate"], cwd=str(terraform_dir))
    
    # Plan deployment
    print("\n3. Planning deployment...")
    run_command(["terraform", "plan"], cwd=str(terraform_dir))
    
    # Ask for confirmation
    response = input("\nDo you want to apply these changes? (yes/no): ")
    if response.lower() != "yes":
        print("Deployment cancelled")
        sys.exit(0)
    
    # Apply changes
    print("\n4. Applying changes...")
    run_command(["terraform", "apply", "-auto-approve"], cwd=str(terraform_dir))
    
    print("\n" + "=" * 50)
    print("Deployment completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    deploy()
