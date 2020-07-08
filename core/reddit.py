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


    def testing(self):

        self.subredditStream = self.reddit.subreddit('mytestsubgoaway').stream.comments(skip_existing = True)

        for comment in self.subredditStream:
            urls = rq.urlSniffer(comment.body)
            if urls != False:
                for url in urls:
                    unUrl = rq.unDirect(url)
                    if unUrl != False:
                        id = yt.returnId(unUrl)
                        if id != False:
                            title = yt.getVidTitle(id)
                            if title != False:
                                print(title)
                                print(tf.confidenceCheck(title))






red = RedditClass(constants.reddit_client_id, constants.reddit_client_secret, constants.reddit_password, constants.reddit_user_agent, constants.reddit_username)
