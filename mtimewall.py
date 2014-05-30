#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import json
from weibo import APIClient

#parameters of the app, used to send request
APP_KEY = '193****190'
APP_SECRET = 'c8ea53********7369'
CALLBACK_URL = 'http://itimewall.sinaapp.com/home/'

#constants of dictionary
NDIC = 7
NDIC2 = 7
DCT = {0:u'旅游', 1:u'体育', 2:u'音乐', 3:u'影视', 4:u'饮食', 5:u'游戏', 6:u'购物'}
DCT2 = {0:u'政治', 1:u'军事', 2:u'财经', 3:u'健康', 4:u'娱乐', 5:u'体育', 6:u'科教'}
MON = {'Jan':'1', 'Feb':'2', 'Mar':'3', 'Apr':'4', 'May':'5', 'Jun':'6', 
       'Jul':'7', 'Aug':'8', 'Sep':'9', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

#the color of category displayed on web
color = {0:"rgba(255,165,0,0.5)", 1:"rgba(12,21,255,0.24)", 2:"rgba(55,249,15,0.6)", 3:"rgba(221,123,251,0.4)", 4:"rgba(122,227,255,0.5)", 5:"rgba(2,255,254,0.5)", 6:"rgba(255,0,0,0.25)"}


#init
lib = [[] for i in range(NDIC)]
key = [[] for i in range(NDIC)]
lib2 = [[] for i in range(NDIC2)]
key2 = [[] for i in range(NDIC2)]
person = []
rtime = []
wtime = []
wsign = []
wsign2 = []
sign2 = []

#function of getting dics
def read_text(path, lst):
    f = open(os.path.dirname(__file__) + '/' + path)
    l = f.readlines()
    for ln in l:
        lst.append(ln.strip())
    f.close()

def read_weight(path, lst):
    f = open(os.path.dirname(__file__) + '/' + path)
    l = f.readlines()
    for ln in l:
        ln = ln.split()
        lst.append((ln[0], int(ln[1])))
    f.close()
 
# read keyword database
read_text('dic/rtime.txt', rtime)
read_text('dic/wtime.txt', wtime)
read_weight('dic/person.txt', person)
read_weight('dic/wsign.txt', wsign)
read_weight('dic2/others.txt', wsign2)
read_weight('dic2/sign.txt', sign2)
for i in range(NDIC):
    read_text('dic/' + DCT[i] + '.txt', lib[i])
    read_weight('dic/' + DCT[i] + 'key.txt', key[i])
for i in range(NDIC2):
    read_text('dic2/' + DCT2[i] + '.txt', lib2[i])
    read_weight('dic2/' + DCT2[i] + 'key.txt', key2[i])

''' 
main class

method "classify_life" is used to classify the user's weibos of his own life according to their characters. 
Once executed, you can get a list of weibos in the order of date with its category number in the attribute "timeline_life".

"classify_news" is used to classify the important news retweeted by the user. It works in the similar way.
'''
class TimeWall(object):
    def __init__(self, weibos):
        self.weibos = weibos
        self.timeline_life = []
        self.timeline_news = []
    
    def classify_life(self):
        timeline_life = []
        for ii in range(len(self.weibos)):
            wb = self.weibos[len(self.weibos)-1-ii]
            if wb.has_key('retweeted_status'):
                continue
            line = wb['text'].encode('utf8')
            if ((line.find('转：') == 0) or (line.find('转发') > -1) or
                (line.find('转自') > -1) or (line.find('转')+len('转') == len(line))):
                continue
            max = 3
            id = -1
            for itm in person:
                if line.find(itm[0]) > -1:
                    max -= itm[1]
                    #print itm[0].decode('utf8')
            for itm in rtime:
                if line.find(itm) > -1:
                    max -= 2
                    break
            for itm in wtime:
                if line.find(itm) > -1:
                    max += 6
            for itm in wsign:
                if line.find(itm[0]) > -1:
                    max -= itm[1]
            if max > 15:
                continue
            for i in range(NDIC):
                #print '//////////////'
                #print DCT[i].encode('gbk')
                num = 0
                for word in lib[i]:
                    if line.find(word) > -1:
                        num = 1
                        if (i == 4) and (line.find('吃') + len('吃') == line.find(word)):
                            num = 3
                            break
                        #print word.decode('utf8')
                for itm in key[i]:
                    if line.find(itm[0]) > -1:
                        num += itm[1]
                        #print itm[0].decode('utf8')
                if (i == 3) and (line.find('第') > -1) and (
                    (line.find('集') > line.find('第')) or
                    (line.find('部') > line.find('第')) ):
                    num += 3
                if num > max:
                    max = num
                    id = i
                    #print num
            if id != -1:
                tl = wb['created_at'].encode('utf8').split()
                tm = [tl[5], MON[tl[1]], tl[2]]
                if (len(timeline_life) > 0) and (timeline_life[len(timeline_life) - 1]['time'] 
                    == tm):
                    elmt = {}
                    elmt['color'] = color[id]
                    elmt['txt'] = line
                    timeline_life[len(timeline_life) - 1]['text'].append(elmt)
                else:
                    new = {}
                    new['time'] = tm
                    new['text'] = []
                    elmt = {}
                    elmt['color'] = color[id]
                    elmt['txt'] = line
                    new['text'].append(elmt)
                    timeline_life.append(new)
                #print line
                #print id 
                #print '------------------'
        temp = []
        for i in range(len(timeline_life)):
            if (i % 7) == 0:
                temp.append([])
            temp[len(temp)-1].append(timeline_life[i])
        self.timeline_life = temp

    def classify_news(self):
        timeline_news = []
        for ii in range(len(self.weibos)):
            #wb = self.weibos[len(self.weibos)-1-ii]
            wb = self.weibos[ii]
            if wb.has_key('retweeted_status'):
                line = wb['retweeted_status']['text'].encode('utf8')
                max = 5
                id = -1
                for itm in sign2:
                    if line.find(itm[0]) > -1:
                        max -= itm[1]
                for itm in wsign2:
                    if line.find(itm[0]) > -1:
                        max -= itm[1]
                for i in range(NDIC2):
                    num = 0
                    for word in lib2[i]:
                        if line.find(word) > -1:
                            num = 1
                            break
                    for itm in key2[i]:
                        if line.find(itm[0]) > -1:
                            num += itm[1]
                    if num > max:
                        max = num
                        id = i
                if id != -1:
                    tl = wb['created_at'].encode('utf8').split()
                    tm = [tl[5], MON[tl[1]], tl[2]]
                    if (len(self.timeline_news) > 0) and (self.timeline_news[len(self.timeline_news) - 1]['time'] 
                        == tm):
                        elmt = {}
                        elmt['color'] = color[id]
                        elmt['txt'] = line
                        self.timeline_news[len(self.timeline_news) - 1]['text'].append(elmt)
                    else:
                        new = {}
                        new['time'] = tm
                        new['text'] = []
                        elmt = {}
                        elmt['color'] = color[id]
                        elmt['txt'] = line
                        new['text'].append(elmt)
                        self.timeline_news.append(new)
        temp = []
        for i in range(len(self.timeline_news)):
            if (i % 7) == 0:
                temp.append([])
            temp[len(temp)-1].append(self.timeline_news[i])
        self.timeline_news = temp    

