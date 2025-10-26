# DynamoDB Development and Deployment Workflow

This guide covers the complete workflow for developing and testing with local DynamoDB, then deploying to AWS.

## 📋 Table of Contents

1. [Setup](#setup)
2. [Local Development](#local-development)
3. [Migration to AWS](#migration-to-aws)
4. [Best Practices](#best-practices)

---

## Setup

### Prerequisites

- Python 3.7+
- Docker (for local DynamoDB) or DynamoDB Local JAR
- AWS credentials configured

### 1. Start Local DynamoDB

**Option A: Using Docker (Recommended)**

```bash
docker run -p 8000:8000 amazon/dynamodb-local
```

**Option B: Using Downloaded JAR**

```bash
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
```

### 2. Configure AWS Credentials

Create a `.env` file:

```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
```

For local DynamoDB, even dummy credentials work:

```bash
AWS_ACCESS_KEY_ID=fakekey
AWS_SECRET_ACCESS_KEY=fakesecret
AWS_DEFAULT_REGION=us-east-1
```

---

## Local Development

### Step 1: Create Test Data

Use the setup script to create a test table with sample data:

```bash
python dynamodb_local_setup.py
```

This creates an `employee` table with 6 sample records.

**Output:**
```
======================================================================
Setting Up Test DynamoDB Table on Local Instance
======================================================================

🛠️  Step 1: Creating 'employee' table...
   ✅ Table 'employee' created successfully

📝 Step 2: Adding sample employee data...
   ✅ Added 6 employee records

🔍 Step 3: Verifying data...
   ✅ Verified 6 records in table

======================================================================
Setup Complete!
======================================================================
```

### Step 2: View Your Data

Scan and display the table contents:

```bash
python dynamodb_scan.py
```

### Step 3: Work with Data Programmatically

```python
from aws_manager import AWSManager

# List all local tables
AWSManager.list_dynamodb_tables_local()

# Scan all employees
employees = AWSManager.scan_dynamodb_local('employee')
for emp in employees:
    print(f"{emp['name']} - {emp['department']}")

# Get specific employee
employee = AWSManager.get_item_dynamodb_local('employee', {'id': 'EMP001'})
print(employee)

# Query by department (if you have a GSI)
from boto3.dynamodb.conditions import Key
eng_employees = AWSManager.query_dynamodb_local(
    table_name='employee',
    key_condition_expression=Key('department').eq('Engineering')
)
```

### Step 4: Modify Data

```python
from aws_manager import AWSManager
from resources.aws import Aws

# Connect to local DynamoDB
aws = Aws(use_local_dynamodb=True)

# Add new employee
new_employee = {
    'id': 'EMP007',
    'name': 'Alice Anderson',
    'department': 'Engineering',
    'position': 'Software Engineer',
    'salary': 88000,
    'email': 'alice.anderson@company.com',
    'hire_date': '2023-02-15'
}
aws.put_item_dynamodb('employee', new_employee)

# Update existing employee
aws.update_item_dynamodb(
    table_name='employee',
    key={'id': 'EMP001'},
    update_expression='SET salary = :s, position = :p',
    expression_attribute_values={
        ':s': 100000,
        ':p': 'Principal Engineer'
    }
)

# Delete employee
aws.delete_item_dynamodb('employee', {'id': 'EMP007'})
```

---

## Migration to AWS

### Step 1: Verify Local Data

Before migrating, verify your local data is ready:

```bash
python dynamodb_scan.py
```

### Step 2: Migrate Table

Use the migration script to copy your table to AWS:

```bash
# Migrate with same name
python dynamodb_migrate.py employee

# Or migrate with a different name
python dynamodb_migrate.py employee employee-prod
```

**Interactive Process:**
```
================================================================================
DynamoDB Table Migration: Local → AWS
================================================================================

📋 Source Table (Local):      employee
📋 Destination Table (AWS):   employee-prod

⚠️  This will create a new table on AWS. Continue? (yes/no): yes

================================================================================
Starting Migration Process
================================================================================

🔍 Step 1: Verifying source table exists...
   ✅ Found source table 'employee'
   📊 Key Schema: [{'AttributeName': 'id', 'KeyType': 'HASH'}]
   📊 Billing Mode: PAY_PER_REQUEST

🔍 Step 2: Checking data in source table...
   ✅ Found 6 item(s) to migrate

🔍 Step 3: Migrating table to AWS...
🔄 Starting migration of 'employee' to AWS as 'employee-prod'...
🛠️  Creating table 'employee-prod' on AWS...
✅ DynamoDB table 'employee-prod' created successfully
📊 Scanning items from local table 'employee'...
✅ Scan returned 6 item(s) from table 'employee'
🚀 Migrating 6 item(s) to AWS...
✅ Batch write completed: 6 item(s) added to table 'employee-prod'
✅ Migration complete: 6 item(s) copied to 'employee-prod' on AWS

================================================================================
Migration Complete!
================================================================================

✅ TABLE employee-prod CREATED AND 6 ITEMS MIGRATED

📊 Summary:
   • Source: employee (Local DynamoDB)
   • Destination: employee-prod (AWS DynamoDB)
   • Items Migrated: 6

💡 You can now access the table on AWS using:
   AWSManager.scan_dynamodb('employee-prod')
```

### Step 3: Verify AWS Deployment

```python
from aws_manager import AWSManager

# List AWS tables
AWSManager.list_dynamodb_tables()

# Scan the migrated table
aws_employees = AWSManager.scan_dynamodb('employee-prod')
print(f"AWS has {len(aws_employees)} employees")

# Compare with local
local_employees = AWSManager.scan_dynamodb_local('employee')
print(f"Local has {len(local_employees)} employees")
```

### Step 4: Use Programmatic Migration

```python
from aws_manager import AWSManager

# Get schema from local table
schema = AWSManager.get_table_schema('employee', use_local=True)
print(f"Table structure: {schema}")

# Migrate to AWS
status, message = AWSManager.copy_table_to_aws('employee', 'employee-backup')
print(message)
```

---

## Best Practices

### 🔒 Security

1. **Never commit credentials**: Use `.env` files and add them to `.gitignore`
2. **Use IAM roles**: For production, use IAM roles instead of access keys
3. **Least privilege**: Grant only necessary permissions for DynamoDB operations

### 💰 Cost Management

1. **Use local for development**: Save costs by testing locally first
2. **PAY_PER_REQUEST billing**: The migration uses on-demand billing by default
3. **Clean up test tables**: Delete AWS tables after testing to avoid charges
4. **Monitor usage**: Use AWS Cost Explorer to track DynamoDB costs

### ⚡ Performance

1. **Batch operations**: Use `batch_write_dynamodb()` for multiple items
2. **Pagination**: The scan operations automatically handle pagination
3. **Indexes**: Design GSI/LSI in local, test thoroughly before AWS deployment
4. **Partition keys**: Choose partition keys that distribute data evenly

### 🧪 Testing Strategy

```python
# 1. Develop and test locally
from resources.aws import Aws

local_aws = Aws(use_local_dynamodb=True)
# ... test your operations ...

# 2. Migrate to AWS dev environment
from aws_manager import AWSManager
AWSManager.copy_table_to_aws('employee', 'employee-dev')

# 3. Test on AWS dev
prod_aws = Aws(use_local_dynamodb=False)
# ... verify operations work on AWS ...

# 4. When ready, migrate to production
AWSManager.copy_table_to_aws('employee', 'employee-prod')
```

### 📊 Schema Changes

When modifying table structure:

1. **Test locally first**: Create new table structure in local DynamoDB
2. **Verify compatibility**: Ensure your code works with new schema
3. **Plan migration**: Decide between:
   - New table creation (recommended)
   - In-place updates (risky)
4. **Backup before changes**: Always backup production data

### 🔄 Continuous Development

```bash
# Daily workflow
# 1. Start local DynamoDB
docker run -p 8000:8000 amazon/dynamodb-local

# 2. Load/refresh test data
python dynamodb_local_setup.py

# 3. Develop and test
python your_app.py

# 4. Verify changes
python dynamodb_scan.py

# 5. When ready, deploy
python dynamodb_migrate.py employee employee-staging
```

---

## Common Operations

### Create Custom Table

```python
from resources.aws import Aws

aws = Aws(use_local_dynamodb=True)

# Create table with composite key
aws.create_dynamodb_table(
    table_name='orders',
    key_schema=[
        {'AttributeName': 'customer_id', 'KeyType': 'HASH'},
        {'AttributeName': 'order_date', 'KeyType': 'RANGE'}
    ],
    attribute_definitions=[
        {'AttributeName': 'customer_id', 'AttributeType': 'S'},
        {'AttributeName': 'order_date', 'AttributeType': 'S'}
    ],
    billing_mode='PAY_PER_REQUEST'
)
```

### Bulk Data Import

```python
from resources.aws import Aws
import json

aws = Aws(use_local_dynamodb=True)

# Load data from JSON file
with open('data.json', 'r') as f:
    items = json.load(f)

# Batch write (automatically handles 25-item batches)
aws.batch_write_dynamodb('employee', items)
```

### Delete Local Table

```python
from resources.aws import Aws

aws = Aws(use_local_dynamodb=True)
aws.delete_dynamodb_table('old_table')
```

---

## Troubleshooting

### Local DynamoDB Not Running

**Error:** Connection refused to localhost:8000

**Solution:**
```bash
docker run -p 8000:8000 amazon/dynamodb-local
```

### AWS Credentials Not Configured

**Error:** Unable to locate credentials

**Solution:**
```bash
# Set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret

# Or create .env file
echo "AWS_ACCESS_KEY_ID=your_key" > .env
echo "AWS_SECRET_ACCESS_KEY=your_secret" >> .env
```

### Table Already Exists on AWS

**Error:** ResourceInUseException: Table already exists

**Solution:**
- Use a different destination table name
- Or delete the existing AWS table first (careful!)

### Migration Fails Midway

If migration fails after table creation but before data copy:

```python
from aws_manager import AWSManager

# Continue from local data
local_items = AWSManager.scan_dynamodb_local('employee')

# Manual batch write to AWS
from resources.aws import Aws
aws = Aws(use_local_dynamodb=False)
aws.batch_write_dynamodb('employee-prod', local_items)
```

---

## Additional Resources

- [AWS DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [DynamoDB Local Documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)
- [Boto3 DynamoDB Guide](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html)
