#!/bin/sh

echo "This script will empty your entire API Gateway stash."
read -p "Proceed (y/n)? " proceed

if [ $proceed = y ]
then
	for a in `aws apigateway get-rest-apis | grep id | cut -d "\"" -f 4`; do echo "* $a"; aws apigateway delete-rest-api --rest-api-id $a; done
fi

rm -f ~/.lambackup/awsapigateway
rm -rf ~/.lambackup/.api
