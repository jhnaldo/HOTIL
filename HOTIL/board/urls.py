from django.conf.urls import patterns, include, url
from django.http import *

urlpatterns = patterns('',
    (ur'^$', 'board.views.index'),
)
