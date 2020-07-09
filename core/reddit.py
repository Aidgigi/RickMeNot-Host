import core.constants as constants
import core.requestor as rq
import core.youtube as yt
import core.titleFinder as tf
import praw
from prawcore.exceptions import RequestException, Forbidden, ServerError
from praw.exceptions import APIException, ClientException

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
    def commentConstructor(self, comment, url, title, confidence, multipleFlag):

        # this function will use different arguments like the url, confidence level, and more to create a comment to be sent to the rickroller

        # checking if the link has multiple rick rolls
        if multipleFlag == False:

            # checking the confidence level and creating a fitting comment
            if confidence >= 85:
                head = "Caution! This comment contains a YouTube video that is a rickroll! "

            if confidence >= 70 and confidence < 85:
                head = "Caution! I have detected a YouTube video that appears to be a rickroll in this comment! "

            if confidence >= 60 and confidence < 70:
                head = "Caution! The link in this comment is a YouTube video that may be a rickroll! "

            # line expressing certainty
            certainty = f"I am {confidence}% confident of this."
            # showing where the link redirects
            linkStatement = f"\n\nThe link's destination is [{url}]({url}), a YouTube video with a title of: \"{title}\"."

            footnote = f"\n\n^(I am a Reddit bot with the sole purpose of preventing rickrolls. For me information on me and how I work, visit) ^[r/RickMeNot.](https://reddit.com/r/RickMeNot) ^( Please consider donating to my creator) ^[here.](https://www.paypal.me/aidanginise1)"

            return head + certainty + linkStatement + footnote


        # multipleflag is true
        if multipleFlag == True:
            print(True)


    def testing(self):

        self.subreddit = self.reddit.subreddit('mytestsubgoaway')

        for comment in self.subreddit.stream.comments(skip_existing = True):
            try:
                if comment.author != 'RickMeNot':
                    urls = rq.urlSniffer(comment.body)
                    if urls != False:
                        for url in urls:
                            unUrl = rq.unDirect(url)
                            if unUrl != False:
                                id = yt.returnId(unUrl)
                                if id != False:
                                    title = yt.getVidTitle(id)
                                    if title != False:
                                        comment.reply(self.commentConstructor(comment, unUrl, title, tf.confidenceCheck(title), False))

            except Exception as e:
                print(e)

red = RedditClass(constants.reddit_client_id, constants.reddit_client_secret, constants.reddit_password, constants.reddit_user_agent, constants.reddit_username)
