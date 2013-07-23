from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

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
        print url
        self.last_modified = last_modified
        print last_modified


def init_db():
    Base.metadata.create_all(bind=engine)
