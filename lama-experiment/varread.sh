#!/bin/sh

for i in `seq 1 100`
do
	aws lambda get-function-configuration --function-name database | python -c "import json, sys; x=json.loads(sys.stdin.read()); print x['Environment']['Variables']"
	sleep 1
done
