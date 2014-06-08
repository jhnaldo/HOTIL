#-*- coding: utf-8-*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from board.models import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import simplejson as json
import os
import codecs

# for parsing
from lrparsing import *
from hwp5.xmlmodel import Hwp5File
from hwp5.treeop import STARTEVENT
from hwp5.binmodel import Text, EqEdit, Paragraph

PROBLEM_PER_PAGE = 15

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

            try:
                html = HWPtoText(settings.MEDIA_ROOT+'/hwp/test.hwp')
            except:
                print 'here'
                os.remove(settings.MEDIA_ROOT+'/hwp/test.hwp')
                hwp.delete()
                return HttpResponse(-1)
            problem = Problem(title=title,writer=user,html=html)
            problem.save()

            os.remove(settings.MEDIA_ROOT+'/hwp/test.hwp')
            hwp.delete()
        return HttpResponse(0)
    else:
        return HttpResponseRedirect('/')

@csrf_exempt
def page(request):
    if request.method == 'POST':
        page = int(request.POST.get('pagenum',0))
        problems = Problem.objects.all().order_by('-created')
        remain = (len(problems)-1)%PROBLEM_PER_PAGE+1

        num = (len(problems)-1)/PROBLEM_PER_PAGE+1
        problems = problems[(page-1)*PROBLEM_PER_PAGE:]
        if len(problems)>PROBLEM_PER_PAGE:
            problems = problems[:PROBLEM_PER_PAGE]
        result = {'num':num,'problems':into_json(problems),'remain':remain}
        return HttpResponse(json.dumps(result,ensure_ascii=False,indent=4))
    else:
        return HttpResponseRedirect('/')

def into_json(problems):
    result = []
    for p in problems:
        result.append({'title':p.title,'writer':p.writer.first_name,'created':p.created.strftime("%Y-%m-%d"),'id':p.id})
    return result

def show(request):
    problem_id = int(request.GET.get('id',0))
    problem = Problem.objects.get(id=problem_id)
    return render_to_response('board/show.html', {
        'problem':problem,
    }, context_instance=RequestContext(request))

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        problem_id = request.POST['id']
        problem = Problem.objects.get(id=problem_id)
        problem.delete()
        return HttpResponse(0)
    else:
        return HttpResponseRedirect('/')

def edit(request):
    if request.method == 'POST':
        problem_id = int(request.POST.get('id',0))
        title = request.POST.get('title','')
        html = request.POST.get('html','')

        problem = Problem.objects.get(id=problem_id)
        problem.title = title
        problem.html = html
        problem.save()
        return HttpResponseRedirect('/problem/show/?id='+str(problem.id))
    else:
        problem_id = int(request.GET.get('id',0))
        problem = Problem.objects.get(id=problem_id)
        return render_to_response('board/edit.html', {
            'problem':problem,
        }, context_instance=RequestContext(request))


##################################      PARSER

def Kwd(k):
	return Keyword(k, case=False)

class HEqGrammar(Grammar):
	class T(TokenRegistry):
		value = Token(re="[0-9A-Za-z.]+")
		op = Tokens("+- -+ -> + - * / = != < > ,")
		u_op = Tokens("% ( ) `")
	expr = Ref("expr")
	atom = Ref("atom")
	frac_atom = atom << Kwd('over') << atom
	root_atom = Prio(
		(Kwd('sqrt') | Kwd('root')) >> atom >> Kwd('of') >> atom,
		(Kwd('sqrt') | Kwd('root')) >> atom
	)
	lim_atom = Kwd('lim') << '_' << atom
	paren_atom = '{' + expr + '}'
	concat_atom = atom << atom
	atom = Prio(
		paren_atom | frac_atom | root_atom | lim_atom,
		T.value | T.u_op,
		concat_atom
	)
	s_atom = atom + Repeat('_' + atom) + Repeat('^' + atom)
	expr = Prio(
		s_atom,
		T.op >> THIS,
		THIS << T.op << THIS
	)
	START = expr

def conv(tree):
	nt, G = tree[0], HEqGrammar
	if nt is G.frac_atom:
		return "\\frac %s %s" % (tree[1], tree[3])
	if nt is G.root_atom:
		if len(tree) == 3:
			return "\\sqrt %s" % tree[2]
		if len(tree) == 5:
			return "\\sqrt[%s]%s" % (tree[2], tree[4])
	if nt is G.lim_atom:
		return "\\lim_{%s}" % tree[3]
	if nt is G.concat_atom:
		return "%s%s" % (tree[1], tree[2])
	if nt is G.paren_atom:
		return "{%s}" % tree[2]
	if nt is G.s_atom:
		return "".join(tree[1:])
	if nt is G.expr:
		if len(tree) == 3:
			return "%s%s" % (tree[1], tree[2])
		if len(tree) == 4:
			return "%s%s%s" % (tree[1], tree[2], tree[3])
	if nt is G.T.value:
		tl = tree[1].lower()
		if tree[1] == 'alpha' or tree[1] == 'beta' or tree[1] == 'gamma' or tree[1] == 'delta':
			return "\\%s " % tree[1]
		if tree[1] == 'ALPHA' or tree[1] == 'BETA' or tree[1] == 'GAMMA' or tree[1] == 'DELTA':
			return "\\%s%s " % (tree[1][0], tree[1][1:].lower())
		if tl == 'times' or tl == 'therefore' or tl == 'geq' or tl == 'ge' or tl == 'leq' or tl == 'le' or tl == 'neq' or tl == 'ne':
			return "\\%s " % tl
		if tl == 'divide' or tl == 'div':
			return '\div '
		return tree[1]
	if nt is G.START:
		return tree[1]
	if tree[1] == '%':
		return '\% '
	if tree[1] == '`':
		return ' ' # return '\ '
	if tree[1] == '+-':
		return '\pm '
	if tree[1] == '-+':
		return '\mp '
	if tree[1] == '->':
		return "\\to "
	if tree[1] == '!=':
		return "\\neq "
	return tree[1]

def HEq2TeX(eq):
	return HEqGrammar.parse(eq.replace(u"±", "+-").replace(u"÷", " DIVIDE "), conv)

def HWPtoText(filename):
	def escape(s):
		return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
	f = Hwp5File(filename)
	l = []
	e, ei = [], 0
	for section in f.bodytext.sections:
		for record in section.records():
			if record['tagname'] == 'HWPTAG_CTRL_EQEDIT':
				s = record['payload']
				eql = ord(s[4]) + 256*ord(s[5])
				eq = []
				for i in xrange(eql):
					eq.append(unichr(ord(s[6+i*2])+256*ord(s[7+i*2])))
				e.append(HEq2TeX(''.join(eq)))
	for o in f.events():
		p = o[1]
		if o[0] is STARTEVENT:
			if p[0] is Paragraph:
				l.append("<p>")
			if p[0] is Text:
				l.append(escape(p[1]['text']))
			elif p[0] is EqEdit:
				l.append("<span class='tex'>%s</span>" % escape(e[ei]))
				ei += 1
		else:
			if p[0] is Paragraph:
				l.append("</p>\n")
	return ''.join(l)
