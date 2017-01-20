#!/usr/bin/env python3

"""
3 3 8.48299264907837
"""

import sys
import csv

mins = {}
maxs = {}
prevs = {}
bins = {}

f = open(sys.argv[1])
r = csv.reader(f, delimiter=" ")
prev = None
previt = None
for row in r:
	timing = float(row[2])
	it = row[1]
	if not it in mins or timing < mins[it]:
		mins[it] = timing
	if not it in maxs or timing > maxs[it]:
		maxs[it] = timing
	if row[0] == prev:
		if prev in prevs:
			prevs[prev].append(row[0])
		else:
			prevs[prev] = [previt, it]
	if not it in bins:
		bins[it] = 1
	else:
		bins[it] += 1
	prev = row[0]
	previt = it

for it in mins.keys():
	c = (maxs[it] + mins[it]) / 2
	h = c - mins[it]
	print(it, mins[it], maxs[it], c, h*2, bins[it])

print("DOUBLES", prevs)
