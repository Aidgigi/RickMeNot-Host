from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, session
from sqlalchemy.ext.declarative import declarative_base
from core.models import Base
from core.models import TestingModel
import core.constants as const


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
