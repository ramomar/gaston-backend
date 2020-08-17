USERPOOL_ID=
USERNAME=
PASSWORD=

aws cognito-idp admin-create-user --user-pool-id $USERPOOL_ID --username $USERNAME
aws cognito-idp admin-set-user-password --user-pool-id $USERPOOL_ID --username $USERNAME --password $PASSWORD
