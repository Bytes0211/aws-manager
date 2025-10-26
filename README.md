# AWS Manager ☁️

A Python-based AWS service management library providing simplified interfaces for AWS Lambda, S3, EC2, and DynamoDB operations.

## ✨ Features

- **Lambda Management** ⚡: Invoke, update, and list Lambda functions
- **S3 Operations** 🪣: Bucket creation, file uploads, versioning, and batch operations
- **EC2 Management** 🖥️: Instance creation, starting, stopping, and termination
- **DynamoDB Operations** 🗄️: Table management and full CRUD operations (AWS & Local)
- **Local DynamoDB Support** 💻: Connect to localhost DynamoDB for development/testing
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

# List all DynamoDB tables
AWSManager.list_dynamodb_tables()

# Create and query a DynamoDB table
AWSManager.create_dynamodb_table(
    table_name='Users',
    key_schema=[{'AttributeName': 'userId', 'KeyType': 'HASH'}],
    attribute_definitions=[{'AttributeName': 'userId', 'AttributeType': 'S'}]
)

# Insert an item
AWSManager.put_item_dynamodb('Users', {'userId': '123', 'name': 'John Doe'})
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

### 🗄️ DynamoDB Operations

#### `create_dynamodb_table(table_name, key_schema, attribute_definitions, provisioned_throughput=None, billing_mode='PAY_PER_REQUEST', global_secondary_indexes=None, local_secondary_indexes=None, tags=None)`

Creates a DynamoDB table with specified configuration.

**Parameters:**

- `table_name` (str): Name of the DynamoDB table
- `key_schema` (list): List defining partition key and sort key (e.g., `[{'AttributeName': 'id', 'KeyType': 'HASH'}]`)
- `attribute_definitions` (list): List of attribute definitions (e.g., `[{'AttributeName': 'id', 'AttributeType': 'S'}]`)
- `provisioned_throughput` (dict, optional): ReadCapacityUnits and WriteCapacityUnits (only for PROVISIONED mode)
- `billing_mode` (str): 'PAY_PER_REQUEST' or 'PROVISIONED' (default: 'PAY_PER_REQUEST')
- `global_secondary_indexes` (list, optional): List of global secondary indexes
- `local_secondary_indexes` (list, optional): List of local secondary indexes
- `tags` (list, optional): List of tags to apply to the table

**Returns:** Tuple of (status_code, table)

**Example:**

```python
AWSManager.create_dynamodb_table(
    table_name='Products',
    key_schema=[
        {'AttributeName': 'productId', 'KeyType': 'HASH'},
        {'AttributeName': 'category', 'KeyType': 'RANGE'}
    ],
    attribute_definitions=[
        {'AttributeName': 'productId', 'AttributeType': 'S'},
        {'AttributeName': 'category', 'AttributeType': 'S'}
    ]
)
```

#### `put_item_dynamodb(table_name, item)`

Inserts or updates an item in a DynamoDB table.

**Parameters:**

- `table_name` (str): Name of the DynamoDB table
- `item` (dict): Dictionary representing the item to insert/update

**Returns:** Tuple of (status_code, response)

**Example:**

```python
AWSManager.put_item_dynamodb('Products', {
    'productId': 'P123',
    'category': 'Electronics',
    'name': 'Laptop',
    'price': 999.99
})
```

#### `get_item_dynamodb(table_name, key)`

Retrieves an item from a DynamoDB table by key.

**Parameters:**

- `table_name` (str): Name of the DynamoDB table
- `key` (dict): Dictionary representing the primary key (e.g., `{'productId': 'P123'}`)

**Returns:** Dictionary containing the item, or empty dict if not found

**Example:**

```python
item = AWSManager.get_item_dynamodb('Products', {'productId': 'P123', 'category': 'Electronics'})
print(item)
```

#### `update_item_dynamodb(table_name, key, update_expression, expression_attribute_values=None, expression_attribute_names=None, return_values='ALL_NEW')`

Updates an item in a DynamoDB table.

**Parameters:**

- `table_name` (str): Name of the DynamoDB table
- `key` (dict): Dictionary representing the primary key
- `update_expression` (str): Expression defining the update (e.g., `'SET price = :val'`)
- `expression_attribute_values` (dict, optional): Dictionary mapping expression values (e.g., `{':val': 899.99}`)
- `expression_attribute_names` (dict, optional): Dictionary mapping expression attribute names
- `return_values` (str): What to return after update (default: 'ALL_NEW')

**Returns:** Tuple of (status_code, response)

**Example:**

