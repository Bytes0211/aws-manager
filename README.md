# AWS Manager ☁️

A Python-based AWS service management library providing simplified interfaces for AWS Lambda, S3, and EC2 operations.

## ✨ Features

- **Lambda Management** ⚡: Invoke, update, and list Lambda functions
- **S3 Operations** 🪣: Bucket creation, file uploads, versioning, and batch operations
- **EC2 Management** 🖥️: Instance creation, starting, stopping, and termination
- **Lambda Deployment** 📦: Complete deployment pipeline with dependency packaging

## 📥 Installation

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Create a `.env` file in the project root with your AWS credentials and configuration:

```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
```

## 🚀 Usage

### Basic Example

```python
from aws_manager import AWSManager

# List all Lambda functions
AWSManager.list_functions()

# Invoke a Lambda function
response = AWSManager.invoke_function(
    function_name='my-function',
    function_params={'key': 'value'},
    get_log=True
)
```

## 📚 API Reference

### ⚡ Lambda Operations

#### `invoke_function(function_name, function_params, get_log=False)`

Invokes a Lambda function with the specified parameters.

**Parameters:**

- `function_name` (str): Name of the Lambda function
- `function_params` (dict): Parameters to pass to the function
- `get_log` (bool): Whether to retrieve execution logs

**Returns:** Response dictionary from Lambda invocation

#### `update_function_code(function_name, deployment_package)`

Updates Lambda function code with a .zip archive.

**Parameters:**

- `function_name` (str): Name of the Lambda function
- `deployment_package` (bytes): Bytes of the .zip deployment package

#### `update_function_configuration(function_name, env_vars)`

Updates Lambda function environment variables.

**Parameters:**

- `function_name` (str): Name of the Lambda function
- `env_vars` (dict): Dictionary of environment variables

#### `list_functions()`

Lists all Lambda functions in the current account with details.

### 🪣 S3 Operations

#### `create_bucket(bucket_prefix)`

Creates an S3 bucket with proper region configuration.

**Parameters:**

- `bucket_prefix` (str): Prefix for the bucket name

**Returns:** Tuple of (bucket_name, bucket_response)

#### `list_buckets()`

Lists all S3 buckets in the account.

#### `list_bucket_objects(bucket_name)`

Lists all objects in a specific S3 bucket.

**Parameters:**

- `bucket_name` (str): Name of the S3 bucket

#### `add_file_to_bucket(bucket_name, file_name, object_name, url=None)`

Uploads a file to S3 from local path or URL.

**Parameters:**

- `bucket_name` (str): Name of the S3 bucket
- `file_name` (str): Name of the file to upload
- `object_name` (str): Name for the object in S3
- `url` (str, optional): URL to download file from

**Returns:** Tuple of (status_code, message)

#### `copy_to_bucket(from_bucket, to_bucket, file_name)`

Copies an object between S3 buckets.

**Parameters:**

- `from_bucket` (str): Source bucket name
- `to_bucket` (str): Destination bucket name
- `file_name` (str): Name of the file to copy

**Returns:** Success message string

#### `delete_files_from_bucket(bucket_name, file_list)`

Deletes multiple files from an S3 bucket efficiently.

**Parameters:**

- `bucket_name` (str): Name of the S3 bucket
- `file_list` (list): List of file keys to delete

**Returns:** Tuple of (status_code, message)

#### `enable_bucket_versioning(bucket_name)`

Enables versioning for an S3 bucket.

**Parameters:**

- `bucket_name` (str): Name of the S3 bucket

**Returns:** Success message with versioning status

### 🖥️ EC2 Operations

#### `create_ec2(image_id, instance_type='t2.micro', min_count=1, max_count=1, key_name=None, security_group_ids=None, subnet_id=None, tags=None)`

Creates EC2 instance(s) with specified configuration.

**Parameters:**

- `image_id` (str): AMI ID to use for the instance
- `instance_type` (str): EC2 instance type (default: 't2.micro')
- `min_count` (int): Minimum number of instances (default: 1)
- `max_count` (int): Maximum number of instances (default: 1)
- `key_name` (str, optional): Name of the key pair for SSH access
- `security_group_ids` (list, optional): List of security group IDs
- `subnet_id` (str, optional): Subnet ID for the instance
- `tags` (list, optional): List of tags to apply

