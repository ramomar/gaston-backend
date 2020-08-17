function_name=
function_path=

bad_usage() {
  printf "Usage:\n%s: -n name -p path\n" $0
  exit 2
}

empty=1
while getopts n:p: params; do
  case $params in
  n) function_name="$OPTARG" ;;
  p) function_path="$OPTARG" ;;
  ?) bad_usage ;;
  esac
  empty=0
done

if [ $empty = 1 ]; then
  bad_usage
fi

aws lambda update-function-code \
  --function-name $function_name \
  --zip-file fileb://$function_path
