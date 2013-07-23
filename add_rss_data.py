from db_setting import db_session, RssStatus
import urllib2
import sys

url = sys.argv[1]

if not RssStatus.query.filter(RssStatus.url == url).first():
    
    print 'rss data is not in database. create data'
    request = urllib2.Request(url)
    f = urllib2.urlopen(request)
    rss_status=RssStatus(url, f.info().get('Last-Modified'))
    db_session.add(rss_status)
    db_session.commit()
    print 'success'
    
else:

    print 'rss data is already in database'
