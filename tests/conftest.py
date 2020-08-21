import pytest
import logging
from os import path
import json
import boto3


@pytest.fixture
def load_event():
    def _load_event(event_path):
        filepath = path.join(path.dirname(__file__), event_path)

        with open(filepath) as event_file:
            event = json.loads(event_file.read())

        return event

    return _load_event


# When the time is needed don't use auto
@pytest.fixture(autouse=True)
def gaston_table():
    logger = logging.getLogger(__name__)
    table_name = 'gaston-local'
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

    try:
        table = dynamodb.Table(table_name)
        table.delete(TableName=table_name)
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        logger.info('No table exists')

    logger.info('Creating table')

    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'owner_id',
                'KeyType': 'HASH',
             },
            {
                'AttributeName': 'record_id',
                'KeyType': 'RANGE',
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'owner_id',
                'AttributeType': 'S',
            },
            {
                'AttributeName': 'record_id',
                'AttributeType': 'S',
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }
    )

    table = dynamodb.Table(table_name)

    return table
