#!/usr/bin/env python2

from __future__ import print_function
import csv
import json
import sys

if len(sys.argv) < 3:
    print("oh no you didn't!", file=sys.stderr)
    sys.exit(1)
#undent

column_names = set()
print("getting column names")
with open(sys.argv[1], "r") as f:
    for line in f:
        row = json.loads(line)
        for k in row.keys():
            column_names.add(k)
#undent
print("writing data")
column_list = list(column_names)
with open(sys.argv[1], "r") as f:
    with open(sys.argv[2], "w") as g:
        writer = csv.DictWriter(g, column_list)
        writer.writeheader()
        for line in f:
            row = json.loads(line)
            for k in row:
                field = row[k]
                if type(field) == unicode:
                    row[k] = field.encode("ascii", "ignore")
            writer.writerow(row)
#undent
