import json
import boto3

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566', # for test-usage there is host not stack
    region_name='us-east-1',              # in zip file there is stack
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

table = dynamodb.Table('Roles')


def lambda_put_item(body):
    table.put_item(Item={
        'id': body['id'],
        'type': body['type'],
        'permissions': body.get('permissions', {})
    })


def lambda_get_item(role_id):
    response = table.get_item(Key={'id': role_id})
    return response.get('Item', {})


def lambda_update_item(body):
    table.update_item(
        Key={'id': body['id']},
        UpdateExpression='SET #t = :t, #p = :p',
        ExpressionAttributeNames={
            '#t': 'type',
            '#p': 'permissions'
        },
        ExpressionAttributeValues={
            ':t': body['type'],
            ':p': body.get('permissions', {})
        }
    )


def lambda_delete_item(role_id):
    table.delete_item(Key={'id': role_id})


def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        http_method = event.get('httpMethod')
        body = json.loads(event['body']) if 'body' in event else {}

        if http_method == 'POST':
            lambda_put_item(body)
            return {
                'statusCode': 201,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'message': 'Item created'})
            }

        elif http_method == 'GET':
            role_id = event['queryStringParameters']['id']
            item = lambda_get_item(role_id)
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(item)
            }

        elif http_method == 'PUT':
            lambda_update_item(body)
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'message': 'Item updated'})
            }

        elif http_method == 'DELETE':
            role_id = body['id']
            lambda_delete_item(role_id)
            return {
                'statusCode': 204,
                'headers': {'Content-Type': 'application/json'},
                'body': ''
            }

        else:
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }

    except KeyError as e:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Missing parameter: {str(e)}'})
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Invalid JSON format'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
