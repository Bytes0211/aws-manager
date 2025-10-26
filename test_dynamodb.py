import pytest
import boto3
from moto import mock_aws
from aws_manager import AWSManager
from resources.aws import Aws


@pytest.fixture
def aws_credentials(monkeypatch):
    """Mock AWS credentials for moto."""
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_REGION", "us-east-1")


@pytest.fixture
def dynamodb_table_config():
    """DynamoDB table configuration for testing."""
    return {
        'table_name': 'test-table',
        'key_schema': [
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        'attribute_definitions': [
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ]
    }


@pytest.fixture
def dynamodb_table_config_with_sort_key():
    """DynamoDB table configuration with sort key for testing."""
    return {
        'table_name': 'test-table-sort',
        'key_schema': [
            {'AttributeName': 'pk', 'KeyType': 'HASH'},
            {'AttributeName': 'sk', 'KeyType': 'RANGE'}
        ],
        'attribute_definitions': [
            {'AttributeName': 'pk', 'AttributeType': 'S'},
            {'AttributeName': 'sk', 'AttributeType': 'S'}
        ]
    }


class TestCreateDynamoDBTable:
    """Test suite for create_dynamodb_table functionality."""
    
    @mock_aws
    def test_create_table_pay_per_request(self, aws_credentials, dynamodb_table_config):
        """Test creating a DynamoDB table with PAY_PER_REQUEST billing mode."""
        status_code, table = AWSManager.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        assert status_code == 200
        assert table.name == dynamodb_table_config['table_name']
        assert table.billing_mode_summary['BillingMode'] == 'PAY_PER_REQUEST'
    
    @mock_aws
    def test_create_table_provisioned(self, aws_credentials, dynamodb_table_config):
        """Test creating a DynamoDB table with PROVISIONED billing mode."""
        provisioned_throughput = {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
        
        status_code, table = AWSManager.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PROVISIONED',
            provisioned_throughput=provisioned_throughput
        )
        
        assert status_code == 200
        assert table.name == dynamodb_table_config['table_name']
        assert table.provisioned_throughput['ReadCapacityUnits'] == 10
        assert table.provisioned_throughput['WriteCapacityUnits'] == 10
    
    @mock_aws
    def test_create_table_with_sort_key(self, aws_credentials, dynamodb_table_config_with_sort_key):
        """Test creating a DynamoDB table with partition key and sort key."""
        status_code, table = AWSManager.create_dynamodb_table(
            table_name=dynamodb_table_config_with_sort_key['table_name'],
            key_schema=dynamodb_table_config_with_sort_key['key_schema'],
            attribute_definitions=dynamodb_table_config_with_sort_key['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        assert status_code == 200
        assert table.name == dynamodb_table_config_with_sort_key['table_name']
        assert len(table.key_schema) == 2
    
    @mock_aws
    def test_create_table_with_tags(self, aws_credentials, dynamodb_table_config):
        """Test creating a DynamoDB table with tags."""
        tags = [
            {'Key': 'Environment', 'Value': 'test'},
            {'Key': 'Project', 'Value': 'aws-manager'}
        ]
        
        status_code, table = AWSManager.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST',
            tags=tags
        )
        
        assert status_code == 200
        assert table.name == dynamodb_table_config['table_name']


class TestPutAndGetItem:
    """Test suite for put_item_dynamodb and get_item_dynamodb functionality."""
    
    @mock_aws
    def test_put_and_get_item(self, aws_credentials, dynamodb_table_config):
        """Test that after put_item_dynamodb, get_item_dynamodb retrieves the correct item."""
        # Create table
        AWSManager.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        # Put item
        test_item = {
            'id': 'test-id-123',
            'name': 'Test Item',
            'value': 42,
            'active': True
        }
        
        status_code, response = AWSManager.put_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            item=test_item
        )
        
        assert status_code == 200
        
        # Get item
        retrieved_item = AWSManager.get_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            key={'id': 'test-id-123'}
        )
        
        assert retrieved_item == test_item
        assert retrieved_item['id'] == 'test-id-123'
        assert retrieved_item['name'] == 'Test Item'
        assert retrieved_item['value'] == 42
        assert retrieved_item['active'] is True
    
    @mock_aws
    def test_get_nonexistent_item(self, aws_credentials, dynamodb_table_config):
        """Test that get_item_dynamodb returns empty dict for nonexistent item."""
        # Create table
        AWSManager.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        # Get nonexistent item
        retrieved_item = AWSManager.get_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            key={'id': 'nonexistent-id'}
        )
        
        assert retrieved_item == {}
    
    @mock_aws
    def test_put_item_overwrites_existing(self, aws_credentials, dynamodb_table_config):
        """Test that put_item_dynamodb overwrites an existing item."""
        # Create table
        AWSManager.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        # Put first item
        first_item = {'id': 'test-id', 'value': 'first'}
        AWSManager.put_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            item=first_item
        )
        
        # Put second item with same key
        second_item = {'id': 'test-id', 'value': 'second'}
        AWSManager.put_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            item=second_item
        )
        
        # Get item should return second item
        retrieved_item = AWSManager.get_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            key={'id': 'test-id'}
        )
        
        assert retrieved_item['value'] == 'second'


