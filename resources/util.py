import os
from dotenv.main import load_dotenv
import boto3 as aws
from functools import lru_cache

# Load environment variables once at module level
load_dotenv()

def clear_env_vars(*var_names):
    """Clear specified environment variables."""
    for var in var_names:
        os.environ.pop(var, None)

def get_env_var(name: str) -> str:
    """Get environment variable by name."""
    return os.environ.get(name)

# Environment variable getters
get_env = lambda: get_env_var('env')
get_appName = lambda: get_env_var('appName')
get_srcDir = lambda: get_env_var('srcDir')
get_srcPattern = lambda: get_env_var('srcPattern')
get_srcFileFormat = lambda: get_env_var('srcFileFormat')

# AWS client factories with caching
# the lru_cache decorator ensures that each client is created only once
@lru_cache(maxsize=1)
def get_s3_client():
    """Get AWS S3 client."""
    return aws.client('s3')

@lru_cache(maxsize=1)
def get_s3_resource():
    """Get AWS S3 resource."""
    return aws.resource('s3')

@lru_cache(maxsize=1)
def get_lambda_client():
    """Get AWS Lambda client."""
    return aws.client('lambda')

@lru_cache(maxsize=1)
def get_iam_client():
    """Get AWS IAM client."""
    return aws.client('iam')

@lru_cache(maxsize=1)
def get_ec2_client():
    """Get AWS EC2 client."""
    return aws.client('ec2')

@lru_cache(maxsize=1)
def get_ec2_resource():
    """Get AWS EC2 resource."""
    return aws.resource('ec2')
