set -e

dir=$(pwd)

path=

bad_usage() {
    printf "Usage:\n%s: -f path\n" $0
    exit 2
}

empty=1
while getopts f: params; do
    case $params in
    f) path="$OPTARG" ;;
    ?) bad_usage ;;
    esac
    empty=0
done

if [ $empty = 1 ]; then
    bad_usage
fi

# Prepare work directory
rm -rf $dir/build
mkdir $dir/build

# Copy function
cp $path $dir/build

# Install dependencies
pip install . --target $dir/build

# Zip function sources
cd $dir/build
zip -r9 $dir/build/function.zip .

echo -e "Done"
