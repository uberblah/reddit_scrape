
import json
import praw
import time

reddit_config_name = "reddit_config.json"
data_config_name = "data_config.json"

# UTILITIES
def now():
    return int(time.time())

# CONFIG LOADING
def loadConfig(filename):
    with open(filename, "r") as f:
        return json.load(f)

class DataConfig:
    def __init__(self, path, interval, update, suffix):
        self.path = path
        self.interval = int(interval)
        self.update = int(update)
        self.suffix = suffix
    def timeBucket(self, t):
        t = int(t)
        return t - (t % self.interval)
    def timeFile(self, t):
        return self.path + "/" + time.strftime("%Y%m%d%H%M%S.json", time.gmtime(float(self.timeBucket(t))))
    def nowBucket(self):
        return self.timeBucket(now())
    def nowFile(self):
        return self.timeFile(now())
    def oldTime(self):
        return now() - self.update
    def oldBucket(self):
        return self.timeBucket(self.oldTime())
    def oldFile(self):
        return self.timeFile(self.oldTime())
    def oldFileNew(self):
        return self.path + "/" + time.strftime("%Y%m%d%H%M%S" + self.suffix + ".json", time.gmtime(float(self.oldBucket())))

def loadDataConfig():
    orig = loadConfig(data_config_name)
    return DataConfig(orig["output_directory"], orig["interval"], orig["update"], orig["suffix"])

# REDDIT CLIENT
def makeDownloaderReddit():
    config = loadConfig(reddit_config_name)
    return praw.Reddit(
        client_id=config["downloader_ident"],
        client_secret=config["downloader_secret"],
        user_agent=config["user_agent"]
    )

def makeUpdaterReddit():
    config = loadConfig(reddit_config_name)
    return praw.Reddit(
        client_id=config["updater_ident"],
        client_secret=config["updater_secret"],
        user_agent=config["user_agent"]
    )

# REDDIT MODELS
def readSubreddit(subreddit):
    if subreddit == None:
        return None
    return subreddit.display_name

def readRedditor(redditor):
    if redditor == None:
        return None
    return redditor.name
