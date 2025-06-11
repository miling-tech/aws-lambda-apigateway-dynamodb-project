import boto3
import zipfile


def create_lambda_function_from_zip_file():
    with zipfile.ZipFile('lambda_function.zip', 'r') as zipf:
        print(zipf.namelist())

    lambda_client = boto3.client('lambda', endpoint_url='http://localhost:4566')

    with open('lambda_function.zip', 'rb') as f:
        zipped_code = f.read()

    try:
        response = lambda_client.create_function(
            FunctionName='my-lambda-function',
            Runtime='python3.12',
            Role='arn:aws:iam::000000000000:role/lambda-role',
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zipped_code},
            Publish=True,
        )
        print("Created function:", response['FunctionName'])
    except lambda_client.exceptions.ResourceConflictException:
        print("Function already exists, updating code...")
        response = lambda_client.update_function_code(
            FunctionName='my-lambda-function',
            ZipFile=zipped_code
        )
        print("Updated function:", response['FunctionName'])