class TestUpdateItem:
    """Test suite for update_item_dynamodb functionality."""
    
    @mock_aws
    def test_update_item_modifies_attributes(self, aws_credentials, dynamodb_table_config):
        """Test that update_item_dynamodb correctly modifies an existing item's attributes."""
        # Create table
        AWSManager.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        # Put item
        original_item = {
            'id': 'test-id',
            'name': 'Original Name',
            'status': 'pending',
            'count': 0
        }
        AWSManager.put_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            item=original_item
        )
        
        # Update item
        status_code, response = AWSManager.update_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            key={'id': 'test-id'},
            update_expression='SET #n = :name, #s = :status, #c = #c + :incr',
            expression_attribute_names={
                '#n': 'name',
                '#s': 'status',
                '#c': 'count'
            },
            expression_attribute_values={
                ':name': 'Updated Name',
                ':status': 'active',
                ':incr': 5
            },
            return_values='ALL_NEW'
        )
        
        assert status_code == 200
        assert response['Attributes']['name'] == 'Updated Name'
        assert response['Attributes']['status'] == 'active'
        assert response['Attributes']['count'] == 5
        
        # Verify with get_item
        retrieved_item = AWSManager.get_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            key={'id': 'test-id'}
        )
        
        assert retrieved_item['name'] == 'Updated Name'
        assert retrieved_item['status'] == 'active'
        assert retrieved_item['count'] == 5
    
    @mock_aws
    def test_update_item_add_new_attribute(self, aws_credentials, dynamodb_table_config):
        """Test that update_item_dynamodb can add new attributes to an item."""
        # Create table
        AWSManager.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        # Put item
        original_item = {'id': 'test-id', 'name': 'Test'}
        AWSManager.put_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            item=original_item
        )
        
        # Update item to add new attribute
        status_code, response = AWSManager.update_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            key={'id': 'test-id'},
            update_expression='SET email = :email',
            expression_attribute_values={':email': 'test@example.com'},
            return_values='ALL_NEW'
        )
        
        assert status_code == 200
        assert response['Attributes']['email'] == 'test@example.com'
        assert response['Attributes']['name'] == 'Test'
    
    @mock_aws
    def test_update_item_remove_attribute(self, aws_credentials, dynamodb_table_config):
        """Test that update_item_dynamodb can remove attributes from an item."""
        # Create table
        AWSManager.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        # Put item
        original_item = {
            'id': 'test-id',
            'name': 'Test',
            'temporary': 'remove-me'
        }
        AWSManager.put_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            item=original_item
        )
        
        # Update item to remove attribute
        status_code, response = AWSManager.update_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            key={'id': 'test-id'},
            update_expression='REMOVE temporary',
            return_values='ALL_NEW'
        )
        
        assert status_code == 200
        assert 'temporary' not in response['Attributes']
        assert response['Attributes']['name'] == 'Test'


