#-*- coding: utf-8-*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from board.models import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

def index(request):
    problems = Problem.objects.all()
    return render_to_response('board/index.html', {
        'questions':problems
    }, context_instance=RequestContext(request))

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        for key in request.FILES:
            f = request.FILES[key]
            title = str(f)
            title = title[:-len(title.split('.')[-1])-1]
            f.name = 'test.hwp'
            hwp = HWPFile(hwp=f)
            hwp.save()

            #TODO parse

            html=''
            problem = Problem(title=title,writer=user,html=html)
            problem.save()

            os.remove(settings.MEDIA_ROOT+'/hwp/test.hwp')
            hwp.delete()
        return HttpResponse(0)
    else:
        return HttpResponseRedirect('/')
