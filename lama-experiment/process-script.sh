#!/bin/sh

grep elapsed log-bench-100 | cut -d " " -f 3 | sed -e 's/elapsed//' | xargs -L1 python -c "import sys; x = sys.argv[1]; print int(x[0]) * 60 + int(x[2:4]) + int(x[5:7]) / 100.0" > log-bench-100.csv.1

grep \"id\" log-bench-100 | sed -r "s/\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?m//g" | xargs -d\\n -L1 python -c "import sys, json; x = json.loads(sys.argv[1]); print len(x['id'])-1" > log-bench-100.csv.2

paste -d " " log-bench-100.csv.1 log-bench-100.csv.2 > log-bench-100.csv

rm -f log-bench-100.csv.1 log-bench-100.csv.2
