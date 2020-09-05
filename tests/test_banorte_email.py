import json
from decimal import Decimal
from functions import banorte_email
from banes.records import ExpenseRecord, ExtraAmount, EXPENSE_RECORD_TYPE

EVENT_PATH = 'handle-banorte-email-event.json'


def test_handle(load_event):
    """it should handle correctly a SNS event"""
    event = load_event(EVENT_PATH)
    expense_json = {
        'source': 'FAST_TRANSFER_EMAIL',
        'type': 'EXPENSE',
        'note': 'Transferencias Rápidas | P',
        'amount': '650.00',
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
    expected = {
        'success': True,
        'record': {
            'owner_id': 'ramomar',
            'record_id': event['Records'][0]['Sns']['MessageId'],
            'note': 'Transferencias Rápidas | P',
            'date': '2020-07-27T23:57:00.335Z',
            'amount': Decimal('653.48'),
            'raw': expense_json,
            'origin': 'BANORTE_EMAIL_SES',
        }
    }
    actual = banorte_email.handle(event, context=None)

    actual['record']['raw'] = json.loads(actual['record']['raw'])

    assert actual == expected


def test_handle_record_is_stored(load_event, gaston_table):
    "it should store a record"
    event = load_event(EVENT_PATH)
    record_key = {
        'owner_id': 'ramomar',
        'record_id': event['Records'][0]['Sns']['MessageId'],
    }
    expense_json = {
        'source': 'FAST_TRANSFER_EMAIL',
        'type': 'EXPENSE',
        'note': 'Transferencias Rápidas | P',
        'amount': '650.00',
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
            },
        ],
    }
    expected = {
        'owner_id': 'ramomar',
        'record_id': event['Records'][0]['Sns']['MessageId'],
        'note': 'Transferencias Rápidas | P',
        'date': '2020-07-27T23:57:00.335Z',
        'amount': Decimal('653.48'),
        'raw': expense_json,
        'origin': 'BANORTE_EMAIL_SES',
    }

    banorte_email.handle(event, None)

    actual = gaston_table.get_item(Key=record_key)['Item']

    actual['raw'] = json.loads(actual['raw'])

    assert actual == expected


def test_handle_idempotence(load_event):
    """it should not store the same record twice"""
    event = load_event(EVENT_PATH)

    expected = {
        'success': False,
        'code': 'ConditionalCheckFailedException',
        'message': 'The conditional request failed',
    }

    banorte_email.handle(event, context=None)

    actual = banorte_email.handle(event, context=None)

    assert actual == expected


def test__calculate_total_amount(load_event):
    """it should compute the total amount correctly"""
    event = load_event(EVENT_PATH)

    record = ExpenseRecord(
        source='TEST',
        type=EXPENSE_RECORD_TYPE,
        note='Test record',
        amount='10',
        extra_amounts=[
            ExtraAmount(
                name='fee',
                amount='5',
                tax='5'
            ),
            ExtraAmount(
                name='another fee',
                amount='5',
                tax='5',
            ),
        ],
    )

    expected = Decimal(30)

    actual = banorte_email._calculate_total_amount(record)

    assert actual == expected
