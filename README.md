Build:

`scripts/lambda-build.sh -f $FUNCTION_PATH`

Create:

`scripts/lambda-create.sh -n $FUNCTION_NAME -r $ROLE_ARN -p build/function.zip -h $NAMESPACE.FUNCTION_HANDLER`

Update:

`scripts/lambda-update.sh -n $FUNCTION_NAME -p build/function.zip`

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html