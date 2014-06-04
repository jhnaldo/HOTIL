from django.conf.urls import patterns, include, url
from django.http import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (ur'^$', lambda request: HttpResponseRedirect('/main/')),
    (ur'^main/', include('main.urls')),
    (ur'^signup/$', 'account.views.signup'),
    (ur'^id_check/$', 'account.views.id_check'),
    (ur'^login/$', 'account.views._login'),
    (ur'^logout/$', 'account.views._logout'),
    (ur'^problem/', include('board.urls')),
    (ur'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './media'}),

    (ur'^admin/', include(admin.site.urls)),
)
