import json
import unittest
import boto3
from lambda_function import lambda_handler


class LambdaFunctionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url='http://localhost:4566',
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )

        try:
            cls.table = cls.dynamodb.create_table(
                TableName='Roles',
                KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
                BillingMode='PAY_PER_REQUEST'
            )
            cls.table.wait_until_exists()
        except Exception as e:
            cls.table = cls.dynamodb.Table('Roles')

    def setUp(self):
        self.table.scan().get('Items', [])

    def test_create_item(self):
        event = {
            'httpMethod': 'POST',
            'body': json.dumps({
                'id': 'test1',
                'type': 'Admin',
                'permissions': {'read': True}
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 201)
        self.assertIn('Item created', response['body'])

    def test_get_item(self):
        self.test_create_item()

        event = {
            'httpMethod': 'GET',
            'queryStringParameters': {'id': 'test1'}
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['id'], 'test1')

    def test_update_item(self):
        self.test_create_item()

        event = {
            'httpMethod': 'PUT',
            'body': json.dumps({
                'id': 'test1',
                'type': 'SuperAdmin',
                'permissions': {'read': True, 'write': True}
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)

        get_event = {
            'httpMethod': 'GET',
            'queryStringParameters': {'id': 'test1'}
        }
        updated_item = json.loads(lambda_handler(get_event, None)['body'])
        self.assertEqual(updated_item['type'], 'SuperAdmin')

    def test_delete_item(self):
        self.test_create_item()

        event = {
            'httpMethod': 'DELETE',
            'body': json.dumps({'id': 'test1'})
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 204)

        get_event = {
            'httpMethod': 'GET',
            'queryStringParameters': {'id': 'test1'}
        }
        response = lambda_handler(get_event, None)
        self.assertEqual(json.loads(response['body']), {})

    def test_invalid_method(self):
        event = {
            'httpMethod': 'PATCH',
            'body': json.dumps({'id': 'test1'})
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 405)

    def test_missing_parameters(self):
        event = {
            'httpMethod': 'POST',
            'body': json.dumps({'type': 'Admin'})  # Brak id
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)


if __name__ == '__main__':
    unittest.main(buffer=False)
