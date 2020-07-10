import urllib.request
import random
import json
import re

# getting a list of user agents to use
agentFile = open("core/userAgents.json", "r")
agentsData = json.load(agentFile)
agentFile.close()

agents = agentsData['agents']


# a function that will check if a string has a url in it, and return that url
def urlSniffer(url):
    urlList = [sub.replace(')', '') for sub in re.findall(r'(https?://\S+)', url)]
    
    return urlList if len(urlList) > 0 else False

# a function used to decipher and decode urls that might redirect to something else, like a certain youtube video
def unDirect(url):
    #trying to make the request
    try:
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
        opener.addheaders = [('User-Agent', random.choice(agents))]
        request = opener.open(url)

        return url if request.url == url else request.url
    #excepting an error so the bot doesnt crash
    except Exception:
        return False
