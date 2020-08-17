aws dynamodb create-table \
  --table gaston \
  --attribute-definitions \
  AttributeName=owner_id,AttributeType=S \
  AttributeName=record_id,AttributeType=S \
  --key-schema \
  AttributeName=owner_id,KeyType=HASH \
  AttributeName=record_id,KeyType=RANGE \
  --billing-mode PROVISIONED \
  --provisioned-throughput=ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --tags Key=gaston,Value=true
