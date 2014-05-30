# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from os import path
import json
import mtimewall
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from walls.models import Reginfo
RURL = 'https://api.weibo.com/oauth2/authorize?redirect_uri=http%3A//itimewall.sinaapp.com/home/&response_type=code&client_id=1930287190'

def rdrct(request):
    return HttpResponseRedirect(RURL)

def ihomepage(request):
    client = mtimewall.APIClient(mtimewall.APP_KEY, mtimewall.APP_SECRET, mtimewall.CALLBACK_URL)
    if request.get_full_path() == '/home/':
        return HttpResponseRedirect(RURL)
    if 'code' in request.GET:
        code = request.get_full_path().split('code=')[1]
        res = client.request_access_token(code)
        client.set_access_token(res.access_token, res.expires_in)

        stats = client.statuses.user_timeline.get()
        pg = 2
        st = client.statuses.user_timeline.get(page = pg)
        while st["statuses"]:
            stats["statuses"].extend(st["statuses"])
            if pg == 100:
                break
            pg = pg + 1
            st = client.statuses.user_timeline.get(page = pg)
        time_wall = mtimewall.TimeWall(stats["statuses"])
        time_wall.classify_life()
        try:
            preinfo = Reginfo.objects.get(user_name = stats["statuses"][0]["user"]["name"])
        except:
            rinfo = Reginfo(user_name = stats["statuses"][0]["user"]["name"], token=res.access_token)
            rinfo.save()
    else:
        nm = request.GET["name"]
        rinfo = Reginfo.objects.get(user_name = nm)
        client.set_access_token(rinfo.token, 1212121)

        stats = client.statuses.user_timeline.get()
        pg = 2
        st = client.statuses.user_timeline.get(page = pg)
        while st["statuses"]:
            stats["statuses"].extend(st["statuses"])
            if pg == 100:
                break
            pg = pg + 1
            st = client.statuses.user_timeline.get(page = pg)
        time_wall = mtimewall.TimeWall(stats["statuses"])
        time_wall.classify_life()
    
    ctxt = {'lst':[]}
    page = 0
    if 'page' in request.GET:
        page = int(request.GET['page'])
    ctxt['name'] = '&name=' + stats["statuses"][0]["user"]["name"]
    if time_wall.timeline_life:
        for i in range(len(time_wall.timeline_life[page])):
            dc = {}
            dc['time'] = '-'.join(time_wall.timeline_life[page][i]['time'])
            dc['text'] = time_wall.timeline_life[page][i]['text'];
            ctxt['lst'].append(dc)
        ctxt['page'] = []
        if page == 0:
            if len(time_wall.timeline_life) != 1:
                pg = {}
                pg['pg'] = page + 1
                pg['cont'] = '--此后>'
                ctxt['page'].append(pg)
        elif page == len(time_wall.timeline_life) - 1:
            pg = {}
            pg['pg'] = page - 1
            pg['cont'] = '<此前--'
            ctxt['page'].append(pg)
        else:
            ctxt['page'] = []
            pg = {}
            pg['pg'] = page - 1
            pg['cont'] = '<此前--'
            ctxt['page'].append(pg)
            pg = {}
            pg['pg'] = page + 1
            pg['cont'] = '--此后>'
            ctxt['page'].append(pg)
    ctxt['l'] = 14*len(ctxt['lst'])
    return render_to_response('timewall.html', ctxt)

def newspage(request):
    f1 = open(path.dirname(__file__) + '/' + '2013-06_1813080181.weibo')
    wbs = []
    l = f1.readlines()
    for i in l:
        if len(i) > 10:
            wbs.append(json.loads(i))
    time_wall = mtimewall.TimeWall(wbs)
    time_wall.classify_news()
    ctxt = {'lst':[]}
    page = 0
    if 'page' in request.GET:
        page = int(request.GET['page'])
    if time_wall.timeline_news:
        for i in range(len(time_wall.timeline_news[page])):
            dc = {}
            dc['time'] = '-'.join(time_wall.timeline_news[page][i]['time'])
            dc['text'] = time_wall.timeline_news[page][i]['text'];
            ctxt['lst'].append(dc)
        ctxt['page'] = []
        if page == 0:
            if len(time_wall.timeline_news) != 1:
                pg = {}
                pg['pg'] = page + 1
                pg['cont'] = '--此后>'
                ctxt['page'].append(pg)
        elif page == len(time_wall.timeline_news) - 1:
            pg = {}
            pg['pg'] = page - 1
            pg['cont'] = '<此前--'
            ctxt['page'].append(pg)
        else:
            ctxt['page'] = []
            pg = {}
            pg['pg'] = page - 1
            pg['cont'] = '<此前--'
            ctxt['page'].append(pg)
            pg = {}
            pg['pg'] = page + 1
            pg['cont'] = '--此后>'
            ctxt['page'].append(pg)
    ctxt['l'] = 14*len(ctxt['lst'])
    return render_to_response('newswall.html', ctxt)