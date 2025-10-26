#!/usr/bin/env python3
"""
Script to scan the employee table from local DynamoDB instance.

Prerequisites:
1. Local DynamoDB must be running on localhost:8000
2. Employee table must exist in the local DynamoDB

To run local DynamoDB:
    docker run -p 8000:8000 amazon/dynamodb-local
    
    OR
    
    java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
"""

import sys
import os
import json

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from aws_manager import AWSManager


def scan_employee_table():
    """Scan and display all employees from the local DynamoDB employee table."""
    
    print("=" * 70)
    print("Scanning Employee Table from Local DynamoDB (localhost:8000)")
    print("=" * 70)
    print()
    
    try:
        # Scan the employee table
        employees = AWSManager.scan_dynamodb_local('employee')
        
        if not employees:
            print("⚠️  No employees found in the table.")
            return
        
        # Display results
        print(f"✅ Found {len(employees)} employee(s):\n")
        print("-" * 70)
        
        for idx, emp in enumerate(employees, 1):
            print(f"\nEmployee #{idx}:")
            print("-" * 40)
            
            # Pretty print each employee's data
            for key, value in sorted(emp.items()):
                print(f"  {key:20s}: {value}")
        
        print("\n" + "=" * 70)
        print(f"Total Employees: {len(employees)}")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error scanning employee table: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Ensure local DynamoDB is running on localhost:8000")
        print("2. Verify the 'employee' table exists")
        print("3. Check AWS credentials are configured (even dummy values work for local)")
        print("\nTo start local DynamoDB:")
        print("   docker run -p 8000:8000 amazon/dynamodb-local")
        sys.exit(1)


def list_local_tables():
    """List all tables in the local DynamoDB instance."""
    print("\nListing all tables in local DynamoDB:")
    print("-" * 70)
    try:
        AWSManager.list_dynamodb_tables_local()
    except Exception as e:
        print(f"❌ Error listing tables: {str(e)}")


if __name__ == "__main__":
    # First, list all tables
    list_local_tables()
    print()
    
    # Then scan the employee table
    scan_employee_table()
