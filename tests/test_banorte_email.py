import json
from decimal import Decimal
import dataclasses
from functions import banorte_email
import banes.records as records

EVENT_PATH = 'handle-banorte-email-event.json'


def test_handle_event(load_event):
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
            'bank': 'BANCO',
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
            'type': 'EXPENSE',
        }
    }
    actual = banorte_email.handle(event, context=None)

    actual['record']['raw'] = json.loads(actual['record']['raw'])

    assert actual == expected


def test_handle_record_is_account_operation_record(mocker, load_event):
    """it should raise an exception when the record is an account operation record"""
    event = load_event(EVENT_PATH)
    account_operation_record = records.AccountOperationRecord(
        source='EMAIL_CHANGED',
        type=records.ACCOUNT_OPERATION_TYPE,
        note='El email se ha actualizado con exito | viejo_email@mail.com | nuevo_email@mail.com',
    )

    mocker.patch('banes.banorte_email.scrape', return_value=account_operation_record)

    expected = {
        'success': False,
        'code': 'NotImplemented',
        'message': 'Insertion of account operation records not implemented'
    }
    actual = banorte_email.handle(event, None)

    assert actual == expected


def test_handle_record_is_stored(load_event, gaston_table):
    """it should store a record"""
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
            'bank': 'BANCO',
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
        'type': 'EXPENSE',
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


def test__make_item_expense():
    """it should create an item from an expense record"""
    expense = records.ExpenseRecord(
        source='TEST',
        type=records.EXPENSE_RECORD_TYPE,
        note='Test record',
        amount='10',
        extra_amounts=[
            records.ExtraAmount(
                name='fee',
                amount='5',
                tax='5'
            ),
            records.ExtraAmount(
                name='another fee',
                amount='5',
                tax='5',
            ),
        ],
    )
    record_id = '8203565b-41a0-46bc-bd63-809eefbf71f9'
    date = '1609007911591'
    expected = {
        'owner_id': 'ramomar',
        'record_id': record_id,
        'note': 'Test record',
        'amount': Decimal('30'),
        'date': date,
        'raw': json.dumps(dataclasses.asdict(expense), default=str),
        'origin': 'BANORTE_EMAIL_SES',
        'type': 'EXPENSE',
    }
    actual = banorte_email._make_item(expense, record_id, date)

    assert expected == actual


def test__make_item_income():
    """it should create an item from an income record"""
    income = records.IncomeRecord(
        source='TEST',
        type=records.INCOME_RECORD_TYPE,
        note='Pago de la comida',
        amount='10',
    )
    record_id = '8203565b-41a0-46bc-bd63-809eefbf71f9'
    date = '1609007911591'
    expected = {
        'owner_id': 'ramomar',
        'record_id': record_id,
        'note': 'Pago de la comida',
        'amount': Decimal('10'),
        'date': date,
        'raw': json.dumps(dataclasses.asdict(income), default=str),
        'origin': 'BANORTE_EMAIL_SES',
        'type': 'INCOME',
    }
    actual = banorte_email._make_item(income, record_id, date)

    assert expected == actual


def test__calculate_total_amount():
    """it should compute the total amount correctly"""
    record = records.ExpenseRecord(
        source='TEST',
        type=records.EXPENSE_RECORD_TYPE,
        note='Test record',
        amount='10',
        extra_amounts=[
            records.ExtraAmount(
                name='fee',
                amount='5',
                tax='5',
            ),
            records.ExtraAmount(
                name='another fee',
                amount='5',
                tax='5',
            ),
        ],
    )
    expected = Decimal(30)
    actual = banorte_email._calculate_total_amount(record)

    assert actual == expected
