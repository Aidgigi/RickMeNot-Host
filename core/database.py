from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from core.models import Base
from core.models import *
from core.helpers import unique, countOcc, dictSort, dictMerge
import core.constants as const
import json, random
from random import randint


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

        # we need this to update the roll count
        self.boards = self.db.query(Stats).all()
        # performing some checks to make sure we dont work with bad data
        if len(self.boards) == 0:
            print("[DATABASE] Warning! Stats cannot be extracted (empty)!")
            # returning 0 provides deeper error handling and prevents the rest of the function from running
            self.boards = 0

        self.boards = self.boards[0]

        self.boards.roll_count += 1

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
        print(f"[DATABASE] Message! Logged a roll by user {user}!")


    # this function will return the current scoreboards
    def scoreboardExtract(self):

        #reflecting the db locally
        self.meta.reflect(bind = self.engine)

        self.boards = self.db.query(Stats).all()

        if len(self.boards) == 0:
            print("[DATABASE] Warning! Stats cannot be extracted (empty)!")
            # returning 0 provides deeper error handling and prevents the rest of the function from running
            return 0

        self.boards = self.boards[0]

        # checks passed, moving on

        return {
            "boards": {
                'roll_count': self.boards.roll_count,
                'roller_board': json.loads(self.boards.roller_board),
                'subreddit_board': json.loads(self.boards.subreddit_board),
                'video_board': json.loads(self.boards.video_board)
            }
        }



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

        # merging dicts with the current boards
        currentBoards = self.scoreboardExtract()

        rollerBoard = dictMerge(rollerBoard, currentBoards['boards']['roller_board'])
        subredditBoard = dictMerge(subredditBoard, currentBoards['boards']['subreddit_board'])
        urlBoard = dictMerge(urlBoard, currentBoards['boards']['video_board'])

        # getting the board
        self.boards = self.db.query(Stats).all()

        if len(self.boards) == 0:
            print("[DATABASE] Warning! Stats cannot be extracted (empty)!")
            # returning 0 provides deeper error handling and prevents the rest of the function from running
            return 0

        self.boards = self.boards[0]

        self.boards.roller_board = json.dumps(dictSort(rollerBoard))
        self.boards.subreddit_board = json.dumps(dictSort(subredditBoard))
        self.boards.video_board = json.dumps(dictSort(urlBoard))

        # committing our changes
        self.db.commit()
        self.wipeLogs()


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


    # this function will trim each scoreboard, leaving the top 100 entries
    def scoreboardTrim(self):

        #reflecting the db locally
        self.meta.reflect(bind = self.engine)

        # getting the boards
        self.boards = self.db.query(Stats).all()

        if len(self.boards) == 0:
            print("[DATABASE] Warning! Stats cannot be extracted (empty)!")
            # returning 0 provides deeper error handling and prevents the rest of the function from running
            return 0

        self.boards = self.boards[0]

        # getting the first 100 elements
        self.boards.roller_board = json.dumps({A:N for (A,N) in [x for x in dictSort(json.loads(self.boards.roller_board)).items()][:100]})
        self.boards.subreddit_board = json.dumps({A:N for (A,N) in [x for x in dictSort(json.loads(self.boards.subreddit_board)).items()][:100]})
        self.boards.video_board = json.dumps({A:N for (A,N) in [x for x in dictSort(json.loads(self.boards.video_board)).items()][:100]})

        self.db.commit()



    # a function for writing some test rows
    def testLogs(self, num):

        username1 = ['aidgigi', 'aidgigi', 'spez', 'ohbarmer', 'joe']
        username2 = ['me', 'me', 'tomato', 'godzilla']
        subreddit = ['mytestsubgoaway', 'memes', 'fortnite']
        url = ['https://obama.com', 'https://youtube.com', 'https://twitter.com']

        for i in range(num):
            self.logRoll(randint(0, 300), randint(0, 300), random.choice(subreddit), random.choice(url))

    def smallTest(self):

        #reflecting the db locally
        self.meta.reflect(bind = self.engine)

        # getting the boards
        self.boards = self.db.query(Stats).all()

        if len(self.boards) == 0:
            print("[DATABASE] Warning! Stats cannot be extracted (empty)!")
            # returning 0 provides deeper error handling and prevents the rest of the function from running
            return 0

        self.boards = self.boards[0]

        print(len(json.loads(self.boards.roller_board)))








db = mainDB(const.database_username, const.database_password, const.database_host, const.database_port, const.database_name)