class TestDeleteItem:
    """Test suite for delete_item_dynamodb functionality."""
    
    @mock_aws
    def test_delete_item_removes_from_table(self, aws_credentials, dynamodb_table_config):
        """Test that delete_item_dynamodb removes an item from the table."""
        # Create table
        AWSManager.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        # Put item
        test_item = {'id': 'test-id', 'name': 'Test Item'}
        AWSManager.put_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            item=test_item
        )
        
        # Verify item exists
        retrieved_item = AWSManager.get_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            key={'id': 'test-id'}
        )
        assert retrieved_item == test_item
        
        # Delete item
        status_code, response = AWSManager.delete_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            key={'id': 'test-id'}
        )
        
        assert status_code == 200
        
        # Verify item is deleted
        retrieved_item = AWSManager.get_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            key={'id': 'test-id'}
        )
        assert retrieved_item == {}
    
    @mock_aws
    def test_delete_nonexistent_item(self, aws_credentials, dynamodb_table_config):
        """Test that deleting a nonexistent item doesn't raise an error."""
        # Create table
        AWSManager.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        # Delete nonexistent item (should succeed without error)
        status_code, response = AWSManager.delete_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            key={'id': 'nonexistent-id'}
        )
        
        assert status_code == 200
    
    @mock_aws
    def test_delete_multiple_items(self, aws_credentials, dynamodb_table_config):
        """Test deleting multiple items from the table."""
        # Create table
        AWSManager.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        # Put multiple items
        items = [
            {'id': 'id-1', 'name': 'Item 1'},
            {'id': 'id-2', 'name': 'Item 2'},
            {'id': 'id-3', 'name': 'Item 3'}
        ]
        
        for item in items:
            AWSManager.put_item_dynamodb(
                table_name=dynamodb_table_config['table_name'],
                item=item
            )
        
        # Delete items one by one
        for item_id in ['id-1', 'id-2', 'id-3']:
            status_code, _ = AWSManager.delete_item_dynamodb(
                table_name=dynamodb_table_config['table_name'],
                key={'id': item_id}
            )
            assert status_code == 200
        
        # Verify all items are deleted
        for item_id in ['id-1', 'id-2', 'id-3']:
            retrieved_item = AWSManager.get_item_dynamodb(
                table_name=dynamodb_table_config['table_name'],
                key={'id': item_id}
            )
            assert retrieved_item == {}


