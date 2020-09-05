# gaston-backend

This is the backend for the [Gaston](https://github.com/ramomar/gaston) project.


### Functions

| Identifier                                               | Description        | Configuration |
|----------------------------------------------------|--------------------|---------------|
| `banorte_email.handle` | This function is triggered when an email from Banorte arrives. It parses the email using [banes](https://github.com/ramomar/banes) in order to create and insert a record in a DynamoDB table.| OWNER_ID |
| `record.get_records` | This function fetches all records. | OWNER_ID |
| `record.get_record` | This function gets a record by id. | OWNER_ID |
| `record_review.post_review` | This function creates a review for a given record. | OWNER_ID |

### Testing

The test suite is composed of integration tests mainly and it depends on [DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html) local.

1. Start DynamoDB local:
`java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb`
2. Run: `pytest`.

### Deploying

**Build**

`scripts/lambda-build.sh -f $FUNCTION_PATH`

**Create**

`scripts/lambda-create.sh -n $FUNCTION_NAME -r $ROLE_ARN -p build/function.zip -h $NAMESPACE.FUNCTION_HANDLER`

**Update**

`scripts/lambda-update.sh -n $FUNCTION_NAME -p build/function.zip`