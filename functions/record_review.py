import os
import json
import boto3
from decimal import Decimal
import botocore.exceptions

IS_AWS = os.environ.get('AWS_EXECUTION_ENV', False)
OWNER_ID = os.environ.get('OWNER_ID', 'ramomar')


def put_review(event, context):
    client = boto3.resource('dynamodb', **{} if IS_AWS else {'endpoint_url': 'http://localhost:8000'})
    table = client.Table('gaston' if IS_AWS else 'gaston-local')

    if 'review' not in event:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': {
                'code': 'NoReview',
                'message': 'Review is not present'
            },
        }

    try:
        review = dict(event['review'], **{'amount': Decimal(event['review']['amount'])}) if 'amount' in event else event['review']

        update_result = table.update_item(
            Key={'owner_id': OWNER_ID, 'record_id': event['record_id']},
            ReturnValues='ALL_NEW',
            UpdateExpression='SET review = :review',
            ExpressionAttributeValues={
                ':review': review,
            },
            ConditionExpression='attribute_exists(record_id)'
        )
        result = {
            'record': update_result['Attributes'],
        }
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps(result, indent=4, default=str),
        }
    except botocore.exceptions.ClientError as error:
        error_details = error.response['Error']

        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': {
                'code': error_details['Code'],
                'message': error_details['Message'],
            },
        }
