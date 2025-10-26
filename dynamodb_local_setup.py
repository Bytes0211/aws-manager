#!/usr/bin/env python3
"""
Script to create a test DynamoDB table on local instance with sample data.

Prerequisites:
1. Local DynamoDB must be running on localhost:8000

Usage:
    python dynamodb_local_setup.py

This will create an 'employee' table with sample employee data for testing.
"""

import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from aws_manager import AWSManager
from resources.aws import Aws


def create_test_employee_table():
    """Create a test employee table in local DynamoDB with sample data."""
    
    print("=" * 70)
    print("Setting Up Test DynamoDB Table on Local Instance")
    print("=" * 70)
    print()
    
    # Initialize local AWS client
    aws = Aws(use_local_dynamodb=True)
    
    try:
        # Step 1: Create the table
        print("🛠️  Step 1: Creating 'employee' table...")
        
        table_name = 'employee'
        key_schema = [
            {'AttributeName': 'id', 'KeyType': 'HASH'},  # Partition key
        ]
        attribute_definitions = [
            {'AttributeName': 'id', 'AttributeType': 'S'},  # String
        ]
        
        try:
            aws.create_dynamodb_table(
                table_name=table_name,
                key_schema=key_schema,
                attribute_definitions=attribute_definitions,
                billing_mode='PAY_PER_REQUEST'
            )
            print(f"   ✅ Table '{table_name}' created successfully")
        except Exception as e:
            if 'ResourceInUseException' in str(e) or 'Table already exists' in str(e):
                print(f"   ⚠️  Table '{table_name}' already exists, skipping creation")
            else:
                raise
        
        print()
        
        # Step 2: Add sample data
        print("📝 Step 2: Adding sample employee data...")
        
        employees = [
            {
                'id': 'EMP001',
                'name': 'John Doe',
                'department': 'Engineering',
                'position': 'Senior Software Engineer',
                'salary': 95000,
                'email': 'john.doe@company.com',
                'hire_date': '2020-03-15'
            },
            {
                'id': 'EMP002',
                'name': 'Jane Smith',
                'department': 'Engineering',
                'position': 'Lead Developer',
                'salary': 110000,
                'email': 'jane.smith@company.com',
                'hire_date': '2019-06-01'
            },
            {
                'id': 'EMP003',
                'name': 'Michael Johnson',
                'department': 'Marketing',
                'position': 'Marketing Manager',
                'salary': 85000,
                'email': 'michael.johnson@company.com',
                'hire_date': '2021-01-10'
            },
            {
                'id': 'EMP004',
                'name': 'Emily Davis',
                'department': 'Engineering',
                'position': 'DevOps Engineer',
                'salary': 92000,
                'email': 'emily.davis@company.com',
                'hire_date': '2020-09-20'
            },
            {
                'id': 'EMP005',
                'name': 'Robert Wilson',
                'department': 'Sales',
                'position': 'Sales Director',
                'salary': 105000,
                'email': 'robert.wilson@company.com',
                'hire_date': '2018-11-05'
            },
            {
                'id': 'EMP006',
                'name': 'Sarah Brown',
                'department': 'HR',
                'position': 'HR Manager',
                'salary': 78000,
                'email': 'sarah.brown@company.com',
                'hire_date': '2021-04-12'
            }
        ]
        
        # Batch write employees
        aws.batch_write_dynamodb(table_name, employees)
        print(f"   ✅ Added {len(employees)} employee records")
        
        print()
        
        # Step 3: Verify data
        print("🔍 Step 3: Verifying data...")
        items = aws.scan_dynamodb(table_name)
        print(f"   ✅ Verified {len(items)} records in table")
        
        print()
        print("=" * 70)
        print("Setup Complete!")
        print("=" * 70)
        print()
        print("✅ Successfully created test employee table with sample data")
        print()
        print("📊 Summary:")
        print(f"   • Table Name: {table_name}")
        print(f"   • Total Records: {len(items)}")
        print(f"   • Departments: Engineering, Marketing, Sales, HR")
        print()
        print("💡 Next Steps:")
        print("   1. View data:")
        print("      python dynamodb_scan.py")
        print()
        print("   2. Migrate to AWS:")
        print("      python dynamodb_migrate.py employee")
        print()
        print("   3. Query programmatically:")
        print("      from aws_manager import AWSManager")
        print("      employees = AWSManager.scan_dynamodb_local('employee')")
        print()
        
    except Exception as e:
        print()
        print("=" * 70)
        print("Setup Failed")
        print("=" * 70)
        print(f"\n❌ Error: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure local DynamoDB is running on localhost:8000")
        print("   2. Start local DynamoDB with:")
        print("      docker run -p 8000:8000 amazon/dynamodb-local")
        print("   3. Verify you have AWS credentials configured (even dummy values work)")
        sys.exit(1)


if __name__ == "__main__":
    create_test_employee_table()
