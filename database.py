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

class RssStatus(Base):
    __tablename__ = 'rss_status'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    last_modified = Column(String)

    def __init__(self, url, last_modified):
        self.url = url
        self.last_modified = last_modified


def init_db():
    
    Base.metadata.create_all(bind=engine)


def is_in_database(url):
    
    return (True if RssStatus.query.filter(RssStatus.url == url).first() 
                 else False)
    


def add_rss_data(url):
    if not RssStatus.query.filter(RssStatus.url == url).first():
        
        print 'rss data is not in database. create data'
        request = urllib2.Request(url)
        request.add_header("Accept", "text/xml")
        f = urllib2.urlopen(request)
        rss_status=RssStatus(url, f.info().get('Last-Modified'))
        db_session.add(rss_status)
        db_session.commit()
        print 'success'

def is_feed_updated(url):
    rss_data = RssStatus.query.filter(RssStatus.url == url).first()

    if not rss_data.last_modified:

        return True

    else:
       
        request = urllib2.Request(url)
        request.add_header("Accept","text/xml")
        f = urllib2.urlopen(request)
        current_last_modified = f.info().get('Last-Modified')
    
        if rss_data.last_modified == current_last_modified:
        
            return False

        else:
            
            return True


def update_last_modified(url):
    
    rss_data = RssStatus.query.filter(RssStatus.url == url).first()
    request = urllib2.Request(url)
    request.add_header("Accept","text/xml")
    f = urllib2.urlopen(request)
    current_last_modified = f.info().get('Last-Modified')
    rss_data.last_modified = current_last_modified
    db_session.commit()
