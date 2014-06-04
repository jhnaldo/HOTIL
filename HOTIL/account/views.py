#-*- coding: utf-8-*-

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        user_id = request.POST.get('id','')
        password = request.POST.get('password','')
        name = request.POST.get('name','')
        user_type = request.POST.get('usertype','')

        user = User.objects.create_user(username=user_id, password=password)
        user.first_name = name
        user.is_staff = user_type=='manager'
        user.save()

        return HttpResponseRedirect('/');
    else:
        return render_to_response('account/signup.html', {
        }, context_instance=RequestContext(request))

@csrf_exempt
def _logout(request):
    print 1
    if request.method == 'POST':
        logout(request)
        return HttpResponse(0)
    else:
        return HttpResponseRedirect('/')

@csrf_exempt
def _login(request):
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

@csrf_exempt
def id_check(request):
    username = request.POST.get('id','')
    count = len(User.objects.filter(username=username))
    print count
    return HttpResponse(count)