**Returns:** Tuple of (status_code, list of instance IDs)

#### `start_ec2(instance_ids)`

Starts one or more EC2 instances.

**Parameters:**

- `instance_ids` (list): List of EC2 instance IDs to start

**Returns:** Tuple of (status_code, response)

#### `stop_ec2(instance_ids)`

Stops one or more EC2 instances.

**Parameters:**

- `instance_ids` (list): List of EC2 instance IDs to stop

**Returns:** Tuple of (status_code, response)

#### `list_ec2s()`

Lists all EC2 instances with details including ID, state, type, and IP addresses.

#### `remove_ec2s(instance_ids)`

Terminates one or more EC2 instances.

**Parameters:**

- `instance_ids` (list): List of EC2 instance IDs to terminate

**Returns:** Tuple of (status_code, response)

## 📦 Lambda Deployment

The project includes a comprehensive Lambda deployment system via the `LambdaDeployer` class. See [aws_lambda_deployment_guide.md](aws_lambda_deployment_guide.md) for detailed instructions.

### Quick Lambda Deployment

```python
from resources.lambdadeployer import LambdaDeployer

deployer = LambdaDeployer()

# Install dependencies
deployer.install_lambda_dependencies('requirements_lambda.txt', 'package')

# Create deployment package
deployer.create_lambda_package(
    source_files=['lambda_function.py', 'package'],
    package_name='deployment.zip'
)

# Create IAM role with specific permissions
role_arn = deployer.create_function_specific_role(
    function_name='my-function',
    required_services=['s3', 'dynamodb']
)

# Deploy function
deployer.deploy_lambda_function(
    function_name='my-function',
    zip_file='deployment.zip',
    handler='lambda_function.handler',
    role_arn=role_arn,
    runtime='python3.13',
    timeout=300,
    memory_size=256,
    environment_vars={'ENV': 'production'}
)

# Test function
deployer.test_lambda_function(
    function_name='my-function',
    test_payload={'key': 'value'}
)
```

## 📁 Project Structure

```bash
aws-manager/
├── aws_manager.py              # Main AWSManager class with static methods
├── resources/
│   ├── aws.py                 # Core AWS service wrapper
│   ├── lambdadeployer.py      # Lambda deployment utilities
│   └── util.py                # Utility functions and client factories
├── requirements.txt           # Project dependencies
├── requirements_lambda.txt    # Lambda-specific dependencies
├── test.py                   # Test file
└── aws_lambda_deployment_guide.md  # Comprehensive deployment guide
```

## 📋 Requirements

- Python 3.7+
- boto3 >= 1.40.59
- python-dotenv >= 1.1.1
- requests >= 2.32.5

See [requirements.txt](requirements.txt) for full dependency list.

## 💡 Best Practices

### 🔒 Security

- Store AWS credentials in environment variables or AWS credentials file
- Use IAM roles with least-privilege permissions
- Never commit credentials to version control
- Use AWS Secrets Manager for sensitive data in Lambda functions

### ⚡ Performance

- Reuse AWS client instances when possible (handled automatically by util.py)
- Use batch operations for S3 deletions
- Right-size Lambda memory allocations based on workload
- Keep Lambda packages under 50MB for direct upload

### 💰 Cost Optimization

- Use `t2.micro` instances for development/testing
- Enable S3 bucket versioning only when needed
- Set appropriate Lambda timeout values
- Clean up unused EC2 instances and S3 buckets

## ⚠️ Error Handling

All methods include comprehensive error handling with informative error messages:

```python
try:
    AWSManager.invoke_function('my-function', {'key': 'value'})
except Exception as e:
    print(f"Error: {e}")
```

## 📄 License

This project is intended for personal/educational use.

## 🤝 Contributing

Contributions are welcome! Please ensure all code follows existing patterns and includes appropriate error handling.

## 💬 Support

For issues related to AWS services, consult the [AWS Documentation](https://docs.aws.amazon.com/).

For deployment-specific questions, refer to [aws_lambda_deployment_guide.md](aws_lambda_deployment_guide.md).
