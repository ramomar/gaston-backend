import os
import json
import base64
import boto3
from boto3.dynamodb.conditions import Key

IS_AWS = bool(os.environ.get('AWS_EXECUTION_ENV', False))
OWNER_ID = os.environ.get('OWNER_ID', 'ramomar')
GET_RECORDS_QUERY_LIMIT = int(os.environ.get('GET_RECORDS_QUERY_LIMIT', 10))


def get_records(event, context):
    client = boto3.resource('dynamodb', **{} if IS_AWS else {'endpoint_url': 'http://localhost:8000'})
    table = client.Table('gaston' if IS_AWS else 'gaston-local')
    page = event.get('queryStringParameters', {}).get('page', None)
    only_unreviewed = 'unreviewed' in event.get('path', '')
    exclusive_start_key = json.loads(base64.b64decode(page)) if page else None
    query = table.query(KeyConditionExpression=Key('owner_id').eq(OWNER_ID),
                        Limit=GET_RECORDS_QUERY_LIMIT,
                        **{'ExclusiveStartKey': exclusive_start_key} if exclusive_start_key else {},
                        **{'FilterExpression': 'attribute_not_exists(review)'} if only_unreviewed else {},
                        )
    last_evaluated_key = query.get('LastEvaluatedKey', None)
    result = {
        'records': query['Items'],
        'hasMore': last_evaluated_key is not None,
        'nextPage': base64.urlsafe_b64encode(json.dumps(last_evaluated_key, default=str, ensure_ascii=False).encode('utf-8')).decode('utf-8') if last_evaluated_key else None,
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
        'record': get_item_result.get('Item', None)
    }

    return {
        'statusCode': 200 if 'Item' in get_item_result else 404,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(result, indent=4, default=str),
    }
