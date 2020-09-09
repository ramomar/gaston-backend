cognito_userpool_client_id=
cognito_username=
cognito_password=

aws cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH --client-id $cognito_userpool_client_id --auth-parameters USERNAME=$cognito_username,PASSWORD=$cognito_password
