from db_setting import RssStatus, db_session
import urllib2
import sys

url = sys.argv[1]
rss_data = RssStatus.query.filter(RssStatus.url == url).first()

if not rss_data:
    print 'rss data is not in database'

else:
    if not rss_data.last_modified:

        print "no 'Last-Modified' data in database"
    
    else:
       
        request = urllib2.Request(url)
        request.add_header("Accept","text/xml")
        f = urllib2.urlopen(request)
        current_last_modified = f.info().get('Last-Modified')
        
        if rss_data.last_modified == current_last_modified:
        
            print 'not updated'
        
        else:
            
            print 'updated'
            print "updating 'Last-Modified' data"
            rss_data.last_modified = current_last_modified
            db_session.commit()
            print 'success'

