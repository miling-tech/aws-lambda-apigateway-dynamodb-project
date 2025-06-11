import boto3

def create_api():

    client = boto3.client('apigateway', endpoint_url='http://localhost:4566')

    api = client.create_rest_api(name='RoleAPI')
    api_id = api['id']

    resources = client.get_resources(restApiId=api_id)
    root_id = None
    for item in resources['items']:
        if item['path'] == '/':
            root_id = item['id']
            break

    resource = client.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart='roles'
    )
    resource_id = resource['id']

    client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='POST',
        authorizationType='NONE'
    )

    lambda_arn = 'arn:aws:lambda:us-east-1:000000000000:function:my-lambda-function'

    client.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod='POST',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
    )

    lambda_client = boto3.client('lambda', endpoint_url='http://localhost:4566')

    try:
        lambda_client.add_permission(
            FunctionName='my-lambda-function',
            StatementId='apigateway-invoke-permissions',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:us-east-1:000000000000:{api_id}/*/POST/roles'
        )
    except lambda_client.exceptions.ResourceConflictException:
        print('Permission already exists')

    deployment = client.create_deployment(
        restApiId=api_id,
        stageName='dev'
    )

    print(f"API ID: {api_id}")
    print(f"Invoke URL: http://localhost:4566/restapis/{api_id}/dev/_user_request_/roles")
    return api_id