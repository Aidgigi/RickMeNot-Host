import json
from os import environ

# a veriable used for local testing
local = True

# the bot is running in the cloud
if not local:


    # reddit creds for praw
    reddit_username = environ['REDDIT_USERNAME']
    reddit_password = environ['REDDIT_PASSWORD']
    reddit_client_id = environ['REDDIT_CLIENT_ID']
    reddit_client_secret = environ['REDDIT_CLIENT_SECRET']
    reddit_user_agent = environ['REDDIT_USER_AGENT']

    # database creds
    database_username = environ['DATABASE_USERNAME']
    database_password = environ['DATABASE_PASSWORD']
    database_host = environ['DATABASE_HOST']
    database_port = environ['DATABASE_PORT']
    database_name = environ['DATABASE_NAME']


# the bot is running locally
if local:

    # opening and getting our creds
    credsFile = open("core/creds.json", "r")
    creds = json.load(creds)
    creds.close()

    # reddit creds for praw
    reddit_username = creds['reddit']['username']
    reddit_password = creds['reddit']['password']
    reddit_client_id = creds['reddit']['client_id']
    reddit_client_secret = creds['reddit']['client_secret']
    reddit_user_agent = creds['reddit']['user_agent']

    # database creds
    database_username = creds['database']['username']
    database_password = creds['database']['password']
    database_host = creds['database']['host']
    database_port = creds['database']['port']
    database_name = creds['database']['database']
