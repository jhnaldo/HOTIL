#-*- coding: utf-8-*-

from django.shortcuts import render_to_response
from django.template import RequestContext

def signup(request):
    return render_to_response('account/signup.html', {
    }, context_instance=RequestContext(request))

def _login(request):
    return render_to_response('account/login.html', {
    }, context_instance=RequestContext(request))

def _logout(request):
    return render_to_response('account/login.html.html', {
    }, context_instance=RequestContext(request))
