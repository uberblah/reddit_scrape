#!/usr/bin/env python2

from __future__ import print_function
import sys
import os
import json

def manual_label(entry):
    print("============================================")
    print("--------------------------------------------")
    print(json.dumps(entry, indent=4))
    raw_label = raw_input("O? > ")
    entry["offensive"] = raw_label.lower() == "o"
    return entry

def main():
    if len(sys.argv) < 3:
        print("oh no you didn't!", file=sys.stderr)
        sys.exit(1)
    #undent

    infile = sys.argv[1]
    outfile = sys.argv[2]

    try:
        with open(infile, "r") as f, open(outfile, "a") as g:
            for line in f:
                entry = json.loads(line)
                print(json.dumps(manual_label(entry)), file=g)
    except KeyboardInterrupt:
        pass # catch keyboard interrupts to prevent output truncation

if __name__ == "__main__":
    main()
