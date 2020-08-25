import requests
import time
import re
import json
from sseclient import SSEClient
from datetime import datetime, timedelta, timezone


prev = ""

def returnBatch():
    global prev
    # defining some things
    previousEpoch = int(datetime.utcnow().replace(tzinfo = timezone.utc).timestamp())
    terms = "http|https|youtube"
    after = "1h"
    filter = "author,id,body,subreddit,created_utc"
    sort = "created_utc:asc"
    url = f"https://api.pushshift.io/reddit/comment/search/?q={terms}&sort={sort}&after={after}&filter={filter}"
    breakOut = False

    json = requests.get(url, headers = {'User-Agent': "RickMeNot v1.0.3 by u/Aidgigi"})
    objects = json.json()['data']
    if len(objects) == 0:
        return 0
    for comment in objects:
        print(f"{comment}\n")

    lc = objects[-1]
    print(f"Last comment is {int(datetime.utcnow().timestamp()) - int(lc['created_utc'])} seconds old.")




def findComments2():

    # defining some things
    url = "http://stream.pushshift.io/?type=comments&filter="
    params = {'Accept-Encoding': 'gzip', 'User-Agent': 'RickMeNot v1.0.3 by u/Aidgigi'}
    fields = 'body,id,link_id,created_utc'
    comments = SSEClient(url + fields, params = params)

    for comment in comments:
        try:
            comment = json.loads(comment.data)
            urls = re.findall(r'(https?://\S+)', comment['body'])
            if len(urls) != 0:
                print(comment['body'] + '\n')

        except Exception as e:
            print(e)
