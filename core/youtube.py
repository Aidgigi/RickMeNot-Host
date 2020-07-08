import requests
from bs4 import BeautifulSoup as bs
import time
import simplejson

#getting data from the youtube video
def getVidInfo(url):

    #timing shit
    timeStart = time.time()

    id = 'KQEOBZLx-Z8'
    url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % id

    json = simplejson.load(urllib.urlopen(url))

    title = json['entry']['title']['$t']
    author = json['entry']['author'][0]['name']

    timeEnd = time.time()
    print(f"That took {timeEnd - timeStart} seconds.")

    return "id:%s\nauthor:%s\ntitle:%s" % (id, author, title)
