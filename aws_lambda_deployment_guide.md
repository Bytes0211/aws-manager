# AWS Lambda Deployment with Python Modules - Complete Guide

## Overview
This guide shows you how to deploy Python Lambda functions with custom modules and third-party dependencies using boto3.

## 🚀 Quick Start

### 1. Project Structure
```
your-project/
├── lambda_function.py      # Main Lambda handler
├── util.py                # Your custom modules
├── aws.py                 # AWS helper functions
├── requirements.txt       # Dependencies
├── package/              # Auto-generated dependencies
│   ├── requests/
│   ├── boto3/
│   └── other_packages/
└── deployment.zip        # Final package
```

### 2. Install Dependencies
```bash
# Install to package directory for Lambda
pip install -r requirements.txt -t package/ --no-deps

# Or install specific packages
pip install requests boto3 python-dotenv -t package/
```

### 3. Create Deployment Package
Include these files in your zip:
- Your Python files (`*.py`)
- `package/` directory (contains dependencies)
- Any other resources your Lambda needs

### 4. Deploy Using Boto3
Use the AWS SDK to deploy your packaged Lambda function.

## 📋 Detailed Steps

### Step 1: Prepare Your Lambda Function

**Example Lambda Handler** (`github_function.py`):
```python
import json
import boto3
import requests
from util import some_utility_function  # Your custom module

def upload_handler(event, context):
    """
    Lambda handler function.
    
    Args:
        event: Lambda event data
        context: Lambda context object
    
    Returns:
        dict: Response with statusCode and body
    """
    try:
        # Use your custom modules
        result = some_utility_function(event.get('data'))
        
        # Use third-party libraries
        response = requests.get('https://api.example.com')
        
        # Use AWS services
        s3 = boto3.client('s3')
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Success',
                'result': result
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### Step 2: Manage Dependencies

**Best Practices for `requirements.txt`:**
```txt
# Keep dependencies minimal for faster cold starts
boto3==1.34.162          # AWS SDK
requests==2.32.5         # HTTP library
python-dotenv==1.0.0     # Environment variables

# Avoid heavy libraries in Lambda:
# pandas  # ~50MB - Use sparingly
# numpy   # ~20MB - Consider alternatives
# scipy   # ~30MB - Often unnecessary
```

**Installation Commands:**
```bash
# Method 1: From requirements.txt
pip install -r requirements.txt -t package/ --no-deps

# Method 2: Individual packages
pip install requests -t package/
pip install boto3 -t package/

# Method 3: With upgrade and no cache
pip install -r requirements.txt -t package/ --upgrade --no-cache-dir --no-deps
```

### Step 3: Create Deployment Package

**Automated Packaging Script:**
```python
from zipfile import ZipFile
from pathlib import Path

def create_deployment_package(source_files, output_name):
    """Create a Lambda deployment package."""
    with ZipFile(output_name, 'w') as zipf:
        for item in source_files:
            item_path = Path(item)
            
            if item_path.is_file():
                zipf.write(item_path, item_path.name)
            elif item_path.is_dir():
                for file_path in item_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(item_path.parent)
                        zipf.write(file_path, arcname)

# Usage
files_to_package = [
    'github_function.py',
    'util.py', 
    'aws.py',
    'package'  # Dependencies directory
]

create_deployment_package(files_to_package, 'lambda_deployment.zip')
```

### Step 4: Deploy with Boto3

**Deployment Script:**
```python
import boto3
import json

def deploy_lambda_function():
    # Initialize clients
    lambda_client = boto3.client('lambda')
    iam_client = boto3.client('iam')
    
    # Get IAM role ARN
    role_name = 'lambda-execution-role'
    role_response = iam_client.get_role(RoleName=role_name)
    role_arn = role_response['Role']['Arn']
    
    # Read deployment package
    with open('lambda_deployment.zip', 'rb') as f:
        zip_content = f.read()
    
    # Function configuration
    function_config = {
        'FunctionName': 'my-lambda-function',
        'Runtime': 'python3.9',  # or python3.10, python3.11
        'Role': role_arn,
        'Handler': 'github_function.upload_handler',
        'Code': {'ZipFile': zip_content},
        'Description': 'Lambda function with custom modules',
        'Timeout': 300,  # 5 minutes
        'MemorySize': 256,  # MB
        'Environment': {
            'Variables': {
                'ENV': 'production',
                'LOG_LEVEL': 'INFO'
            }
        }
    }
    
    try:
        # Try to update existing function
        response = lambda_client.update_function_code(
            FunctionName=function_config['FunctionName'],
            ZipFile=zip_content
        )
        print("✅ Function updated")
        
    except lambda_client.exceptions.ResourceNotFoundException:
        # Create new function
        response = lambda_client.create_function(**function_config)
        print("✅ Function created")
    
    return response

