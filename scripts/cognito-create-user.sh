cognito_userpool_id=
cognito_username=
cognito_password=

aws cognito-idp admin-create-user --user-pool-id $cognito_userpool_id --cognito_username $cognito_username
aws cognito-idp admin-set-user-password --user-pool-id $cognito_userpool_id --username $cognito_username --password $cognito_password --permanent
