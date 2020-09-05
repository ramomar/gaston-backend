import json
import uuid
from decimal import Decimal
from functions import record


def test_get_records_empty():
    """it should return an empty list when there are no records"""
    event = {}
    actual = record.get_records(event, None)
    expected_body = {
        'records': []
    }
    expected = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
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
        'raw': json.dumps(record_raw, default=str, ensure_ascii=False),
        'origin': 'BANORTE_EMAIL_SES',
    }

    gaston_table.put_item(Item=item)

    event = {}
    actual = record.get_records(event, None)
    expected_body = {
        'records': [
            item,
        ]
    }
    expected = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps(expected_body, indent=4, default=str)
    }

    assert actual['statusCode'] == expected['statusCode']
    assert actual['headers'] == expected['headers']
    assert json.loads(actual['body']) == json.loads(expected['body'])
