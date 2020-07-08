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

    # looking for urls
    urlList = re.findall(r'(https?://\S+)', url)

    if len(urlList) != 0:
        urlListFinal = [sub.replace(')', '') for sub in urlList]

        return urlListFinal

    else:
        return False

# a function used to decipher and decode urls that might redirect to something else, like a certain youtube video
def unDirect(url):

    #trying to make the request
    try:
        agentChoice = random.choice(agents)
        #print(agentChoice)

        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
        opener.addheaders = [('User-Agent', agentChoice)]
        request = opener.open(url)

        #checking if the returned url equals the given one
        if request.url == url:
            return 0

        if request.url != url:
            return request.url

    #excepting an error so the bot doesnt crash
    except Exception as e:
        #print(f"[REQUESTOR] Error! {e}")
        return False
