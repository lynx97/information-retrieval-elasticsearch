from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, QueryDict
from elasticsearch import Elasticsearch
from django.core.paginator import Paginator
from .ResultsProxy import ResultsProxy
from .custom_pagination import custom_pagination
import time
 
def index(request):
    template = loader.get_template('demo/index.html')
    context = {
        
    }
    return HttpResponse(template.render(context, request))

def advanced_index(request):
    template = loader.get_template('demo/advanced_index.html')
    context = {
        
    }
    return HttpResponse(template.render(context, request))

def search(request, text, page):
    size = 10
    text_search = request.GET.get('textsearch','')
    if text_search == '':
        text_search = text
    page1 = request.GET.get('page')
    if page1 == None:
        page1 = page
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    doc = {
        "query": {
            "bool" : {
            "should" : [
                {"match_phrase" : {"title" : text_search}},
                {"match_phrase" : {"description" : text_search}},
                {"match_phrase" : {"content" : text_search}},
                {"match" : {"title" : text_search}},
                {"match" : {"description" : text_search}},
                {"match" : {"content" : text_search}}
            ]
            }
        }
    }
    #create object
    ress = ResultsProxy(es, "vnexpress", doc)
    page1 = int(page1)
    start = (page1 - 1) * size
    end = start + size
    t1 = time.time()
    cnt = ress.__len__()
    sl = slice(start, end, 1)
    t2 = time.time()
    tmp = ress.__getitem__(sl)
    sub_time = round(t2-t1, 4) #tinh thoi gian

    #pagination
    p = custom_pagination(cnt, size)
    xxx = p.gen_page(page1)
    page_obj = p.gen_page_obj(page1)
    for x in tmp:
        x['source'] = x['_source']
    return render(request, 'demo/search.html', {
        'res': tmp,'page_obj': page_obj, 'text': text_search.replace(' ', '+'), 'value': text_search.replace('+',' '),'count':cnt, 'time': sub_time, 'xxx': xxx
    })

def advanced_search(request, page, title = None, description = None, content = None, date1 = None, date2 = None):
    size = 10
    title1 = request.GET.get('title','')
    description1 = request.GET.get('description','')
    content1 = request.GET.get('content','')
    date1_1 = request.GET.get('date1','')
    date2_1 = request.GET.get('date2','')
    
    page1 = request.GET.get('page')
    if page1 == None:
        page1 = page
    if title != None:
        title1 = title
    if description != None:
        description1 = description 
    if content != None:
        content1 = content 
    if date1 != None:
        date1_1 = date1
    if date2 != None:
        date2_1 = date2 
    obj = {"title": title1, "description": description1, "content": content1,"date1": date1_1, "date2": date2_1}
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    #tim kiem theo cac truong title, description, content
    #khi co dau vao khac "" thi moi tim kiem
    must_match = []
    if(title1 != ""):
        obj_title = {"match_phrase" : {"title" : title1}}
        must_match.append(obj_title)
    if(description1 != ""):
        obj_description = {"match_phrase" : {"description" : description1}}
        must_match.append(obj_description)
    if(content1 != ""):
        obj_content = {"match_phrase" : {"content" : content1}}
        must_match.append(obj_content)
    doc = {
        "query": {
            "bool" : {
            "must" : must_match
            }
        }
    }
    #create object
    ress = ResultsProxy(es, "vnexpress", doc)
    page1 = int(page1)
    start = (page1 - 1) * size
    end = start + size
    t1 = time.time()
    sl = {"date1": date1_1, "date2": date2_1, "start": start, "end": end}
    res = ress.__getitembydate__(sl)
    tmp = res["tmp"]
    cnt = res["count"]
    t2 = time.time()
    sub_time = round(t2-t1, 4) #tinh thoi gian

    #pagination
    p = custom_pagination(cnt, size)
    xxx = p.gen_page(page1)
    page_obj = p.gen_page_obj(page1)
    for x in tmp:
        x['source'] = x['_source']
    return render(request, 'demo/advanced_search.html', {
        'res': tmp,'page_obj': page_obj, 'time': sub_time, 'xxx': xxx, "obj":obj,"cnt": cnt
    })
