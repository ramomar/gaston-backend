import os
import json
import copy
import boto3
from decimal import Decimal
import botocore.exceptions

IS_AWS = bool(os.environ.get('AWS_EXECUTION_ENV', False))
OWNER_ID = os.environ.get('OWNER_ID', 'ramomar')


def put_record_review(event, context):
    client = boto3.resource('dynamodb', **{} if IS_AWS else {'endpoint_url': 'http://localhost:8000'})
    table = client.Table('gaston' if IS_AWS else 'gaston-local')
    request_body = json.loads(event['body']) if event['body'] else {}

    if 'review' not in request_body:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': {
                'code': 'NoReview',
                'message': 'Review is not present'
            },
        }

    try:
        review = request_body['review']
        new_review = dict(review, **{'amount': Decimal(review['amount'])})
        update_result = table.update_item(
            Key={'owner_id': OWNER_ID, 'record_id': event['pathParameters']['record_id']},
            ReturnValues='ALL_NEW',
            UpdateExpression='SET review = :review',
            ExpressionAttributeValues={
                ':review': new_review,
            },
            ConditionExpression='attribute_exists(record_id)'
        )['Attributes']
        record = copy.deepcopy(update_result)
        review = copy.deepcopy(update_result['review'])

        del record['review']

        result = {
            'record': record,
            'review': review,
        }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(result, indent=4, default=str),
        }
    except botocore.exceptions.ClientError as error:
        error_details = error.response['Error']

        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': {
                'code': error_details['Code'],
                'message': error_details['Message'],
            },
        }
