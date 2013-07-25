from database import *
import sys
import urllib2
import os

path = 'contents/'
if not os.path.exists(path):
    print 'mkdir'
    os.mkdir(path)



def crawl(url):
    request = urllib2.Request(url)
    request.add_header("Accept", "text/xml")
    f = urllib2.urlopen(request)
    rssfile = f.read()
    file(path+(url[7:].replace('/','-')),"w").write(rssfile)



url = sys.argv[1]

if not is_in_database(url):
    add_rss_data(url)
    crawl(url)
    exit(1)

else:
    if not is_feed_updated(url):
        print 'not updated'
        exit(1)

    else:
        crawl(url)
        exit(1)
        
