import os
import json
import boto3
from boto3.dynamodb.conditions import Key

IS_AWS = os.environ.get('AWS_EXECUTION_ENV', False)
OWNER_ID = os.environ.get('OWNER_ID', 'ramomar')


def get_records(event, context):
    client = boto3.resource('dynamodb', **{} if IS_AWS else {'endpoint_url': 'http://localhost:8000'})
    table = client.Table('gaston' if IS_AWS else 'gaston-local')
    query = table.query(KeyConditionExpression=Key('owner_id').eq(OWNER_ID))
    result = {
        'records': query['Items'],
    }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(result, indent=4, default=str),
    }


def get_record(event, context):
    client = boto3.resource('dynamodb', **{} if IS_AWS else {'endpoint_url': 'http://localhost:8000'})
    table = client.Table('gaston' if IS_AWS else 'gaston-local')
    get_item_result = table.get_item(Key={'owner_id': OWNER_ID, 'record_id': event['pathParameters']['record_id']})
    result = {
        'record': get_item_result['Item'] if 'Item' in get_item_result else None
    }

    return {
        'statusCode': 200 if 'Item' in get_item_result else 404,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(result, indent=4, default=str),
    }
