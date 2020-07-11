from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from core.models import Base
from core.models import *
from core.helpers import unique, countOcc, dictSort
import core.constants as const
import json


#"""This class represents the main db, and everything it may need to do"""
class mainDB:

    #our init function, to get everything started
    #initializing the database class
    def __init__(self, username, password, host, port, database):

        # a string used for logging in
        self.uri = f"postgresql://{username}:{password}@{host}:{str(port)}/{database}"

        #this logs into and creates a database instance
        self.engine = create_engine(self.uri)
        self.db = scoped_session(sessionmaker(bind = self.engine))
        self.meta = MetaData(self.engine)

        #making a base
        self.Base = Base


    #a function for creating the tables
    def createTabs(self):

        #reflecting the db locally
        self.meta.reflect(bind = self.engine)

        #checking to make sure that the tables dont exist, if a table doesnt exist, it's made
        self.Base.metadata.create_all(self.engine, self.Base.metadata.tables.values(), checkfirst = True)

        print('[DATABASE] Tables Created!')
        return True


    # a function for logging a rickroll
    def logRoll(self, user, target, subreddit, url):

        #reflecting the db locally
        self.meta.reflect(bind = self.engine)

        self.db.add(RollerLog(
            roller = user,
            target = target
        ))

        self.db.add(SubredditLog(
            subreddit = subreddit
        ))

        self.db.add(URLog(
            url = url
        ))

        self.db.commit()
        print("Success!")



    # this function will take what's in the roll logs and compile the scoreboards
    def scoreboardCompile(self):

        #reflecting the db locally
        self.meta.reflect(bind = self.engine)

        #getting our rows
        self.rollers = self.db.query(RollerLog).all()
        self.subreddits = self.db.query(SubredditLog).all()
        self.urls = self.db.query(URLog).all()

        #making some blank lists
        rollerList = []
        #targetList = []
        subredditList = []
        urlList = []

        #looping through each row, compiling the data
        for log in self.rollers:
            rollerList.append(log.roller)
            #targetList.append(log.target)

        for log in self.subreddits:
            subredditList.append(log.subreddit)

        for log in self.urls:
            urlList.append(log.url)

        # these three lines extract uniquie list occurances, make a dictionary containing the number of times each unique elements occurs
        # and then sorts it from greatest to least
        rollerBoard = dictSort(countOcc(rollerList, unique(rollerList)))
        subredditBoard = dictSort(countOcc(subredditList, unique(subredditList)))
        urlBoard = dictSort(countOcc(urlList, unique(urlList)))
        print(rollerBoard, subredditBoard, urlBoard)





    # a function for wiping the logs
    def wipeLogs(self):

        #reflecting the db locally
        self.meta.reflect(bind = self.engine)

        #getting our rows
        self.rollers = self.db.query(RollerLog).delete()
        self.subreddits = self.db.query(SubredditLog).delete()
        self.urls = self.db.query(URLog).delete()

        self.db.commit()
        print(f"[DATABASE] Message! {self.rollers+self.subreddits+self.urls} rows deleted successfully!")





db = mainDB(const.database_username, const.database_password, const.database_host, const.database_port, const.database_name)
