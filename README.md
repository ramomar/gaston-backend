# gaston-backend

This is a very simple backend for the [Gaston](https://github.com/ramomar/gaston) project.

<p align="center">
   <img src="https://user-images.githubusercontent.com/10622989/200975223-466dac5c-3beb-481c-8c69-c82a574c0e65.png" />
</p>


## API

Implemented via AWS API Gateway. Please note that `OPTIONS` requests are for CORS preflight requests.

### Records

`PUT /records/{record_id}/review`

`OPTIONS /records/{record_id}/review`

`GET /records/{record_id}`

`OPTIONS /records/{record_id}`

`GET /records`

`OPTIONS /records`

### Categories

`GET /categories`

`OPTIONS /categories`


## Functions

### List of functions

| Identifier | Description | Configuration variables |
|----------------------------------------------------|--------------------|---------------|
| `banorte_email.handle` | This function is triggered when an email from Banorte arrives via a SES driven SNS subscription. It parses the email using [banes](https://github.com/ramomar/banes) in order to create and insert a record in a DynamoDB table.| OWNER_ID |
| `record.get_records` | This function fetches all records. | OWNER_ID, GET_RECORDS_QUERY_LIMIT |
| `record.get_record` | This function gets a record by id. | OWNER_ID |
| `record_review.put_record_review` | This function creates a review for a given record. | OWNER_ID |
| `category.get_categories` | This function fetches all categories. Currently all the categories are hardcoded. | None |

### Configuration variables

- _OWNER_ID_: Sets the `owner_id` of the record when querying or creating.
- _GET_RECORDS_QUERY_LIMIT_: Sets the number of records returned in the response before paginating.

## Testing

The test suite is composed mainly of integration tests and it depends on [DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html) local.

In order to run the tests you should:

1. Start DynamoDB local:
`java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb`
2. Run: `pytest`.

## Scripts

The repository contains simple scripts to manage the functions.

**Build**

`scripts/lambda-build.sh -f $FUNCTION_PATH`

**Create**

`scripts/lambda-create.sh -n $FUNCTION_NAME -r $ROLE_ARN -p build/function.zip -h $NAMESPACE.FUNCTION_HANDLER`

**Update**

`scripts/lambda-update.sh -n $FUNCTION_NAME -p build/function.zip`
