#!/bin/sh
#
# Call: ./run-restore.sh > log-restore 2>&1

lbdir=../tools

for file in `ls -1 $lbdir/refdata`
do
	for i in `seq 1 3`
	do
		echo $file
		time $lbdir/lambackup restore $lbdir/refdata/$file
	done
done

rm -f restored.*
