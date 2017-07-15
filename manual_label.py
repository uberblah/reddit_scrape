#!/usr/bin/env python2

from __future__ import print_function
import sys
import os
import json

def manual_label(entry, field):
    print("============================================")
    print("--------------------------------------------")
    print(json.dumps(entry, indent=4))
    raw_label = raw_input(field + "? (y/n) ")
    entry[field] = raw_label.lower() == "y"
    return entry

def load_already_labeled(filename):
    try:
        labeled_raw = []
        with open(filename, "r") as f:
            for line in f:
                labeled_raw.append(json.loads(line))
    except IOError:
        pass
    return {item["fullname"]: item for item in labeled_raw}

def main():
    if len(sys.argv) < 3:
        print("./manual_label.py <infile.json> <outfile.json> <field>", file=sys.stderr)
        sys.exit(1)
    #undent

    infile = sys.argv[1]
    outfile = sys.argv[2]
    field = sys.argv[3]

    labeled = load_already_labeled(outfile)

    try:
        with open(infile, "r") as f, open(outfile, "a") as g:
            for line in f:
                entry = json.loads(line)
                if entry["fullname"] in labeled:
                    continue
                print(json.dumps(manual_label(entry, field)), file=g)
    except KeyboardInterrupt:
        pass # catch keyboard interrupts to prevent output truncation

if __name__ == "__main__":
    main()
