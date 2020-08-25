import praw, time, asyncio, json, re
from prawcore.exceptions import Forbidden
from praw.exceptions import APIException, ClientException
from sseclient import SSEClient
import core.constants as constants
import core.requestor as rq
import core.youtube as yt
import core.titleFinder as tf
from psaw import PushshiftAPI


class RedditClass:
    def __init__(self, client_id, client_secret, password, user_agent, username):
        self.reddit = praw.Reddit(
                    client_id = client_id,
                    client_secret = client_secret,
                    password = password,
                    user_agent = user_agent,
                    username = username)

        self.ps = PushshiftAPI(self.reddit)

        print("\'Reddit\' instance initialized!")


    # a function for crafting a comment to be sent to a user
    def commentConstructor(self, url):
        # initialize our head
        head = "Caution! "

        unUrl = rq.unDirect(url)
        id = yt.returnId(unUrl)
        title = yt.getVidTitle(id)
        confidence = tf.confidenceCheck(title)

        # this is cancer
        head += "This comment contains a youtube video that is a rickroll!" if confidence >=  80 else \
        "I have detected a YouTube video that appears to be a rickroll in this comment!" if 70 <=  confidence < 80 else \
        "The link in this comment is a YouTube video that may be a rickroll!" if 60 <=  confidence < 70 else None

        # initializing our body
        body = f" I am {confidence}% confident of this.\n\n"\
        f"The link's destination is [{unUrl}]({unUrl}), a YouTube video with a title of: \"{title}\".\n\n"

        # adding final shit
        body +=  "^(I am a Reddit bot with the sole purpose of preventing rickrolls. For me information on me and how I work, visit) ^[r/RickMeNot](https://www.reddit.com/r/RickMeNot). ^(Please consider supporting my development) ^[here.](https://cash.app/$AidanGinise)"

        # and finally, return it
        return f"{head}{body}"

    # this function checks a comment for a rickroll, and responds if needed
    def check(self, comment):
        print(True)

    # this function will handle checking the comments
    def commentStream(self):

        # getting the start time
        start = time.time() - 7200

        # defining our terms
        query = "http,https,youtube,www,com"
        fields = "author,subreddit,body,url,id"

        self.id = ""

        # getting a comments generator
        gen = list(self.ps.search_comments(after = int(start), after_id = self.id, q = query, filter = fields, limit = 100000))
        if len(gen) != 0:
            self.id = gen[-1].id
            for comment in gen:
                urls = rq.urlSniffer(comment.body)
                if not urls: continue
                for url in urls:
                    data = rq.unDirect(url)
                    if (data := yt.returnId(url)):
                        if (title := yt.getVidTitle(data)):
                            print(title)
                            print(f"{tf.confidenceCheck(title)}% sure I found a rickroll.")



red = RedditClass(constants.reddit_client_id, constants.reddit_client_secret, constants.reddit_password, constants.reddit_user_agent, constants.reddit_username)