class TestCopyTableToAWS:
    """Test suite for copy_table_to_aws functionality."""
    
    @mock_aws
    def test_copy_table_migrates_schema_and_data(self, aws_credentials, dynamodb_table_config):
        """Test that copy_table_to_aws successfully migrates a table and its data."""
        # Create local table (simulated with moto)
        local_aws = Aws(use_local_dynamodb=True)
        local_aws.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        # Add items to local table
        test_items = [
            {'id': 'item-1', 'name': 'Item One', 'value': 100},
            {'id': 'item-2', 'name': 'Item Two', 'value': 200},
            {'id': 'item-3', 'name': 'Item Three', 'value': 300}
        ]
        
        for item in test_items:
            local_aws.put_item_dynamodb(
                table_name=dynamodb_table_config['table_name'],
                item=item
            )
        
        # Copy table to AWS (destination name different)
        destination_table = 'aws-test-table'
        status_code, message = AWSManager.copy_table_to_aws(
            source_table_name=dynamodb_table_config['table_name'],
            destination_table_name=destination_table
        )
        
        assert status_code == 200
        assert destination_table in message
        assert '3 ITEMS MIGRATED' in message
        
        # Verify table exists on AWS
        aws_client = Aws(use_local_dynamodb=False)
        schema = aws_client.get_table_schema(destination_table)
        assert schema['table_name'] == destination_table
        assert schema['billing_mode'] == 'PAY_PER_REQUEST'
        
        # Verify all items migrated
        for item in test_items:
            retrieved_item = aws_client.get_item_dynamodb(
                table_name=destination_table,
                key={'id': item['id']}
            )
            assert retrieved_item['id'] == item['id']
            assert retrieved_item['name'] == item['name']
            assert retrieved_item['value'] == item['value']
    
    @mock_aws
    def test_copy_table_empty_table(self, aws_credentials, dynamodb_table_config):
        """Test that copy_table_to_aws handles empty tables correctly."""
        # Create local table (simulated with moto)
        local_aws = Aws(use_local_dynamodb=True)
        local_aws.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        # Copy empty table
        destination_table = 'aws-empty-table'
        status_code, message = AWSManager.copy_table_to_aws(
            source_table_name=dynamodb_table_config['table_name'],
            destination_table_name=destination_table
        )
        
        assert status_code == 200
        assert '0 items migrated' in message.lower()
        
        # Verify table exists on AWS
        aws_client = Aws(use_local_dynamodb=False)
        schema = aws_client.get_table_schema(destination_table)
        assert schema['table_name'] == destination_table
    
    @mock_aws
    def test_copy_table_same_name(self, aws_credentials, dynamodb_table_config):
        """Test that copy_table_to_aws uses source name when destination not specified."""
        # Create local table
        local_aws = Aws(use_local_dynamodb=True)
        local_aws.create_dynamodb_table(
            table_name=dynamodb_table_config['table_name'],
            key_schema=dynamodb_table_config['key_schema'],
            attribute_definitions=dynamodb_table_config['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        # Add item
        test_item = {'id': 'test-1', 'data': 'test data'}
        local_aws.put_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            item=test_item
        )
        
        # Copy without specifying destination name
        status_code, message = AWSManager.copy_table_to_aws(
            source_table_name=dynamodb_table_config['table_name']
        )
        
        assert status_code == 200
        assert dynamodb_table_config['table_name'] in message
        
        # Verify table exists with same name on AWS
        aws_client = Aws(use_local_dynamodb=False)
        retrieved_item = aws_client.get_item_dynamodb(
            table_name=dynamodb_table_config['table_name'],
            key={'id': 'test-1'}
        )
        assert retrieved_item['data'] == 'test data'
    
    @mock_aws
    def test_copy_table_with_sort_key(self, aws_credentials, dynamodb_table_config_with_sort_key):
        """Test that copy_table_to_aws handles tables with sort keys correctly."""
        # Create local table with sort key
        local_aws = Aws(use_local_dynamodb=True)
        local_aws.create_dynamodb_table(
            table_name=dynamodb_table_config_with_sort_key['table_name'],
            key_schema=dynamodb_table_config_with_sort_key['key_schema'],
            attribute_definitions=dynamodb_table_config_with_sort_key['attribute_definitions'],
            billing_mode='PAY_PER_REQUEST'
        )
        
        # Add items with composite keys
        test_items = [
            {'pk': 'user-1', 'sk': 'order-001', 'total': 100},
            {'pk': 'user-1', 'sk': 'order-002', 'total': 150},
            {'pk': 'user-2', 'sk': 'order-001', 'total': 200}
        ]
        
        for item in test_items:
            local_aws.put_item_dynamodb(
                table_name=dynamodb_table_config_with_sort_key['table_name'],
                item=item
            )
        
        # Copy table
        destination_table = 'aws-sort-key-table'
        status_code, message = AWSManager.copy_table_to_aws(
            source_table_name=dynamodb_table_config_with_sort_key['table_name'],
            destination_table_name=destination_table
        )
        
        assert status_code == 200
        assert '3 ITEMS MIGRATED' in message
        
        # Verify schema copied correctly
        aws_client = Aws(use_local_dynamodb=False)
        schema = aws_client.get_table_schema(destination_table)
        assert len(schema['key_schema']) == 2
        
        # Verify items with composite keys
        for item in test_items:
            retrieved_item = aws_client.get_item_dynamodb(
                table_name=destination_table,
                key={'pk': item['pk'], 'sk': item['sk']}
            )
            assert retrieved_item['total'] == item['total']
