from django.conf.urls import patterns, include, url
from django.http import *

urlpatterns = patterns('',
    (ur'^$', lambda request: HttpResponseRedirect('/main/')),
    (ur'^main/', include('main.urls')),
    (ur'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './media'}),
)
