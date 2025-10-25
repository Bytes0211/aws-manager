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
    """Manager class with static methods for AWS Lambda operations."""

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



if __name__ == "__main__":
    AWSManager.list_functions()
        

