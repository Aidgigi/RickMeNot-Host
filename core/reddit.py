import praw
from prawcore.exceptions import Forbidden
from praw.exceptions import APIException, ClientException
import core.constants as constants
import core.requestor as rq
import core.youtube as yt
import core.titleFinder as tf


class RedditClass:
    def __init__(self, client_id, client_secret, password, user_agent, username):
        self.reddit = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    password=password,
                    user_agent=user_agent,
                    username=username)

        print("\'Reddit\' instance initialized!")

    # a function for crafting a comment to be sent to a user
    def commentConstructor(self, urls):
        # initialize our head
        head = "Caution! "

        ul = len(urls)

        unUrls = [rq.unDirect(u) for u in urls if rq.unDirect(u)]
        ids = [yt.returnId(u) for u in unUrls if yt.returnId(u)]
        titles = [yt.getVidTitle(id) for id in ids if yt.getVidTitle(id)]
        confidences = [tf.confidenceCheck(t) for t in titles]

        # this is cancer
        head += f"This comment contains {ul} youtube videos which are likely to be rickrolls!" if ul > 1 else \
        "This comment contains a youtube video that is a rickroll!" if confidences[0] >= 85 else \
        "I have detected a YouTube video that appears to be a rickroll in this comment!" if 60 <= confidences[0] < 70 else \
        "The link in this comment is a YouTube video that may be a rickroll!" if 60 <= confidences[0] < 70 else None

        # initializing our body
        body = ""

        # if only one url
        if ul == 1:
            body += f" I am {confidences[0]}% confident of this.\n\n"\
            f"The link's destination is [{unUrls[0]}]({unUrls[0]}), a YouTube video with a title of: \"{titles[0]}\".\n\n"
        # this is also cancer
        else:
            body += "\n\nThese are as follows:\n\n"

            body += ''.join([f"[{unUrls[i]}]({unUrls[i]}) - Video with title {titles[i]}. I am {confidences[i]}%"\
            f" confident this is a rickroll.\n\n" for i in enumerate(urls)])

        # adding final shit
        body += "^(I am a Reddit bot with the sole purpose of preventing rickrolls. For me information on me and how I work, visit) ^r/RickMeNot. ^(Please consider donating to my creator) ^[here.](https://www.paypal.me/aidanginise1)"

        # and finally, return it
        return f"{head}\n\n{body}"

    def commentStream(self):
        subreddit = self.reddit.subreddit('mytestsubgoaway')

        for comment in subreddit.stream.comments(skip_existing=True):
            if comment.author != 'RickMeNot':
                try:
                    urls = rq.urlSniffer(comment.body)
                    if urls: comment.reply(self.commentConstructor(urls))
                except Exception as e:
                    err = "[STREAM] "

                    if isinstance(e, APIException):
                        err += "API error occurred:"
                    elif isinstance(e, ClientException):
                        err += "Client-side error occurred:"
                    elif isinstance(e, Forbidden):
                        err += f"Bot is banned from subreddit {comment.subreddit}:"
                    else:
                        err += "Unknown error occurred:"

                    err += f"{e}"

                    print(err)

red = RedditClass(constants.reddit_client_id, constants.reddit_client_secret, constants.reddit_password, constants.reddit_user_agent, constants.reddit_username)
