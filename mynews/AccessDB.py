# -*- coding: utf-8 -*-
import time, pprint

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from handlers.models import *

import textwrap
import random
import re

def hasChinese(mystr):
    RE = re.compile(u'[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]', re.UNICODE)
    nochinese = RE.sub('', mystr)
    return len(nochinese)<len(mystr)

def getMyNews(user_id):
    articles=db.GqlQuery("select * from Article order by published_date DESC limit 1000")
    mycats=getCategories(user_id)
    
    result={"CATEGORY":[(mycatname, [{"brief": article.title, "fulltext": textwrap.fill(article.summary, width=100/(1+hasChinese(article.summary))).replace('\n', '<br>'), "url": article.link, "id":int(random.random()*100000000)} for article in articles if any(i in article.summary.lower() for i in mycats[mycatname])][:10]) for mycatname in sorted(mycats.keys())],
            "REAL TIME":[{"brief": article.title, "fulltext": textwrap.fill(article.summary, width=100/(1+hasChinese(article.summary))).replace('\n', '<br>'), "url": article.link, "id":int(random.random()*100000000)} for article in articles[:55]]}    
    
    return result


def getCategories(user_id):
    mycats=db.GqlQuery("select * from UserCategory where username='%s'" % user_id)
    if len(list(mycats))==0:
        result= {u'Asia': [u'china', u'chinese', u'asia', u'japan', u'hongkong', u'singapore', u'taiwan', u'中国', u'亚洲', u'日本', u'香港', u'新加坡', u'台湾'],
                 u'Chemistry': [u'chemistry', u'chemical', u'dupont', u'air', u'化工', u'化学', u'药', u'生化'],
                 u'Commodities': [u'oil', u'energy', u'electricity', u'gas', u'石油', u'能源', u'电力', u'天然气'],
                 u'Electronics': [u'electr', u'chip', u'hardware', u'cpu', u'semiconductor', u'apple', u'samsung', u'htc', u'intel', u'芯片', u'导体', u'苹果', u'三星', u'英特尔', u'电子'],
                 u'Europe': [u'london', u'europe', u'france', u'russia', u'伦敦', u'欧', u'法国', u'俄罗斯', u'英国'],
                 u'Finance': [u'bank', u'investment', u'fund', u'stock', u'money', u'银行', u'投资', u'基金', u'股', u'货币', u'金融', u'经济'],
                 u'Food': [u'food',
                           u'fruit',
                           u'corn',
                           u'juice',
                           u'vegetable',
                           u'meat',
                           u'agricult',
                           u'食',
                           u'水果',
                           u'谷',
                           u'果汁',
                           u'蔬菜',
                           u'肉',
                           u'农',
                           u'转基因'],
                 u'Health Care': [u'biology', u'health', u'drug', u'medicine', u'medical', u'生物', u'健康', u'药', u'医', u'基因'],
                 u'Technology': [u'cpu', u'computer', u'software', u'技术', u'计算机', u'软件', u'开发', u'系统', u'科技'],
                 u'USA': [u'USA', u'america', u'美国', u'欧美']}
    else:
        result=dict([(mycat.categoryname, mycat.keywords.split()) for mycat in mycats])
    return result
"""
    {u'Asia': [u'china', u'chinese', u'asia', u'japan', u'hongkong', u'singapore'],
     u'Chemistry': [u'chemistry', u'chemical', u'dupont', u'air'],
     u'Commodities': [u'oil', u'energy', u'electricity', u'gas'],
     u'Electronics': [u'electr', u'chip', u'hardware', u'cpu', u'semiconductor'],
     u'Europe': [u'london', u'europe', u'france', u'russia'],
     u'Finance': [u'bank', u'investment', u'fund', u'stock', u'money'],
     u'Food': [u'food',
               u'fruit',
               u'corn',
               u'juice',
               u'vegetable',
               u'meat',
               u'agricult'],
     u'Health Care': [u'biology', u'health', u'drug', u'medicine', u'medical'],
     u'Technology': [u'cpu', u'computer', u'software'],
     u'USA': [u'USA', u'america']}
"""
    #===========================================================================
    # return {
    #     'computer': ['pc', 'cpu', 'computer'],
    #     'electronics': ['quantum', 'algorithm'],
    # }
    #===========================================================================


def updateCategories(user_id, categories):
    pass
