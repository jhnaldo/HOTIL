from django.conf.urls import patterns, include, url
from django.http import *

urlpatterns = patterns('',
    (ur'^$', 'board.views.index'),
    (ur'^upload/$', 'board.views.upload'),
    (ur'^page/$', 'board.views.page'),
    (ur'^show/$', 'board.views.show'),
    (ur'^delete/$', 'board.views.delete'),
)
