#!/bin/sh
#
# Call: ./run-backup.sh > log-backup 2>&1

lbdir=../tools

for file in `ls -1 $lbdir/refdata`
do
	for i in `seq 1 3`
	do
		echo $file
		time $lbdir/lambackup backup $lbdir/refdata/$file
	done
done
