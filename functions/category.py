import json

CATEGORIES = [
    {'name': 'Comida'},
    {'name': 'Renta'},
    {'name': 'Salud'},
]


def get_categories(event, context):
    result = {
        'categories': CATEGORIES,
    }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(result, indent=4, default=str),
    }