# Deploy the function
result = deploy_lambda_function()
print(f"Function ARN: {result['FunctionArn']}")
```

### Step 5: Test Your Function

**Testing Script:**
```python
def test_lambda_function(function_name, test_payload):
    """Test the deployed Lambda function."""
    lambda_client = boto3.client('lambda')
    
    response = lambda_client.invoke(
        FunctionName=function_name,
        Payload=json.dumps(test_payload)
    )
    
    result = response['Payload'].read().decode('utf-8')
    print(f"Response: {result}")
    return result

# Test with sample data
test_data = {
    'bucket_name': 'my-test-bucket',
    'file_name': 'test.json',
    'url': 'https://example.com'
}

test_lambda_function('my-lambda-function', test_data)
```

## ⚠️ Common Issues & Solutions

### 1. Package Size Limits
- **Direct Upload**: 50 MB limit
- **S3 Upload**: 250 MB limit (unzipped)
- **Solutions**: 
  - Remove unused dependencies
  - Use Lambda Layers for common libraries
  - Upload large packages via S3

### 2. Import Errors
```python
# ❌ Wrong - modules not in Python path
import my_module

# ✅ Correct - ensure modules are at root level
from my_module import function_name
```

### 3. Dependency Conflicts
```bash
# Use --no-deps to avoid conflicts with Lambda runtime
pip install requests -t package/ --no-deps
```

### 4. Permission Issues
Ensure your IAM role has:
- `AWSLambdaBasicExecutionRole` (minimum)
- Additional permissions for AWS services you use (S3, DynamoDB, etc.)

## 🎯 Best Practices

### Performance
1. **Keep packages small** - Faster cold starts
2. **Reuse connections** - Initialize clients outside handler
3. **Use Lambda Layers** - For common dependencies
4. **Optimize memory** - Right-size for your workload

### Security
1. **Least privilege IAM** - Minimal required permissions
2. **Environment variables** - For configuration, not secrets
3. **AWS Secrets Manager** - For sensitive data
4. **VPC configuration** - If accessing private resources

### Monitoring
1. **CloudWatch Logs** - Built-in logging
2. **Custom metrics** - Track business metrics
3. **Error handling** - Proper exception management
4. **Dead letter queues** - For failed invocations

## 📁 Example File Structure

```
github-download/
├── github_function.py      # Main Lambda handler
├── util.py                # Utility functions
├── aws.py                 # AWS operations
├── requirements.txt       # Dependencies
├── package/              # Auto-installed deps
│   ├── requests/
│   ├── certifi/
│   └── urllib3/
├── admin.ipynb           # Deployment notebook
├── lambda_deployment.zip  # Final package
└── README.md             # Documentation
```

This structure allows you to:
- Develop locally with your modules
- Package everything for Lambda
- Deploy using boto3
- Test and iterate quickly

## 🔧 Troubleshooting

**Import Errors:**
```python
# Add this to your Lambda function for debugging
import sys
print("Python path:", sys.path)

import os
print("Current directory contents:", os.listdir('.'))
print("Package directory contents:", os.listdir('./package'))
```

**Memory Issues:**
- Increase Lambda memory allocation
- Profile your code to find memory leaks
- Consider streaming for large data processing

**Timeout Issues:**
- Increase timeout setting (max 15 minutes)
- Optimize code performance
- Consider async processing for long tasks

Remember: AWS Lambda is designed for short-lived, stateless functions. For long-running processes, consider ECS, EC2, or other compute services.