.PHONY: help install install-dev test lint format clean deploy package

help:
	@echo "Available commands:"
	@echo "  install       Install production dependencies"
	@echo "  install-dev   Install development dependencies"
	@echo "  test          Run tests with coverage"
	@echo "  lint          Run linting (flake8, mypy)"
	@echo "  format        Format code with black"
	@echo "  clean         Remove build artifacts"
	@echo "  package       Package Lambda functions"
	@echo "  deploy        Deploy infrastructure with Terraform"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest

lint:
	flake8 src tests
	mypy src

format:
	black src tests

clean:
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .coverage htmlcov
	rm -rf **/__pycache__
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

package:
	cd src/lambda_functions && zip -r ../../sentiment_analyzer.zip . -x "*.pyc" -x "__pycache__/*"

deploy:
	cd infrastructure/terraform && terraform init && terraform apply
