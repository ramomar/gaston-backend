function_name=
function_role=
function_path=
function_handler=

bad_usage() {
  printf "Usage:\n%s: -n name -r role arn -p path -h handler\n" $0
  exit 2
}

empty=1
while getopts n:r:p:h: params; do
  case $params in
  n) function_name="$OPTARG" ;;
  r) function_role="$OPTARG" ;;
  p) function_path="$OPTARG" ;;
  h) function_handler="$OPTARG" ;;
  ?) bad_usage ;;
  esac
  empty=0
done

if [ $empty = 1 ]; then
  bad_usage
fi

aws lambda create-function \
  --function-name $function_name \
  --zip-file fileb://$function_path \
  --handler $function_handler \
  --runtime python3.7 \
  --role $function_role \
  --tags "gaston=true"
