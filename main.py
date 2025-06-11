import boto3

import createLambdaFunctionFromZipFile
import create_api
import dynamodb
import lambda_function
import sendRequest


def main():
    dynamodb.dynamo_db_main()
    dynamodb.showing_all_tables_in_dynamo_db()
    lambda_function.lambda_handler({}, None)
    createLambdaFunctionFromZipFile.create_lambda_function_from_zip_file()
    api_id = create_api.create_api()
    sendRequest.send_request(api_id)


if __name__ == '__main__':
    main()
