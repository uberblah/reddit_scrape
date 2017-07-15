#!/usr/bin/env python2

import lib
import json
import signal

reddit = lib.makeDownloaderReddit()
subreddit = reddit.subreddit("All")

# the print loop is wrapped in a try to avoid interrupting a print
try:
    for comment in subreddit.stream.comments():
        print(comment.__dict__.keys())
        #print(json.dumps(lib.readComment(comment)))
#undent
except KeyboardInterrupt:
    pass
