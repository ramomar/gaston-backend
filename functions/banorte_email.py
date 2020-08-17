import os
import json
import email
from email import policy
from decimal import Decimal
import dataclasses
import base64
import boto3
import botocore.exceptions
from banes.records import EXPENSE_RECORD_TYPE
from banes import banorte_email

OWNER_ID = os.environ.get('OWNER_ID', 'ramomar')
IS_AWS = os.environ.get('AWS_EXECUTION_ENV', False)


def _extra_amount_total(extra_amount):
    return Decimal(extra_amount.amount) + Decimal(extra_amount.tax)


def _calculate_total_amount(record):
    amounts = record.extra_amounts
    extra_amount_total = sum([_extra_amount_total(ea) for ea in amounts]) if amounts is not None else 0

    return Decimal(record.amount) + extra_amount_total


def handle(event, context):
    sns_event_content = json.loads(
        event['Records'][0]['Sns']['Message'])['content']
    email_content = email.message_from_bytes(base64.b64decode(sns_event_content), policy=policy.default).get_content()
    record = banorte_email.scrape(email_content)

    if record.type == EXPENSE_RECORD_TYPE:
        client = boto3.resource('dynamodb',
                                **{} if IS_AWS else {'endpoint_url': 'http://localhost:8000'})
        table = client.Table('gaston' if IS_AWS else 'gaston-local')
        total_amount = _calculate_total_amount(record)
        item = {
            'owner_id': OWNER_ID,
            'record_id': event['Records'][0]['Sns']['MessageId'],
            'note': record.note,
            'amount': total_amount,
            'date': event['Records'][0]['Sns']['Timestamp'],
            'raw': json.dumps(dataclasses.asdict(record), default=str, ensure_ascii=False)
        }

        try:
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
