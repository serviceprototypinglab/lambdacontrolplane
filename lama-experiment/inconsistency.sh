#!/bin/bash
#
# call: ./inconsistency.sh | tee inconsistency-log

for x in `seq 1 200`
do
	echo `date +%s.%N` "RESET"
	randomvar=$RANDOM
	aws lambda update-function-configuration --function-name inconsistency --environment "Variables={CID=$randomvar}" >/dev/null

	# triggered/not triggered
	sleep 10

	for i in `seq 1 10`
	do
		date +%s.%N
		aws lambda invoke --function-name inconsistency _i2.json >/dev/null
		date +%s.%N
		aws lambda get-function-configuration --function-name inconsistency | python -c "import json, sys; x=json.loads(sys.stdin.read()); y={'id': x['Environment']['Variables']['CID'].split(';')}; print json.dumps(y)" > _i1.json
		echo >> _i2.json
		sum1=`md5sum _i1.json | cut -d " " -f 1`
		sum2=`md5sum _i2.json | cut -d " " -f 1`
		c1=`cat _i1.json`
		c2=`cat _i2.json`
		if [ $sum1 != $sum2 ]
		then
			echo "FAIL ($c1 | $c2 | should be $randomvar)"
		else
			echo "SUCCESS ($c1 | $c2 | $randomvar)"
		fi
	done
done

rm -f _i*.json
