import os
import json
import email
from email import policy
from decimal import Decimal
import dataclasses
import base64
import boto3
import botocore.exceptions
from banes import records
from banes import banorte_email

IS_AWS = bool(os.environ.get('AWS_EXECUTION_ENV', False))
OWNER_ID = os.environ.get('OWNER_ID', 'ramomar')


def _extra_amount_total(extra_amount):
    return Decimal(extra_amount.amount) + Decimal(extra_amount.tax)


def _calculate_total_amount(record):
    has_extra_amounts = record.type == records.EXPENSE_RECORD_TYPE and record.extra_amounts is not None
    extra_amount_total = sum([_extra_amount_total(ea) for ea in record.extra_amounts])\
        if has_extra_amounts else Decimal(0)

    return Decimal(record.amount) + extra_amount_total


def _make_item(record, record_id, date):
    total_amount = _calculate_total_amount(record)
    return {
        'owner_id': OWNER_ID,
        'record_id': record_id,
        'note': record.note,
        'amount': total_amount,
        'date': date,
        'raw': json.dumps(dataclasses.asdict(record), default=str),
        'origin': 'BANORTE_EMAIL_SES',
        'type': record.type,
    }


def handle(event, context):
    sns_event_content = json.loads(event['Records'][0]['Sns']['Message'])['content']
    email_content = email.message_from_bytes(base64.b64decode(sns_event_content), policy=policy.default).get_content()
    record = banorte_email.scrape(email_content)

    if record.type == records.ACCOUNT_OPERATION_TYPE:
        return {
            'success': False,
            'code': 'NotImplemented',
            'message':  'Insertion of account operation records not implemented',
        }

    try:
        client = boto3.resource('dynamodb', **{} if IS_AWS else {'endpoint_url': 'http://localhost:8000'})
        table = client.Table('gaston' if IS_AWS else 'gaston-local')
        item = _make_item(
            record,
            event['Records'][0]['Sns']['MessageId'],
            event['Records'][0]['Sns']['Timestamp'],
        )
        table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(record_id)',
        )

        return {
            'success': True,
            'record': item,
        }
    except botocore.exceptions.ClientError as error:
        error_details = error.response['Error']

        return {
            'success': False,
            'code': error_details['Code'],
            'message': error_details['Message'],
        }
