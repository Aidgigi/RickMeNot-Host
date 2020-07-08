import urllib.request
import json
import urllib
import pprint

def returnId(url):

    #making sure this is a youtube video
    if 'https://www.youtube.com/watch?v' in url:

        idString = url.split('watch?v=')[1]

        if '&feature=' in idString:
            return idStrinf.split('&feature=')[0]

        else:
            return idString

    #isnt a youtube video
    if 'https://www.youtube.com/watch?v' not in url:
        return False

#getting data from the youtube video
def getVidTitle(url):
