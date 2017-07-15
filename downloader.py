#!/usr/bin/env python2

from __future__ import print_function
import lib
import json
import sys
import os
from updater import update

reddit = lib.makeDownloaderReddit()
data_config = lib.loadDataConfig()
subreddit = reddit.subreddit("All")

bucket = data_config.nowBucket()

def readComment(comment):
    if comment == None:
        return None
    return {
        "author": lib.readRedditor(comment.author),
        "body": comment.body,
        "timestamp": comment.created_utc,
        "subreddit": lib.readSubreddit(comment.subreddit),
        "id": comment.id,
        "fullname": comment.fullname,
    }

def prepFile():
    filename = data_config.nowFile()
    filedir = os.path.dirname(filename)
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    f = open(filename, "a")
    return f

def updatePastWeek():
    pass

f = prepFile()
try:
    for comment in subreddit.stream.comments():
        print(json.dumps(readComment(comment)), file=f)
        
        # check whether we've entered a new time bucket
        new_bucket = data_config.nowBucket()
        if new_bucket != bucket:
            f.close()
            bucket = new_bucket
            f = prepFile()
except KeyboardInterrupt:
    pass
#undent
