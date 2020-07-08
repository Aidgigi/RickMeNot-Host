import urllib.request
import json
import urllib

def returnId(url):

    #making sure this is a youtube video
    if 'https://www.youtube.com/watch?v=' in url:
        idString = url.split('watch?v=')[1]

        if '&feature=' in idString:
            return idString.split('&feature=')[0]
        else:
            return idString
    #isnt a youtube video
    if 'https://www.youtube.com/watch?v=' not in url:
        return False

#getting data from the youtube video
def getVidTitle(id):
    # defining the things to send
    params = {"format": "json", "url": f"https://www.youtube.com/watch?v={id}"}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        print(data['title'])
