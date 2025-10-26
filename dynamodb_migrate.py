#!/usr/bin/env python3
"""
Script to migrate DynamoDB tables from local instance to AWS.

Prerequisites:
1. Local DynamoDB must be running on localhost:8000 with data
2. AWS credentials must be configured for deployment
3. Source table must exist in local DynamoDB

Usage:
    python dynamodb_migrate.py <table_name> [destination_name]
    
Examples:
    # Migrate employee table with same name
    python dynamodb_migrate.py employee
    
    # Migrate employee table with different name
    python dynamodb_migrate.py employee employee-prod
"""

import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from aws_manager import AWSManager


def migrate_table(source_table: str, destination_table: str = None):
    """Migrate a table from local DynamoDB to AWS."""
    
    if destination_table is None:
        destination_table = source_table
    
    print("=" * 80)
    print("DynamoDB Table Migration: Local → AWS")
    print("=" * 80)
    print(f"\n📋 Source Table (Local):      {source_table}")
    print(f"📋 Destination Table (AWS):   {destination_table}")
    print()
    
    # Confirm migration
    response = input("⚠️  This will create a new table on AWS. Continue? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("\n❌ Migration cancelled by user.")
        sys.exit(0)
    
    print("\n" + "=" * 80)
    print("Starting Migration Process")
    print("=" * 80)
    print()
    
    try:
        # Step 1: Check source table exists
        print("🔍 Step 1: Verifying source table exists...")
        try:
            schema = AWSManager.get_table_schema(source_table, use_local=True)
            print(f"   ✅ Found source table '{source_table}'")
            print(f"   📊 Key Schema: {schema['key_schema']}")
            print(f"   📊 Billing Mode: {schema['billing_mode']}")
        except Exception as e:
            print(f"   ❌ Source table '{source_table}' not found in local DynamoDB")
            print(f"   Error: {str(e)}")
            print("\n💡 Tip: Ensure local DynamoDB is running on localhost:8000")
            sys.exit(1)
        
        print()
        
        # Step 2: Get item count
        print("🔍 Step 2: Checking data in source table...")
        items = AWSManager.scan_dynamodb_local(source_table)
        print(f"   ✅ Found {len(items)} item(s) to migrate")
        print()
        
        # Step 3: Perform migration
        print("🔍 Step 3: Migrating table to AWS...")
        status_code, message = AWSManager.copy_table_to_aws(source_table, destination_table)
        
        print()
        print("=" * 80)
        print("Migration Complete!")
        print("=" * 80)
        print(f"\n✅ {message}")
        print(f"\n📊 Summary:")
        print(f"   • Source: {source_table} (Local DynamoDB)")
        print(f"   • Destination: {destination_table} (AWS DynamoDB)")
        print(f"   • Items Migrated: {len(items)}")
        print()
        print("💡 You can now access the table on AWS using:")
        print(f"   AWSManager.scan_dynamodb('{destination_table}')")
        print()
        
    except Exception as e:
        print()
        print("=" * 80)
        print("Migration Failed")
        print("=" * 80)
        print(f"\n❌ Error: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure local DynamoDB is running on localhost:8000")
        print("   2. Verify AWS credentials are configured correctly")
        print("   3. Check that you have permissions to create DynamoDB tables on AWS")
        print("   4. Ensure the destination table doesn't already exist on AWS")
        sys.exit(1)


def show_local_tables():
    """Display all tables in local DynamoDB."""
    print("\n📋 Tables in Local DynamoDB:")
    print("-" * 80)
    try:
        AWSManager.list_dynamodb_tables_local()
    except Exception as e:
        print(f"❌ Error listing local tables: {str(e)}")
        print("💡 Ensure local DynamoDB is running on localhost:8000")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dynamodb_migrate.py <source_table> [destination_table]")
        print("\nExamples:")
        print("  python dynamodb_migrate.py employee")
        print("  python dynamodb_migrate.py employee employee-prod")
        print()
        show_local_tables()
        sys.exit(1)
    
    source = sys.argv[1]
    destination = sys.argv[2] if len(sys.argv) > 2 else None
    
    migrate_table(source, destination)
