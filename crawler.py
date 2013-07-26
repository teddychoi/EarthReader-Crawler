from database import *
import sys
import urllib2
import os


path = 'contents/'
if not os.path.exists(path):
    print 'mkdir'
    os.mkdir(path)



def crawl(rss_data):

    request = urllib2.Request(rss_data.url)
    request.add_header("Accept", "text/xml")
    request.add_header("If-Modified-Since", rss_data.last_modified)
    try :
        f = urllib2.urlopen(request)
        rssfile = f.read()
        current_last_modified = f.info().get('Last-Modified')
        file(path+(rss_data.url[7:].replace('/','-')),"w").write(rssfile)
        rss_data.update_last_modified(current_last_modified)
    
    except urllib2.HTTPError as e :
        print 'not updated'



url = sys.argv[1]


if not is_in_database(url):
    add_rss_data(url)
    rss_data = RssData.query.filter(RssData.url == url).first()  
    crawl(rss_data)
    exit(1)

rss_data = RssData.query.filter(RssData.url == url).first()
crawl(rss_data)
exit(1)
        
