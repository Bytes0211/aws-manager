# DynamoDB Unit Tests

This file contains comprehensive unit tests for the DynamoDB operations in the AWS Manager project.

## Test Coverage

The test suite covers the following DynamoDB operations:

### 1. `create_dynamodb_table`
- ✅ Creating tables with PAY_PER_REQUEST billing mode
- ✅ Creating tables with PROVISIONED billing mode
- ✅ Creating tables with partition key and sort key
- ✅ Creating tables with tags

### 2. `put_item_dynamodb` and `get_item_dynamodb`
- ✅ Putting and retrieving items from DynamoDB
- ✅ Getting nonexistent items (returns empty dict)
- ✅ Overwriting existing items with put_item

### 3. `update_item_dynamodb`
- ✅ Modifying existing item attributes
- ✅ Adding new attributes to items
- ✅ Removing attributes from items
- ✅ Incrementing numeric values

### 4. `delete_item_dynamodb`
- ✅ Removing items from tables
- ✅ Deleting nonexistent items (no error)
- ✅ Deleting multiple items

### 5. `copy_table_to_aws`
- ✅ Migrating table schema from local to AWS
- ✅ Migrating all table data
- ✅ Handling empty tables
- ✅ Using default destination table name
- ✅ Handling tables with composite keys (partition + sort)

## Installation

Install test dependencies:

```bash
pip install -r requirements-test.txt
```

Or install individually:

```bash
pip install pytest pytest-cov moto[dynamodb]
```

## Running Tests

### Run all tests
```bash
pytest test_dynamodb.py -v
```

### Run specific test class
```bash
pytest test_dynamodb.py::TestCreateDynamoDBTable -v
```

### Run specific test
```bash
pytest test_dynamodb.py::TestPutAndGetItem::test_put_and_get_item -v
```

### Run with coverage report
```bash
pytest test_dynamodb.py --cov=aws_manager --cov=resources.aws --cov-report=html
```

### Run with detailed output
```bash
pytest test_dynamodb.py -vv -s
```

## Test Structure

The tests use:
- **pytest**: Testing framework
- **moto**: AWS service mocking library (no real AWS calls or costs)
- **fixtures**: Reusable test configurations for DynamoDB tables

### Key Fixtures

- `aws_credentials`: Mocks AWS credentials for testing
- `dynamodb_table_config`: Simple table with partition key only
- `dynamodb_table_config_with_sort_key`: Table with partition + sort key

## Mocking Strategy

All tests use the `@mock_aws` decorator from `moto` to:
- Mock AWS DynamoDB services completely
- Avoid real AWS API calls
- Run tests locally without AWS credentials
- Execute tests quickly without network latency
- Prevent any AWS charges

## Test Classes

### `TestCreateDynamoDBTable`
Tests table creation with various configurations including billing modes, keys, and tags.

### `TestPutAndGetItem`
Tests item insertion and retrieval operations, ensuring data integrity.

### `TestUpdateItem`
Tests item updates including modifying attributes, adding new fields, and removing fields.

### `TestDeleteItem`
Tests item deletion including edge cases like deleting nonexistent items.

### `TestCopyTableToAWS`
Tests the migration functionality from local DynamoDB to AWS, including schema and data transfer.

## CI/CD Integration

To integrate with CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    pip install -r requirements-test.txt

- name: Run tests
  run: pytest test_dynamodb.py -v --cov --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Notes

- All tests are isolated and independent
- Tests use in-memory mocked services (no real AWS infrastructure)
- Each test creates its own table to avoid conflicts
- Mock data is automatically cleaned up after each test
