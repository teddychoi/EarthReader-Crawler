from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import urllib2
import argparse


engine = create_engine('sqlite:///rss.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class RssData(Base):
    __tablename__ = 'rss_data'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    last_modified = Column(String)


    def __init__(self, url):
        self.url = url


    def is_feed_updated(self, current_last_modified):

        if not self.last_modified:

            return True

        else:
       
            if self.last_modified == current_last_modified:
        
                return False

            else:
            
                return True


    def update_last_modified(self, current_last_modified):
    
        self.last_modified = current_last_modified
        db_session.commit()


def init_db():
    
    Base.metadata.create_all(bind=engine)


def is_in_database(url):
    
    return (True if RssData.query.filter(RssData.url == url).first() 
                 else False)
    

def add_rss_data(url):
        
    print 'rss data is not in database. create data'
    rss_data=RssData(url, None)
    db_session.add(rss_data)
    db_session.commit()
    print 'success'
