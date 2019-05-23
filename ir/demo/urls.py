from django.conf.urls import url 
 
from . import views 
app_name = "demo"
urlpatterns = [ 
    url(r'^$', views.index, name='index'),
    url(r'^advanced/$', views.advanced_index, name='advanced_index'),
    url(r'^(?P<text>[\w.@+-]*)/(?P<page>[0-9]+)/$', views.search, name='search'),
    url(r'^(?P<page>[0-9]+)/$', views.advanced_search, name='advanced_search'),
    url(r'^(?P<page>[0-9]+)/(?P<title>[\w.@+-]*)/(?P<description>[\w.@+-]*)/(?P<content>[\w.@+-]*)/(?P<date1>[\w.@+-]*)/(?P<date2>[\w.@+-]*)$', views.advanced_search, name='advanced_search'),
]