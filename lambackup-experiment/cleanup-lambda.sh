#!/bin/sh

echo "This script will empty your entire Lambda stash."
read -p "Proceed (y/n)? " proceed

if [ $proceed = y ]
then
	for f in `aws lambda list-functions | grep FunctionName | cut -d "\"" -f 4`; do echo "* $f"; aws lambda delete-function --function-name $f; done
fi