```python
AWSManager.update_item_dynamodb(
    table_name='Products',
    key={'productId': 'P123', 'category': 'Electronics'},
    update_expression='SET price = :price, stock = :stock',
    expression_attribute_values={':price': 899.99, ':stock': 50}
)
```

#### `delete_item_dynamodb(table_name, key)`

Deletes an item from a DynamoDB table.

**Parameters:**

- `table_name` (str): Name of the DynamoDB table
- `key` (dict): Dictionary representing the primary key

**Returns:** Tuple of (status_code, response)

**Example:**

```python
AWSManager.delete_item_dynamodb('Products', {'productId': 'P123', 'category': 'Electronics'})
```

#### `query_dynamodb(table_name, key_condition_expression, expression_attribute_values=None, expression_attribute_names=None, filter_expression=None, index_name=None)`

Queries a DynamoDB table with a key condition.

**Parameters:**

- `table_name` (str): Name of the DynamoDB table
- `key_condition_expression` (str): Key condition for the query
- `expression_attribute_values` (dict, optional): Dictionary mapping expression values
- `expression_attribute_names` (dict, optional): Dictionary mapping expression attribute names
- `filter_expression` (str, optional): Optional filter expression
- `index_name` (str, optional): Optional index name to query against

**Returns:** List of items matching the query

**Example:**

```python
from boto3.dynamodb.conditions import Key

items = AWSManager.query_dynamodb(
    table_name='Products',
    key_condition_expression=Key('productId').eq('P123')
)
```

#### `scan_dynamodb(table_name, filter_expression=None, expression_attribute_values=None, expression_attribute_names=None)`

Scans a DynamoDB table (reads all items).

**Parameters:**

- `table_name` (str): Name of the DynamoDB table
- `filter_expression` (str, optional): Optional filter expression
- `expression_attribute_values` (dict, optional): Dictionary mapping expression values
- `expression_attribute_names` (dict, optional): Dictionary mapping expression attribute names

**Returns:** List of all items in the table (with automatic pagination handling)

**Example:**

```python
all_items = AWSManager.scan_dynamodb('Products')
print(f"Total items: {len(all_items)}")
```

#### `batch_write_dynamodb(table_name, items)`

Batch writes items to a DynamoDB table (up to 25 items per batch).

**Parameters:**

- `table_name` (str): Name of the DynamoDB table
- `items` (list): List of items to insert (automatically batched in groups of 25)

**Returns:** Tuple of (status_code, message)

**Example:**

```python
items = [
    {'productId': 'P124', 'category': 'Electronics', 'name': 'Phone'},
    {'productId': 'P125', 'category': 'Electronics', 'name': 'Tablet'},
    {'productId': 'P126', 'category': 'Books', 'name': 'Novel'}
]
AWSManager.batch_write_dynamodb('Products', items)
```

#### `list_dynamodb_tables()`

Lists all DynamoDB tables in the account with details.

**Example:**

```python
AWSManager.list_dynamodb_tables()
# Output:
# 📋 DynamoDB Tables in account [3]:
#  - Products
#    Status: ACTIVE
#    Item Count: 150
#    Size: 24576 bytes
#    Billing Mode: PAY_PER_REQUEST
```

#### `delete_dynamodb_table(table_name)`

Deletes a DynamoDB table.

**Parameters:**

- `table_name` (str): Name of the DynamoDB table to delete

**Returns:** Tuple of (status_code, message)

**Example:**

```python
AWSManager.delete_dynamodb_table('Products')
```

### 💻 Local DynamoDB Operations

All DynamoDB operations have corresponding `_local` methods that connect to a local DynamoDB instance running on `localhost:8000`. This is perfect for development and testing.

#### Setting Up Local DynamoDB

**Using Docker:**

```bash
docker run -p 8000:8000 amazon/dynamodb-local
```

**Or download and run locally:**

```bash
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
```

#### `scan_dynamodb_local(table_name, filter_expression=None, expression_attribute_values=None, expression_attribute_names=None)`

Scans a DynamoDB table on localhost:8000.

**Example:**

```python
# Scan local employee table
employees = AWSManager.scan_dynamodb_local('employee')
print(f"Found {len(employees)} employees")
for emp in employees:
    print(emp)
```

#### `list_dynamodb_tables_local()`

Lists all DynamoDB tables on localhost:8000.

**Example:**

```python
AWSManager.list_dynamodb_tables_local()
```

#### `get_item_dynamodb_local(table_name, key)`

Retrieves an item from a local DynamoDB table by key.

**Example:**

