import json
import uuid
from decimal import Decimal
from functions import record


def test_get_records_empty():
    """it should return an empty list when there are no records"""
    event = {}
    actual = record.get_records(event, context=None)
    expected_body = {
        'records': [],
        'hasMore': False,
        'nextPage': None,
    }
    expected = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(expected_body, indent=4),
    }

    assert actual == expected


def test_get_records(gaston_table):
    """it should return a list of records"""
    record_raw = {
        'source': 'FAST_TRANSFER_EMAIL',
        'type': 'EXPENSE',
        'note': 'Transferencias Rápidas | P',
        'amount': '650',
        'operation_date': '27/Jul/2020 18:56:55 horas',
        'application_date': None,
        'receiver': {
            'name': 'No capturado',
            'bank': 'BANCO'
        },
        'channel': None,
        'extra_amounts': [
            {
                'name': 'fee',
                'amount': '3.00',
                'tax': '0.48',
            }
        ],
    }
    item = {
        'owner_id': 'ramomar',
        'record_id': str(uuid.uuid4()),
        'note': record_raw['note'],
        'amount': Decimal(record_raw['amount']),
        'date': record_raw['operation_date'],
        'raw': json.dumps(record_raw, default=str),
        'origin': 'BANORTE_EMAIL_SES',
    }

    gaston_table.put_item(Item=item)

    event = {}
    actual = record.get_records(event, context=None)
    expected_body = {
        'records': [
            item,
        ],
        'hasMore': False,
        'nextPage': None,
    }
    expected = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(expected_body, indent=4, default=str)
    }

    assert actual['statusCode'] == expected['statusCode']
    assert actual['headers'] == expected['headers']
    assert json.loads(actual['body']) == json.loads(expected['body'])


def test_paginate_records(gaston_table):
    """it should paginate records"""
    record_raw = {
        'source': 'FAST_TRANSFER_EMAIL',
        'type': 'EXPENSE',
        'note': 'Transferencias Rápidas | P',
        'amount': '650',
        'operation_date': '27/Jul/2020 18:56:55 horas',
        'application_date': None,
        'receiver': {
            'name': 'No capturado',
            'bank': 'BANCO'
        },
        'channel': None,
        'extra_amounts': [
            {
                'name': 'fee',
                'amount': '3.00',
                'tax': '0.48',
            }
        ],
    }
    item = {
        'owner_id': 'ramomar',
        'record_id': '5f018b3d-e50e-44c9-a540-1717e00f09ba',
        'note': record_raw['note'],
        'amount': Decimal(record_raw['amount']),
        'date': record_raw['operation_date'],
        'raw': json.dumps(record_raw, default=str),
        'origin': 'BANORTE_EMAIL_SES',
    }

    gaston_table.put_item(Item=item)

    old_record = record.GET_RECORDS_QUERY_LIMIT
    record.GET_RECORDS_QUERY_LIMIT = 1
    event = {}
    actual = record.get_records(event, context=None)
    record.GET_RECORDS_QUERY_LIMIT = old_record
    expected_body = {
        'records': [
            item,
        ],
        'hasMore': True,
        'nextPage': 'eyJyZWNvcmRfaWQiOiAiNWYwMThiM2QtZTUwZS00NGM5LWE1NDAtMTcxN2UwMGYwOWJhIiwgIm93bmVyX2lkIjogInJhbW9tYXIifQ==',
    }
    expected = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(expected_body, indent=4, default=str)
    }

    assert actual['statusCode'] == expected['statusCode']
    assert actual['headers'] == expected['headers']
    assert json.loads(actual['body']) == json.loads(expected['body'])


def test_paginate_records_next_page(gaston_table):
    """it should be able to go to the next page"""
    record_raw = {
        'source': 'FAST_TRANSFER_EMAIL',
        'type': 'EXPENSE',
        'note': 'Transferencias Rápidas | P',
        'amount': '650',
        'operation_date': '27/Jul/2020 18:56:55 horas',
        'application_date': None,
        'receiver': {
            'name': 'No capturado',
            'bank': 'BANCO'
        },
        'channel': None,
        'extra_amounts': [
            {
                'name': 'fee',
                'amount': '3.00',
                'tax': '0.48',
            }
        ],
    }
    item = {
        'owner_id': 'ramomar',
        'record_id': '5f018b3d-e50e-44c9-a540-1717e00f09ba',
        'note': record_raw['note'],
        'amount': Decimal(record_raw['amount']),
        'date': record_raw['operation_date'],
        'raw': json.dumps(record_raw, default=str),
        'origin': 'BANORTE_EMAIL_SES',
    }
    record_raw_2 = {
        'source': 'FAST_TRANSFER_EMAIL',
        'type': 'EXPENSE',
        'note': 'Transferencias Rápidas | P',
        'amount': '651',
        'operation_date': '27/Jul/2020 18:56:55 horas',
        'application_date': None,
        'receiver': {
            'name': 'No capturado',
            'bank': 'BANCO'
        },
        'channel': None,
        'extra_amounts': [
            {
                'name': 'fee',
                'amount': '3.00',
                'tax': '0.48',
            }
        ],
    }
    item_2 = {
        'owner_id': 'ramomar',
        'record_id': 'e12c0208-250f-4231-858b-ed82ffa4ed5e',
        'note': record_raw_2['note'],
        'amount': Decimal(record_raw['amount']),
        'date': record_raw_2['operation_date'],
        'raw': json.dumps(record_raw_2, default=str),
        'origin': 'BANORTE_EMAIL_SES',
    }

    gaston_table.put_item(Item=item)
    gaston_table.put_item(Item=item_2)

    old_record = record.GET_RECORDS_QUERY_LIMIT
    record.GET_RECORDS_QUERY_LIMIT = 1
    first_page_records = record.get_records({}, context=None)
    next_page_event = {
        'queryStringParameters': {
            'page': json.loads(first_page_records['body'])['nextPage'],
        }
    }
    next_page = record.get_records(next_page_event, context=None)
    record.GET_RECORDS_QUERY_LIMIT = old_record
    expected_body = {
        'records': [
            item_2,
        ],
        # Even if it's the last item, DynamoDb still returns a LastEvaluatedKey. The next query will return empty.
        'hasMore': True,
        'nextPage': 'eyJyZWNvcmRfaWQiOiAiZTEyYzAyMDgtMjUwZi00MjMxLTg1OGItZWQ4MmZmYTRlZDVlIiwgIm93bmVyX2lkIjogInJhbW9tYXIifQ==',
    }
    expected = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(expected_body, indent=4, default=str)
    }

    assert next_page['statusCode'] == expected['statusCode']
    assert next_page['headers'] == expected['headers']
    assert json.loads(next_page['body']) == json.loads(expected['body'])


