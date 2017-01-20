#!/bin/sh
#
# Call: ./run-bench.sh > log-bench 2>&1

lbdir=../tools

for i in `seq 1 100`
do
	cat script | time $lbdir/lama 2>&1 | tee -a log-bench
done
