import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566'
)

def create_basic_dynamodb_table():
    table = dynamodb.create_table(
        TableName='Roles',
        KeySchema=[{
            'AttributeName': 'id',
            'KeyType': 'HASH'
        }],
        AttributeDefinitions=[{
            'AttributeName': 'id',
            'AttributeType': 'S'
        }],
        BillingMode='PAY_PER_REQUEST'
    )
    table.wait_until_exists()

def dynamo_db_main():
    if not is_table_existing('Roles'):
        create_basic_dynamodb_table()
    put_item_into_table()


def is_table_existing(table_name):
    client = boto3.client('dynamodb', endpoint_url='http://localhost:4566')
    tables = client.list_tables()['TableNames']
    if table_name in tables:
        return True
    else:
        return False


def put_item_into_table():
    table = dynamodb.Table('Roles')
    table.put_item(Item={
        'id': '1', 'type': 'Administrator', 'permissions': {
            'FullAccess': 'True', 'AllCosts': 'True'
        }})

def showing_all_tables_in_dynamo_db():
    client = boto3.client('dynamodb', endpoint_url='http://localhost:4566')
    tables = client.list_tables()['TableNames']
    for table in tables:
        print(table)


if __name__ == '__main__':
    dynamo_db_main()
    print('--------')
    showing_all_tables_in_dynamo_db()
