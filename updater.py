#!/usr/bin/env python

from __future__ import print_function
import lib
import praw
import sys
import os
import json

def readUpdate(comment):
    if comment == None:
        return None
    return {
        "score": comment.score,
        "ups": comment.ups,
        "downs": comment.downs,
        "deleted": False,
        "report_reasons": comment.report_reasons,
        "num_reports": comment.num_reports,
    }

def updateBatch(reddit, comments):
    fullnames = comments.keys()
    requests = reddit.info(fullnames)
    for pair in zip(fullnames, requests):
        fullname = pair[0]
        request = pair[1]
        try:
            updated = readUpdate(request.refresh())
        except praw.exceptions.ClientException as e:
            if str(e) == "Comment has been deleted":
                updated = {"deleted": True}
            else:
                updated = {"update_error": str(e)}
        original = comments[fullname]
        for k in updated:
            original[k] = updated[k]
        comments[fullname] = original
    return comments

def update(infile, outfile, printHashes):
    reddit = lib.makeUpdaterReddit()

    g = open(outfile, "a")

    try:
        with open(infile, "r") as f:
            comments = {}
            count = 0
            for line in f:
                comment = json.loads(line)
                comments[comment["fullname"]] = comment
                count += 1
                if count >= 100:
                    comments = updateBatch(reddit, comments)
                    for k in comments:
                        print(json.dumps(comments[k]), file=g)
                        continue
                    del comments
                    comments = {}
                    count = 0
                    if printHashes:
                        sys.stdout.write("#")
                        sys.stdout.flush()
        comments = updateBatch(reddit, comments)
        for k in comments:
            print(json.dumps(comments[k]), file=g)
    except KeyboardInterrupt:
        pass

#undent

def main():
    data_config = lib.loadDataConfig()
    inFile = data_config.oldFile()
    if not os.path.exists(inFile):
        print("No input file \"" + inFile + "\", therefore nothing to do", file=sys.stderr)
        sys.exit(1)
    outFile = data_config.oldFileNew()
    update(inFile, outFile, False)
#undent

if __name__ == "__main__":
    main()
#undent
