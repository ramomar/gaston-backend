**Build**

`scripts/lambda-build.sh -f $FUNCTION_PATH`

**Create**

`scripts/lambda-create.sh -n $FUNCTION_NAME -r $ROLE_ARN -p build/function.zip -h $NAMESPACE.FUNCTION_HANDLER`

**Update**

`scripts/lambda-update.sh -n $FUNCTION_NAME -p build/function.zip`

**Test**

The test suite is composed of integration tests and id depends on [DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html) local.

1. Start DynamoDB local:
`java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb`
2. Run: `pytest`.