def test_get_unreviewed_records(gaston_table):
    """it should return a list of unreviewed records"""
    record_raw = {
        'source': 'FAST_TRANSFER_EMAIL',
        'type': 'EXPENSE',
        'note': 'Transferencias Rápidas | P',
        'amount': '650',
        'operation_date': '27/Jul/2020 18:56:55 horas',
        'application_date': None,
        'receiver': {
            'name': 'No capturado',
            'bank': 'BANCO'
        },
        'channel': None,
        'extra_amounts': [
            {
                'name': 'fee',
                'amount': '3.00',
                'tax': '0.48',
            }
        ],
    }
    unreviewed_record = {
        'owner_id': 'ramomar',
        'record_id': '5f018b3d-e50e-44c9-a540-1717e00f09ba',
        'note': record_raw['note'],
        'amount': Decimal(record_raw['amount']),
        'date': record_raw['operation_date'],
        'raw': json.dumps(record_raw, default=str),
        'origin': 'BANORTE_EMAIL_SES',
    }
    record_raw_2 = {
        'source': 'FAST_TRANSFER_EMAIL',
        'type': 'EXPENSE',
        'note': 'Transferencias Rápidas | P',
        'amount': '651',
        'operation_date': '27/Jul/2020 18:56:55 horas',
        'application_date': None,
        'receiver': {
            'name': 'No capturado',
            'bank': 'BANCO'
        },
        'channel': None,
        'extra_amounts': [
            {
                'name': 'fee',
                'amount': '3.00',
                'tax': '0.48',
            }
        ],
    }
    reviewed_record = {
        'owner_id': 'ramomar',
        'record_id': 'e12c0208-250f-4231-858b-ed82ffa4ed5e',
        'note': record_raw_2['note'],
        'amount': Decimal(record_raw['amount']),
        'date': record_raw_2['operation_date'],
        'raw': json.dumps(record_raw_2, default=str),
        'origin': 'BANORTE_EMAIL_SES',
        'review': {
            'amount': '651',
            'date': '2020-07-19T18:56:00.000Z',
            'note': 'Salud',
            'category': 'Salud',
        },
    }

    gaston_table.put_item(Item=unreviewed_record)
    gaston_table.put_item(Item=reviewed_record)

    event = {
        'pathParameters': {
            'status': 'unreviewed',
        },
    }
    actual = record.get_records(event, context=None)
    expected_body = {
        'records': [
            unreviewed_record,
        ],
        'hasMore': False,
        'nextPage': None,
    }
    expected = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(expected_body, indent=4, default=str)
    }

    assert actual['statusCode'] == expected['statusCode']
    assert actual['headers'] == expected['headers']
    assert json.loads(actual['body']) == json.loads(expected['body'])


def test_get_record_not_found():
    """it should return nothing when the record is not found"""
    event = {
        'pathParameters': {
            'record_id': str(uuid.uuid4()),
        }
    }
    actual = record.get_record(event, context=None)
    expected_body = {
        'record': None
    }
    expected = {
        'statusCode': 404,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(expected_body, indent=4, default=str)
    }

    assert actual == expected


def test_get_record(gaston_table):
    """it should return a record"""
    record_raw = {
        'source': 'FAST_TRANSFER_EMAIL',
        'type': 'EXPENSE',
        'note': 'Transferencias Rápidas | P',
        'amount': '650',
        'operation_date': '27/Jul/2020 18:56:55 horas',
        'application_date': None,
        'receiver': {
            'name': 'No capturado',
            'bank': 'BANCO'
        },
        'channel': None,
        'extra_amounts': [
            {
                'name': 'fee',
                'amount': '3.00',
                'tax': '0.48',
            }
        ],
    }
    item_id = str(uuid.uuid4())
    item = {
        'owner_id': 'ramomar',
        'record_id': item_id,
        'note': record_raw['note'],
        'amount': Decimal(record_raw['amount']),
        'date': record_raw['operation_date'],
        'raw': json.dumps(record_raw, default=str),
        'origin': 'BANORTE_EMAIL_SES',
    }

    gaston_table.put_item(Item=item)

    event = {
        'pathParameters': {
            'record_id': item_id,
        }
    }
    actual = record.get_record(event, context=None)
    expected_body = {
        'record': item,
    }
    expected = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(expected_body, indent=4, default=str)
    }

    assert actual['statusCode'] == expected['statusCode']
    assert actual['headers'] == expected['headers']
    assert json.loads(actual['body']) == json.loads(expected['body'])
