#!/usr/bin/env python3

"""
1484042050.248941835 RESET
1484042051.610615496
1484042052.779033567
FAIL ({"id": ["15917"]} | {"id": ["3966"]} | should be 15917)
"""

import sys

timestart = 0.0
timedelta = 0.0
counter = 0
iteration = 0
f = open(sys.argv[1])
lines = f.readlines()
for line in lines:
	line = line.strip().split(" ")
	#print(line)
	if "RESET" in line:
		timestart = float(line[0])
		counter = 0
		iteration += 1
	elif "FAIL" in line:
		print(iteration, counter // 2, timedelta)
	elif "SUCCESS" in line:
		pass
	else:
		timedelta = float(line[0]) - timestart
		counter += 1
