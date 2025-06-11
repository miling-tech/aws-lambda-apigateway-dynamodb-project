import json
import unittest
import boto3
from lambda_function import lambda_handler
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


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
        except cls.dynamodb.meta.client.exceptions.ResourceInUseException:
            cls.table = cls.dynamodb.Table('Roles')
        except Exception as e:
            print(f"Critical error during setup: {str(e)}")
            raise

    def setUp(self):
        try:
            scan = self.table.scan()
            with self.table.batch_writer() as batch:
                for item in scan.get('Items', []):
                    batch.delete_item(Key={'id': item['id']})
        except Exception as e:
            print(f"Cleanup error: {str(e)}")
            raise

    def test_lambda_put_item(self):
        event = {
            'httpMethod': 'POST',
            'body': json.dumps({
                'id': '100',
                'type': 'Admin',
                'permissions': {'Read': 'True'}
            })
        }

        response = lambda_handler(event, None)
        self.assertIn('Item created', response['body'])

    def test_lambda_get_item(self):
        self.table.put_item(Item={
            'id': '200',
            'type': 'User',
            'permissions': {'Write': 'False'}
        })

        event = {
            'httpMethod': 'GET',
            'queryStringParameters': {'id': '200'}
        }

        response = lambda_handler(event, None)
        body = json.loads(response['body'])

        self.assertEqual(body['type'], 'User')

    def test_lambda_update_item(self):
        self.table.put_item(Item={
            'id': '300',
            'type': 'Temporary',
            'permissions': {'Read': 'True'}
        })

        event = {
            'httpMethod': 'PUT',
            'body': json.dumps({
                'id': '300',
                'type': 'Permanent',
                'permissions': {'Read': 'False'}
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(200, response['statusCode'])

        updated_item = self.table.get_item(Key={'id': '300'}).get('Item', {})
        self.assertEqual(updated_item['type'], 'Permanent')

    def test_lambda_delete_item(self):
        self.table.put_item(Item={
            'id': '400',
            'type': 'ToDelete'
        })

        event = {
            'httpMethod': 'DELETE',
            'body': json.dumps({'id': '400'})
        }

        response = lambda_handler(event, None)
        self.assertEqual(204, response['statusCode'])

        item = self.table.get_item(Key={'id': '400'}).get('Item')
        self.assertIsNone(item)

    def test_invalid_method(self):
        event = {
            'httpMethod': 'PATCH',
            'body': json.dumps({'id': '500'})
        }

        response = lambda_handler(event, None)
        self.assertIn('Method not allowed', response['body'])

    def test_missing_parameters(self):
        event = {
            'httpMethod': 'GET',
            'queryStringParameters': {}
        }

        response = lambda_handler(event, None)
        self.assertEqual(400, response['statusCode'])


if __name__ == '__main__':
    unittest.main()
