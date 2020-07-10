#importing all of the things we need for the database models
from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# this table is for keeping track of statistics
class StatsTable(Base):
    __tablename__ = "BOT_STATISTICS"

    id = Column(Integer, primary_key=True)
    total_roll_count = Column(BigInteger)
    biggest_roller = Column(String)
    redirects_used = Column(String)
    urls_used = Column(String)


    def repr(self):
        return 'Bot Statistics Table'


# this table defines subreddits that are on the blacklist
class Blacklist(Base):
    __tablename__ = "SUBREDDIT_BLACKLIST"

    id = Column(BigInteger, primary_key=True)
    subreddit = Column(String)
    opt_reason = Column(String)
