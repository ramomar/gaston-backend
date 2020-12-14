import json
from functions import category


def test_get_categories():
    """it should return a list with categories"""
    event = {}
    actual = category.get_categories(event, context=None)
    expected_body = {
        'categories': [
            {'name': 'Comida'},
            {'name': 'Renta'},
            {'name': 'Salud'},
        ]
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
