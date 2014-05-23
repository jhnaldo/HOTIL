#-*- coding: utf-8-*-

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

def signup(request):
    return render_to_response('account/signup.html', {
    }, context_instance=RequestContext(request))

@csrf_exempt
def _login(request):
    print request.method
    if request.method == 'POST':
        user_id = request.POST.get('id','')
        password = request.POST.get('passwd','')
        try:
            user = authenticate(username=user_id, password=password)
        except UnicodeEncodeError:
            return HttpResponse(-1)
        if user is not None: # Login OK
            login(request, user)
            return HttpResponse(1)
        else: # Login Failed
            return HttpResponse(0)
    else:
        return HttpResponseRedirect('/')

def _logout(request):
    return render_to_response('account/login.html.html', {
    }, context_instance=RequestContext(request))
