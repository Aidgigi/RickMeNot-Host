import requests
import time
from datetime import datetime, timedelta, timezone


endEpoch = int((datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(hours=4)).timestamp())


def findComments():
    # defining some things
    previousEpoch = int(datetime.utcnow().timestamp())
    url = "https://api.pushshift.io/reddit/comment/search?&limit=1000&sort=desc&q=http|https|youtube&before="
    breakOut = False

    # the loop
    while True:
        newUrl = url + str(previousEpoch)
        json = requests.get(newUrl, headers = {'User-Agent': "RickMeNot v1.0.3 by u/Aidgigi"})
        objects = json.json()['data']
        if len(objects) == 0:
            break
        for comment in objects:
            previousEpoch = comment['created_utc'] - 1

            print(f"{datetime.utcnow().timestamp() - comment['created_utc']} seconds old")

            if previousEpoch < endEpoch:
                breakOut = True
                break
        if breakOut:
            break
