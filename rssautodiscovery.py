from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import urllib2
import sys
import re

def get_html(url):
    
    request = urllib2.Request(url)
    f = urllib2.urlopen(request)
    html = f.read()
    f.close()
    return html


def get_rss_url(html):
    rss_url_list = re.findall("link.+type=\"application/rss\+xml\"[^>]+", html)
    for url in rss_url_list:
        match_obj = re.search("(href=\")(http://[^\"]+)", url)
        print match_obj.group(2)

html = get_html(sys.argv[1])
get_rss_url(html)
