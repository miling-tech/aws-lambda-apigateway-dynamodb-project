import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566'
)

def createBasicDynamoDBTable():
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

def dynamoDBMain():
    if not isTableExisting('Roles'):
        createBasicDynamoDBTable()
    putItemIntoTable()


def isTableExisting(table_name):
    client = boto3.client('dynamodb', endpoint_url='http://localhost:4566')
    tables = client.list_tables()['TableNames']
    if table_name in tables:
        return True
    else:
        return False


def putItemIntoTable():
    table = dynamodb.Table('Roles')
    table.put_item(Item={
        'id': '1', 'type': 'Administrator', 'permissions': {
            'FullAccess': 'True', 'AllCosts': 'True'
        }})

def showingAllTablesInDynamoDB():
    client = boto3.client('dynamodb', endpoint_url='http://localhost:4566')
    tables = client.list_tables()['TableNames']
    for table in tables:
        print(table)


if __name__ == '__main__':
    dynamoDBMain()
    print('--------')
    showingAllTablesInDynamoDB()
