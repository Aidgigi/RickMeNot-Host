#importing all of the things we need for the database models
from sqlalchemy import Column, Integer, BigInteger, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# this table is for keeping track of statistics
class Stats(Base):
    __tablename__ = "BOT_STATISTICS_TABLE"

    id = Column(BigInteger, primary_key = True)
    roll_count = Column(BigInteger)
    roller_board = Column(String)
    subreddit_board = Column(String)
    video_board = Column(String)


class RollerLog(Base):
    __tablename__ = "ROLLER_LOG_TABLE"

    id = Column(Integer, Sequence('1'), primary_key=True)
    roller = Column(String)
    target = Column(String)


class SubredditLog(Base):
    __tablename__ = "SUBREDDIT_LOG_TABLE"

    id = Column(Integer, Sequence('2'), primary_key=True)
    subreddit = Column(String)


class URLog(Base):
    __tablename__ = "URL_LOG_TABLE"

    id = Column(Integer, Sequence('3'), primary_key=True)
    url = Column(String)


# this table defines subreddits that are on the blacklist
class Blacklist(Base):
    __tablename__ = "SUBREDDIT_BLACKLIST_TABLE"

    id = Column(BigInteger, primary_key = True)
    subreddit = Column(String)
    opt_reason = Column(String)
