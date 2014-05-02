from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (ur'^main/', include('main.urls')),
    (ur'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './media'}),
)
