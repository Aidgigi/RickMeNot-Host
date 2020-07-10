import json
import urllib, urllib.request

def returnId(url):
    return url.split('watch?v=')[1][:11] if 'https://www.youtube.com/watch?v=' in url else False

#getting data from the youtube video
def getVidTitle(id):
    # defining the things to send
    params = {"format": "json", "url": f"https://www.youtube.com/watch?v={id}"}
    url = f"https://www.youtube.com/oembed?{urllib.parse.urlencode(params)}"

    try:
        return json.loads(urllib.request.urlopen(url).read().decode())['title']
    # excepting any errors
    except Exception as e:
        return False
