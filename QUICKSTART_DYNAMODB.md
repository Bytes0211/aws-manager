# DynamoDB Quick Start Guide

Get up and running with local DynamoDB development and AWS deployment in 5 minutes.

## 🚀 Quick Start (5 Steps)

### Step 1: Start Local DynamoDB

```bash
docker run -p 8000:8000 amazon/dynamodb-local
```

### Step 2: Create Test Data

```bash
python dynamodb_local_setup.py
```

This creates an `employee` table with 6 sample records.

### Step 3: View Your Data

```bash
python dynamodb_scan.py
```

### Step 4: Develop Your Application

```python
from aws_manager import AWSManager

# Query local DynamoDB
employees = AWSManager.scan_dynamodb_local('employee')
for emp in employees:
    print(f"{emp['name']} works in {emp['department']}")
```

### Step 5: Deploy to AWS

```bash
python dynamodb_migrate.py employee employee-prod
```

✅ Done! Your table is now on AWS.

---

## 📝 Common Tasks

### Add New Employee

```python
from resources.aws import Aws

aws = Aws(use_local_dynamodb=True)
aws.put_item_dynamodb('employee', {
    'id': 'EMP007',
    'name': 'Your Name',
    'department': 'Engineering',
    'position': 'Developer',
    'salary': 90000,
    'email': 'your.name@company.com',
    'hire_date': '2024-01-15'
})
```

### Query Employees

```python
from aws_manager import AWSManager

# Get all employees
all_employees = AWSManager.scan_dynamodb_local('employee')

# Get specific employee
employee = AWSManager.get_item_dynamodb_local('employee', {'id': 'EMP001'})
print(employee)
```

### Update Employee

```python
from resources.aws import Aws

aws = Aws(use_local_dynamodb=True)
aws.update_item_dynamodb(
    table_name='employee',
    key={'id': 'EMP001'},
    update_expression='SET salary = :s',
    expression_attribute_values={':s': 105000}
)
```

### Delete Employee

```python
from resources.aws import Aws

aws = Aws(use_local_dynamodb=True)
aws.delete_item_dynamodb('employee', {'id': 'EMP007'})
```

---

## 🔄 Development Workflow

```bash
# 1. Start local DynamoDB (once per session)
docker run -p 8000:8000 amazon/dynamodb-local

# 2. Create/refresh test data (as needed)
python dynamodb_local_setup.py

# 3. Develop and test locally
python your_app.py

# 4. Check your data
python dynamodb_scan.py

# 5. Deploy to AWS (when ready)
python dynamodb_migrate.py employee employee-staging
```

---

## 🎯 Key Methods

### Local Operations (append `_local`)

```python
from aws_manager import AWSManager

# List tables
AWSManager.list_dynamodb_tables_local()

# Scan table
items = AWSManager.scan_dynamodb_local('employee')

# Get item
item = AWSManager.get_item_dynamodb_local('employee', {'id': 'EMP001'})

# Query table
from boto3.dynamodb.conditions import Key
results = AWSManager.query_dynamodb_local(
    'employee',
    key_condition_expression=Key('id').eq('EMP001')
)
```

### AWS Operations (no suffix)

```python
from aws_manager import AWSManager

# List tables
AWSManager.list_dynamodb_tables()

# Scan table
items = AWSManager.scan_dynamodb('employee-prod')

# Get item
item = AWSManager.get_item_dynamodb('employee-prod', {'id': 'EMP001'})
```

### Migration Operations

```python
from aws_manager import AWSManager

# Get table schema
schema = AWSManager.get_table_schema('employee', use_local=True)

# Migrate to AWS
status, msg = AWSManager.copy_table_to_aws('employee', 'employee-prod')
print(msg)
```

---

## 🛠️ Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `dynamodb_local_setup.py` | Create test data | `python dynamodb_local_setup.py` |
| `dynamodb_scan.py` | View table contents | `python dynamodb_scan.py` |
| `dynamodb_migrate.py` | Deploy to AWS | `python dynamodb_migrate.py <source> [dest]` |

---

## 💡 Tips

1. **Always test locally first** - Free and fast
2. **Use meaningful table names** - `employee-dev`, `employee-prod`
3. **Check data before migration** - Run `dynamodb_scan.py`
4. **Use PAY_PER_REQUEST** - Automatically set during migration
5. **Clean up AWS tables** - Delete test tables to avoid costs

---

## 🐛 Troubleshooting

### Can't connect to local DynamoDB
```bash
# Check if Docker container is running
docker ps | grep dynamodb

# Restart if needed
docker run -p 8000:8000 amazon/dynamodb-local
```

### AWS credentials error
```bash
# Set in .env file
echo "AWS_ACCESS_KEY_ID=your_key" > .env
echo "AWS_SECRET_ACCESS_KEY=your_secret" >> .env
echo "AWS_DEFAULT_REGION=us-east-1" >> .env
```

### Table already exists on AWS
```bash
# Use a different destination name
python dynamodb_migrate.py employee employee-v2
```

---

## 📚 More Information

- **Full Documentation**: [README.md](README.md)
- **Complete Workflow Guide**: [DYNAMODB_WORKFLOW.md](DYNAMODB_WORKFLOW.md)
- **Lambda Deployment**: [aws_lambda_deployment_guide.md](aws_lambda_deployment_guide.md)

---

## 🎓 Example: Complete Application

```python
#!/usr/bin/env python3
"""Example: Employee Management System"""

from aws_manager import AWSManager
from resources.aws import Aws

# Initialize local DynamoDB connection
local_aws = Aws(use_local_dynamodb=True)

# Add employees
employees = [
    {'id': 'EMP001', 'name': 'Alice', 'department': 'Engineering', 'salary': 95000},
    {'id': 'EMP002', 'name': 'Bob', 'department': 'Sales', 'salary': 85000},
    {'id': 'EMP003', 'name': 'Carol', 'department': 'Engineering', 'salary': 92000}
]

print("Adding employees...")
local_aws.batch_write_dynamodb('employee', employees)

# Query all employees
print("\nAll employees:")
all_emps = AWSManager.scan_dynamodb_local('employee')
for emp in all_emps:
    print(f"  {emp['id']}: {emp['name']} - {emp['department']} (${emp['salary']})")

# Update salary
print("\nGiving Alice a raise...")
local_aws.update_item_dynamodb(
    'employee',
    {'id': 'EMP001'},
    'SET salary = :s',
    {':s': 105000}
)

# Verify update
alice = AWSManager.get_item_dynamodb_local('employee', {'id': 'EMP001'})
print(f"Alice's new salary: ${alice['salary']}")

# Deploy to AWS
print("\nDeploying to AWS...")
status, msg = AWSManager.copy_table_to_aws('employee', 'employee-demo')
print(msg)

print("\n✅ Complete! Check AWS console for 'employee-demo' table.")
```

Run it:
```bash
python example.py
```

---

Happy coding! 🎉