```python
item = AWSManager.get_item_dynamodb_local('employee', {'id': '123'})
print(item)
```

#### `query_dynamodb_local(table_name, key_condition_expression, ...)`

Queries a local DynamoDB table with key condition.

**Example:**

```python
from boto3.dynamodb.conditions import Key

results = AWSManager.query_dynamodb_local(
    table_name='employee',
    key_condition_expression=Key('department').eq('Engineering')
)
```

### 🔧 DynamoDB Scripts

#### Scanning Local Tables

Scan and display the employee table:

```bash
python dynamodb_scan.py
```

This script will:
1. List all tables in your local DynamoDB instance
2. Scan the `employee` table
3. Display all employee records in a formatted output

#### Setting Up Test Data

Create a test employee table with sample data:

```bash
python dynamodb_local_setup.py
```

This will create an `employee` table with 6 sample employee records for testing.

#### Migrating to AWS

Migrate a local DynamoDB table to AWS:

```bash
# Migrate with same name
python dynamodb_migrate.py employee

# Migrate with different name
python dynamodb_migrate.py employee employee-prod
```

The migration script will:
1. Verify the source table exists locally
2. Read the table schema
3. Create the table on AWS with the same schema
4. Copy all data from local to AWS
5. Provide a summary of the migration

**Example Output:**

```
Listing all tables in local DynamoDB:
----------------------------------------------------------------------
📋 DynamoDB Tables in account [1]:
 - employee
   Status: ACTIVE
   Item Count: 5
   Size: 512 bytes
   Billing Mode: PAY_PER_REQUEST

======================================================================
Scanning Employee Table from Local DynamoDB (localhost:8000)
======================================================================

✅ Found 5 employee(s):

----------------------------------------------------------------------

Employee #1:
----------------------------------------
  department          : Engineering
  id                  : 123
  name                : John Doe
  salary              : 85000

...

======================================================================
Total Employees: 5
======================================================================
```

### 🚀 DynamoDB Migration Methods

#### `get_table_schema(table_name, use_local=False)`

Retrieves the schema information for a DynamoDB table.

**Parameters:**

- `table_name` (str): Name of the DynamoDB table
- `use_local` (bool): If True, gets schema from localhost:8000

**Returns:** Dictionary containing table schema (key schema, attribute definitions, billing mode, indexes)

**Example:**

```python
# Get schema from local table
schema = AWSManager.get_table_schema('employee', use_local=True)
print(schema['key_schema'])
print(schema['billing_mode'])
```

#### `copy_table_to_aws(source_table_name, destination_table_name=None)`

Copies a complete table from local DynamoDB to AWS DynamoDB.

**Parameters:**

- `source_table_name` (str): Name of the source table (from local DynamoDB)
- `destination_table_name` (str, optional): Name for the destination table on AWS (defaults to source name)

**Returns:** Tuple of (status_code, message)

**Example:**

```python
# Migrate employee table to AWS
status, message = AWSManager.copy_table_to_aws('employee', 'employee-prod')
print(message)
# Output: ✅ TABLE employee-prod CREATED AND 6 ITEMS MIGRATED
```

**Migration Process:**

1. Reads table schema from local DynamoDB
2. Creates new table on AWS with same schema
3. Scans all items from local table
4. Batch writes all items to AWS table
5. Uses `PAY_PER_REQUEST` billing mode for new AWS tables

**📖 For a complete workflow guide, see [DYNAMODB_WORKFLOW.md](DYNAMODB_WORKFLOW.md)**

This comprehensive guide covers:
- Setting up local DynamoDB for development
- Creating and managing test data
- Complete migration workflow from local to AWS
- Best practices and troubleshooting
- Common operations and examples

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
├── dynamodb_scan.py           # Script to scan local DynamoDB employee table
├── dynamodb_migrate.py        # Script to migrate local tables to AWS
├── dynamodb_local_setup.py    # Script to create test data in local DynamoDB
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
- Use batch operations for S3 deletions and DynamoDB writes
- Right-size Lambda memory allocations based on workload
- Keep Lambda packages under 50MB for direct upload
- Use local DynamoDB for development to avoid AWS API calls and costs

### 💰 Cost Optimization

- Use `t2.micro` instances for development/testing
- Enable S3 bucket versioning only when needed
- Set appropriate Lambda timeout values
- Clean up unused EC2 instances and S3 buckets
- Use local DynamoDB for development/testing to avoid AWS costs
- Use `PAY_PER_REQUEST` billing mode for DynamoDB tables with unpredictable traffic

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
