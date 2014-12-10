#-*- coding:utf-8 -*-

import urllib, pprint
from bs4 import BeautifulSoup

import urllib2, sys
import cookielib
import feedparser  
import codecs

a = codecs.open("iteye.txt", "w", "utf-8")
 
# pretent to be a browser: firefox 18.0
header_data = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               #'Accept-Language':'en-gb,zh-cn;q=0.8,en-us;q=0.5,en;q=0.3',
               'Connection':'keep-alive'}
def GetSource(url):
    # enable cookie
    cookie = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie,urllib2.HTTPHandler)
    # install opener
    urllib2.install_opener(opener)
    # pretent to be a browser
    request = urllib2.Request(url=url,headers=header_data)
    # send the request
    content = urllib2.urlopen(request)
    if content:
        return content.read()
    else:
        return ''

def getAllTopPythonArticles():
    soup = BeautifulSoup(GetSource('http://www.iteye.com/blogs'))    
    #print(soup.prettify())
    toparticleurls=list(set([i['href'] for i in soup.find_all('a') if len(i.contents[0])>10 and '_blank' in str(i) and 'iteye.com/blog/' in str(i)]))
    topblogs=list(set([i.split('/blog')[0] for i in toparticleurls]))
    topblogRSSes=[i+'/rss' for i in topblogs]
    return toparticleurls, topblogs, topblogRSSes

def writeToFile(str):
    print str
    a.write(str+'\n')    

def getArticle(toparticleurls, feeds):
    for feed in feeds:
        d = feedparser.parse(feed) 
        #print d['feed']['title'], ' '.join(d.channel.title.split()), ' '.join(d.channel.description.split()), feed
        for e in d.entries:
            #if e.link in toparticleurls:
            print e.keys()
            try:
                writeToFile(', '.join(map(str, [e.title, '.'.join(e.id.split('/')[-3:]), e.published])))
                writeToFile(BeautifulSoup(e['summary_detail']['value']).get_text().replace('\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n'))
                writeToFile("#"*50)
            except:	pass

#pprint.pprint(getAllTopPythonArticles())
toparticleurls, topblogs, topblogRSSes=getAllTopPythonArticles()
getArticle(toparticleurls, topblogRSSes)
a.close()
