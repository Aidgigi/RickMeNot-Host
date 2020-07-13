import praw, time, asyncio
from core.pushshift import getComments
from prawcore.exceptions import Forbidden
from praw.exceptions import APIException, ClientException
import core.constants as constants
import core.requestor as rq
import core.youtube as yt
import core.titleFinder as tf


class RedditClass:
    def __init__(self, client_id, client_secret, password, user_agent, username):
        self.reddit = praw.Reddit(
                    client_id = client_id,
                    client_secret = client_secret,
                    password = password,
                    user_agent = user_agent,
                    username = username)

        print("\'Reddit\' instance initialized!")


    # a function for crafting a comment to be sent to a user
    def commentConstructor(self, urls):
        # initialize our head
        self.head = "Caution! "

        self.ul = len(urls)

        self.unUrls = [rq.unDirect(u) for u in urls if rq.unDirect(u)]
        self.ids = [yt.returnId(u) for u in self.unUrls if yt.returnId(u)]
        self.titles = [yt.getVidTitle(id) for id in self.ids if yt.getVidTitle(id)]
        self.confidences = [tf.confidenceCheck(t) for t in self.titles]

        # this is cancer
        self.head +=  f"This comment contains {ul} youtube videos which are likely to be rickrolls!" if self.ul > 1 else \
        "This comment contains a youtube video that is a rickroll!" if self.confidences[0] >=  85 else \
        "I have detected a YouTube video that appears to be a rickroll in this comment!" if 60 <=  self.confidences[0] < 70 else \
        "The link in this comment is a YouTube video that may be a rickroll!" if 60 <=  self.confidences[0] < 70 else None

        # initializing our body
        self.body = ""

        # if only one url
        if self.ul ==  1:
            self.body +=  f" I am {self.confidences[0]}% confident of this.\n\n"\
            f"The link's destination is [{self.unUrls[0]}]({self.unUrls[0]}), a YouTube video with a title of: \"{self.titles[0]}\".\n\n"
        # this is also cancer
        else:
            self.body +=  "\n\nThese are as follows:\n\n"

            self.body +=  ''.join([f"[{self.unUrls[i]}]({self.unUrls[i]}) - Video with title {self.titles[i]}. I am {self.confidences[i]}%"\
            f" confident this is a rickroll.\n\n" for i in enumerate(self.urls)])

        # adding final shit
        self.body +=  "^(I am a Reddit bot with the sole purpose of preventing rickrolls. For me information on me and how I work, visit) ^[r/RickMeNot](https://www.reddit.com/r/RickMeNot). ^(Please consider donating to my creators) ^[here.](https://www.paypal.me/aidanginise1)"

        # and finally, return it
        return f"{self.head}{self.body}"

    # this function checks a comment for a rickroll, and responds if needed
    def check(self, comment):
        print(True)

    # this function will handle checking the comments
    def commentStream(self, freq):

        # defining our subreddit and submissions object
        self.subreddit = self.reddit.subreddit('all')







red = RedditClass(constants.reddit_client_id, constants.reddit_client_secret, constants.reddit_password, constants.reddit_user_agent, constants.reddit_username)
