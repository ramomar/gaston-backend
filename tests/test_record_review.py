import uuid
import json
from decimal import Decimal
from functions import record_review


def test_put_record_review_record_not_found():
    """it should fail when trying to update a record that doesn't exist"""
    event = {
        'pathParameters': {
            'record_id': str(uuid.uuid4()),
        },
        'body': json.dumps({
            'review': {
                'amount': 150,
                'date': '2017-03-19T05:29:02.700Z',
                'note': 'Cena',
                'category': 'Comida',
            },
        }),
    }
    actual = record_review.put_record_review(event, context=None)
    expected = {
        'statusCode': 400,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': {
            'code': 'ConditionalCheckFailedException',
            'message': 'The conditional request failed',
        }
    }

    assert actual == expected


def test_put_record_review_no_review():
    """it should fail if there is no review"""
    event = {
        'pathParameters': {
            'record_id': str(uuid.uuid4()),
        },
        'body': None,
    }
    actual = record_review.put_record_review(event, context=None)
    expected = {
        'statusCode': 400,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': {
            'code': 'NoReview',
            'message': 'Review is not present',
        }
    }

    assert actual == expected


def test_put_record_review_record_found(gaston_table):
    """it should update the record"""
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
        'raw': json.dumps(record_raw, default=str, ensure_ascii=False),
        'origin': 'BANORTE_EMAIL_SES',
    }

    gaston_table.put_item(Item=item)

    event = {
        'pathParameters': {
            'record_id': item_id,
        },
        'body': json.dumps({
            'review': {
                'amount': 655,
                'date': '2020-07-19T18:56:00.000Z',
                'note': 'Curso de musica',
                'category': 'Educación'
            },
        }),
    }
    actual = record_review.put_record_review(event, context=None)
    expected_record = {
        'owner_id': 'ramomar',
        'record_id': item_id,
        'note': record_raw['note'],
        'amount': record_raw['amount'],
        'date': record_raw['operation_date'],
        'raw': json.dumps(record_raw, default=str, ensure_ascii=False),
        'origin': 'BANORTE_EMAIL_SES',
    }
    expected_review = {
        'amount': '655',
        'date': '2020-07-19T18:56:00.000Z',
        'note': 'Curso de musica',
        'category': 'Educación',
    }
    expected = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': {
            'record': json.dumps(expected_record, indent=4, default=str),
            'review': json.dumps(expected_review, indent=4, default=str),
        }
    }

    assert actual['statusCode'] == expected['statusCode']
    assert actual['headers'] == expected['headers']
    assert json.loads(actual['body'])['record'] == json.loads(expected['body']['record'])
