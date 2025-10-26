import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from resources.aws import Aws  # type: ignore

"""
from aws_manager import AWSManager
AWSManager.list_functions()
"""

class AWSManager:
    """Manager class with static methods for AWS operations (Lambda, S3, EC2, DynamoDB)."""

    @staticmethod
    def invoke_function(function_name: str, function_params: dict, get_log: bool = False) -> dict:
        """
        Invokes a Lambda function.
        
        Args:
            function_name: Name of the Lambda function to invoke
            function_params: Dictionary of parameters to pa the function
            get_log: Whether to retrieve execution logs
            
        Returns:
            Response dictionary from Lambda invocation
        """
        aws = Aws()
        return aws.invoke_function(function_name, function_params, get_log)

    @staticmethod
    def update_function_code(function_name: str, deployment_package: bytes) -> None:
        """
        Updates Lambda function code with a .zip archive.
        
        Args:
            function_name: Name of the Lambda function to update
            deployment_package: Bytes of the .zip deployment package
        """
        aws = Aws()
        aws.update_function_code(function_name, deployment_package)

    @staticmethod
    def update_function_configuration(function_name: str, env_vars: dict) -> None:
        """
        Updates Lambda function environment variables.
        
        Args:
            function_name: Name of the Lambda function to update
            env_vars: Dictionary of environment variables to set
        """
        aws = Aws()
        return aws.update_function_configuration(function_name, env_vars)

    @staticmethod
    def list_functions() -> None:
        """
        Lists all Lambda functions for the current account.
        Prints function details including name, description, runtime, and handler.
        """
        aws = Aws()
        aws.list_functions()

    @staticmethod
    def create_bucket_name(prefix: str = 'scotton') -> str:
        """
        Create unique bucket name with UUID suffix.
        
        Args:
            prefix: Prefix for the bucket name (default: 'scotton')
            
        Returns:
            Unique bucket name string
        """
        aws = Aws()
        return aws.create_bucket_name(prefix)

    @staticmethod
    def create_bucket(bucket_prefix: str) -> tuple:
        """
        Create S3 bucket with proper region configuration.
        
        Args:
            bucket_prefix: Prefix for the bucket name
            
        Returns:
            Tuple of (bucket_name, bucket_response)
        """
        aws = Aws()
        return aws.create_bucket(bucket_prefix)

    @staticmethod
    def list_buckets() -> None:
        """
        List all S3 buckets in account.
        Prints bucket names.
        """
        aws = Aws()
        aws.list_buckets()

    @staticmethod
    def list_bucket_objects(bucket_name: str) -> None:
        """
        List objects in S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
        """
        aws = Aws()
        aws.list_bucket_objects(bucket_name)

    @staticmethod
    def add_file_to_bucket(bucket_name: str, file_name: str, object_name: str, url: str = None) -> tuple: # type: ignore
        """
        Upload file to S3 bucket from local path or URL.
        
        Args:
            bucket_name: Name of the S3 bucket
            file_name: Name of the file to upload
            object_name: Name for the object in S3
            url: Optional URL to download file from
            
        Returns:
            Tuple of (status_code, message)
        """
        aws = Aws()
        return aws.add_file_to_bucket(bucket_name, file_name, object_name, url)

    @staticmethod
    def copy_to_bucket(from_bucket: str, to_bucket: str, file_name: str) -> str:
        """
        Copy S3 object between buckets.
        
        Args:
            from_bucket: Source bucket name
            to_bucket: Destination bucket name
            file_name: Name of the file to copy
            
        Returns:
            Success message string
        """
        aws = Aws()
        return aws.copy_to_bucket(from_bucket, to_bucket, file_name)

    @staticmethod
    def delete_files_from_bucket(bucket_name: str, file_list: list) -> tuple:
        """
        Delete multiple files from S3 bucket efficiently.
        
        Args:
            bucket_name: Name of the S3 bucket
            file_list: List of file keys to delete
            
        Returns:
            Tuple of (status_code, message)
        """
        aws = Aws()
        return aws.delete_files_from_bucket(bucket_name, file_list)

    @staticmethod
    def enable_bucket_versioning(bucket_name: str) -> str:
        """
        Enable versioning for S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket
            
        Returns:
            Success message with versioning status
        """
        aws = Aws()
        return aws.enable_bucket_versioning(bucket_name)

    @staticmethod
    def create_ec2(image_id: str, instance_type: str = 't2.micro', min_count: int = 1, max_count: int = 1, key_name: str = None, security_group_ids: list = None, subnet_id: str = None, tags: list = None) -> tuple: # type: ignore
        """
        Create EC2 instance(s) with specified configuration.
        
        Args:
            image_id: AMI ID to use for the instance
            instance_type: EC2 instance type (default: 't2.micro')
            min_count: Minimum number of instances to launch (default: 1)
            max_count: Maximum number of instances to launch (default: 1)
            key_name: Name of the key pair for SSH access
            security_group_ids: List of security group IDs
            subnet_id: Subnet ID for the instance
            tags: List of tags to apply to the instance
            
        Returns:
            Tuple of (status_code, list of instance IDs)
        """
        aws = Aws()
        return aws.create_ec2(image_id, instance_type, min_count, max_count, key_name, security_group_ids, subnet_id, tags)

    @staticmethod
    def start_ec2(instance_ids: list) -> tuple:
        """
        Start one or more EC2 instances.
        
        Args:
            instance_ids: List of EC2 instance IDs to start
            
        Returns:
            Tuple of (status_code, response)
        """
        aws = Aws()
        return aws.start_ec2(instance_ids)

    @staticmethod
    def stop_ec2(instance_ids: list) -> tuple:
        """
        Stop one or more EC2 instances.
        
        Args:
            instance_ids: List of EC2 instance IDs to stop
            
        Returns:
            Tuple of (status_code, response)
        """
        aws = Aws()
        return aws.stop_ec2(instance_ids)

    @staticmethod
    def list_ec2s() -> None:
        """
        List all EC2 instances in account.
        Prints instance details including ID, state, type, and IP addresses.
        """
        aws = Aws()
        aws.list_ec2s()

    @staticmethod
    def remove_ec2s(instance_ids: list) -> tuple:
        """
        Terminate one or more EC2 instances.
        
        Args:
            instance_ids: List of EC2 instance IDs to terminate
            
        Returns:
            Tuple of (status_code, response)
        """
        aws = Aws()
        return aws.remove_ec2s(instance_ids)

    # DynamoDB Operations
    @staticmethod
    def create_dynamodb_table(table_name: str, key_schema: list, attribute_definitions: list,
                             provisioned_throughput: dict = None, billing_mode: str = 'PAY_PER_REQUEST', # type: ignore
                             global_secondary_indexes: list = None, local_secondary_indexes: list = None, # type: ignore
                             tags: list = None) -> tuple: # type: ignore
        """
        Create DynamoDB table with specified configuration.
        
        Args:
            table_name: Name of the DynamoDB table
            key_schema: List defining partition key and sort key
            attribute_definitions: List of attribute definitions
            provisioned_throughput: Dict with ReadCapacityUnits and WriteCapacityUnits (only for PROVISIONED mode)
            billing_mode: 'PAY_PER_REQUEST' or 'PROVISIONED' (default: 'PAY_PER_REQUEST')
            global_secondary_indexes: List of global secondary indexes
            local_secondary_indexes: List of local secondary indexes
            tags: List of tags to apply to the table
            
        Returns:
            Tuple of (status_code, table)
        """
        aws = Aws()
        return aws.create_dynamodb_table(table_name, key_schema, attribute_definitions,
                                        provisioned_throughput, billing_mode,
                                        global_secondary_indexes, local_secondary_indexes, tags)

    @staticmethod
    def put_item_dynamodb(table_name: str, item: dict) -> tuple:
        """
        Insert or update item in DynamoDB table.
        
        Args:
            table_name: Name of the DynamoDB table
            item: Dictionary representing the item to insert/update
            
        Returns:
            Tuple of (status_code, response)
        """
        aws = Aws()
        return aws.put_item_dynamodb(table_name, item)

    @staticmethod
    def get_item_dynamodb(table_name: str, key: dict) -> dict:
        """
        Retrieve item from DynamoDB table by key.
        
        Args:
            table_name: Name of the DynamoDB table
            key: Dictionary representing the primary key of the item
            
        Returns:
            Dictionary containing the item, or empty dict if not found
        """
        aws = Aws()
        return aws.get_item_dynamodb(table_name, key)

    @staticmethod
    def update_item_dynamodb(table_name: str, key: dict, update_expression: str,
                            expression_attribute_values: dict = None, # type: ignore
                            expression_attribute_names: dict = None, # type: ignore
                            return_values: str = 'ALL_NEW') -> tuple:
        """
        Update item in DynamoDB table.
        
        Args:
            table_name: Name of the DynamoDB table
            key: Dictionary representing the primary key of the item
            update_expression: Expression defining the update (e.g., 'SET #n = :val')
            expression_attribute_values: Dictionary mapping expression values
            expression_attribute_names: Dictionary mapping expression attribute names
            return_values: What to return after update (default: 'ALL_NEW')
            
        Returns:
            Tuple of (status_code, response)
        """
        aws = Aws()
        return aws.update_item_dynamodb(table_name, key, update_expression,
                                       expression_attribute_values,
                                       expression_attribute_names, return_values)

    @staticmethod
    def delete_item_dynamodb(table_name: str, key: dict) -> tuple:
        """
        Delete item from DynamoDB table.
        
        Args:
            table_name: Name of the DynamoDB table
            key: Dictionary representing the primary key of the item
            
        Returns:
            Tuple of (status_code, response)
        """
        aws = Aws()
        return aws.delete_item_dynamodb(table_name, key)

    @staticmethod
    def query_dynamodb(table_name: str, key_condition_expression: str,
                      expression_attribute_values: dict = None, # type: ignore
                      expression_attribute_names: dict = None, # type: ignore
                      filter_expression: str = None, # type: ignore
                      index_name: str = None) -> list: # type: ignore
        """
        Query DynamoDB table with key condition.
        
        Args:
            table_name: Name of the DynamoDB table
            key_condition_expression: Key condition for the query
            expression_attribute_values: Dictionary mapping expression values
            expression_attribute_names: Dictionary mapping expression attribute names
            filter_expression: Optional filter expression
            index_name: Optional index name to query against
            
        Returns:
            List of items matching the query
        """
        aws = Aws()
        return aws.query_dynamodb(table_name, key_condition_expression,
                                 expression_attribute_values,
                                 expression_attribute_names,
                                 filter_expression, index_name)

    @staticmethod
    def scan_dynamodb(table_name: str, filter_expression: str = None, # type: ignore
                     expression_attribute_values: dict = None, # type: ignore
                     expression_attribute_names: dict = None) -> list: # type: ignore
        """
        Scan DynamoDB table (reads all items).
        
        Args:
            table_name: Name of the DynamoDB table
            filter_expression: Optional filter expression
            expression_attribute_values: Dictionary mapping expression values
            expression_attribute_names: Dictionary mapping expression attribute names
            
        Returns:
            List of all items in the table (with pagination handling)
        """
        aws = Aws()
        return aws.scan_dynamodb(table_name, filter_expression,
                                expression_attribute_values,
                                expression_attribute_names)

    @staticmethod
    def batch_write_dynamodb(table_name: str, items: list) -> tuple:
        """
        Batch write items to DynamoDB table (up to 25 items per batch).
        
        Args:
            table_name: Name of the DynamoDB table
            items: List of items to insert (automatically batched in groups of 25)
            
        Returns:
            Tuple of (status_code, message)
        """
        aws = Aws()
        return aws.batch_write_dynamodb(table_name, items)

    @staticmethod
    def list_dynamodb_tables() -> None:
        """
        List all DynamoDB tables in account.
        Prints table details including status, item count, size, and billing mode.
        """
        aws = Aws()
        aws.list_dynamodb_tables()

    @staticmethod
    def delete_dynamodb_table(table_name: str) -> tuple:
        """
        Delete DynamoDB table.
        
        Args:
            table_name: Name of the DynamoDB table to delete
            
        Returns:
            Tuple of (status_code, message)
        """
        aws = Aws()
        return aws.delete_dynamodb_table(table_name)

    # Local DynamoDB Operations
    @staticmethod
    def scan_dynamodb_local(table_name: str, filter_expression: str = None, # type: ignore
                           expression_attribute_values: dict = None, # type: ignore
                           expression_attribute_names: dict = None) -> list: # type: ignore
        """
        Scan DynamoDB table on localhost:8000 (reads all items).
        
        Args:
            table_name: Name of the DynamoDB table
            filter_expression: Optional filter expression
            expression_attribute_values: Dictionary mapping expression values
            expression_attribute_names: Dictionary mapping expression attribute names
            
        Returns:
            List of all items in the table (with automatic pagination handling)
        """
        aws = Aws(use_local_dynamodb=True)
        return aws.scan_dynamodb(table_name, filter_expression,
                                expression_attribute_values,
                                expression_attribute_names)

    @staticmethod
    def list_dynamodb_tables_local() -> None:
        """
        List all DynamoDB tables on localhost:8000.
        Prints table details including status, item count, size, and billing mode.
        """
        aws = Aws(use_local_dynamodb=True)
        aws.list_dynamodb_tables()

    @staticmethod
    def get_item_dynamodb_local(table_name: str, key: dict) -> dict:
        """
        Retrieve item from DynamoDB table on localhost:8000 by key.
        
        Args:
            table_name: Name of the DynamoDB table
            key: Dictionary representing the primary key of the item
            
        Returns:
            Dictionary containing the item, or empty dict if not found
        """
        aws = Aws(use_local_dynamodb=True)
        return aws.get_item_dynamodb(table_name, key)

    @staticmethod
    def query_dynamodb_local(table_name: str, key_condition_expression: str,
                            expression_attribute_values: dict = None, # type: ignore
                            expression_attribute_names: dict = None, # type: ignore
                            filter_expression: str = None, # type: ignore
                            index_name: str = None) -> list: # type: ignore
        """
        Query DynamoDB table on localhost:8000 with key condition.
        
        Args:
            table_name: Name of the DynamoDB table
            key_condition_expression: Key condition for the query
            expression_attribute_values: Dictionary mapping expression values
            expression_attribute_names: Dictionary mapping expression attribute names
            filter_expression: Optional filter expression
            index_name: Optional index name to query against
            
        Returns:
            List of items matching the query
        """
        aws = Aws(use_local_dynamodb=True)
        return aws.query_dynamodb(table_name, key_condition_expression,
                                 expression_attribute_values,
                                 expression_attribute_names,
                                 filter_expression, index_name)

    # DynamoDB Migration Operations
    @staticmethod
    def get_table_schema(table_name: str, use_local: bool = False) -> dict:
        """
        Get table schema information (key schema and attribute definitions).
        
        Args:
            table_name: Name of the DynamoDB table
            use_local: If True, gets schema from localhost:8000
            
        Returns:
            Dictionary containing table schema information
        """
        aws = Aws(use_local_dynamodb=use_local)
        return aws.get_table_schema(table_name)

    @staticmethod
    def copy_table_to_aws(source_table_name: str, destination_table_name: str = None) -> tuple: # type: ignore
        """
        Copy a table from local DynamoDB to AWS DynamoDB.
        
        This will:
        1. Read the table schema from local DynamoDB
        2. Create a new table on AWS with the same schema
        3. Scan all items from the local table
        4. Batch write all items to the AWS table
        
        Args:
            source_table_name: Name of the source table (from local DynamoDB)
            destination_table_name: Name for the destination table on AWS (defaults to source name)
            
        Returns:
            Tuple of (status_code, message)
        """
        aws = Aws(use_local_dynamodb=False)  # Deploy to AWS
        return aws.copy_table_to_aws(source_table_name, destination_table_name)



if __name__ == "__main__":
    AWSManager.list_functions()
        

