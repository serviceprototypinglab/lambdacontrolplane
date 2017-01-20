#!/usr/bin/env python3

"""
16.99 10
"""

import sys
import csv

deltas = []

f = open(sys.argv[1])
r = csv.reader(f, delimiter=" ")
prev = None
previt = None
for row in r:
	deltas.append(float(row[0]))

print(len(deltas), "values")
print("min:", min(deltas))
print("max:", max(deltas))
print("avg:", sum(deltas) / len(deltas))
