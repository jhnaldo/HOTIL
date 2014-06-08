# -*- coding: utf-8 -*-

from lrparsing import *

def Kwd(k):
	return Keyword(k, case=False)

class HEqGrammar(Grammar):
	class T(TokenRegistry):
		value = Token(re="[0-9A-Za-z()]+")
		op = Tokens("+- -+ -> + - * / = != < >")
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
		T.value,
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
	# print(tree)
	nt, G = tree[0], HEqGrammar
	if nt is G.frac_atom:
		return "\\frac %s %s" % (tree[1], tree[3])
	if nt is G.root_atom:
		if len(tree) == 3:
			return "\\sqrt %s" % tree[2]
		if len(tree) == 5:
			return "\\sqrt[%s] %s" % (tree[2], tree[4])
	if nt is G.lim_atom:
		return "\\lim_{%s}" % tree[3]
	if nt is G.concat_atom:
		return "%s %s" % (tree[1], tree[2])
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
		if tree[1] == 'alpha' or tree[1] == 'beta' or tree[1] == 'gamma' or tree[1] == 'delta':
			return "\\%s" % tree[1]
		if tree[1] == 'ALPHA' or tree[1] == 'BETA' or tree[1] == 'GAMMA' or tree[1] == 'DELTA':
			return "\\%s%s" % (tree[1][0], tree[1][1:].lower())
		return tree[1]
	if nt is G.START:
		return tree[1]
	if tree[1] == '+-':
		return '\pm'
	if tree[1] == '-+':
		return '\mp'
	if tree[1] == '->':
		return "\\to"
	return tree[1]

def HEq2TeX(eq):
	return HEqGrammar.parse(eq.replace(u"±", "+-"), conv)

if __name__ == '__main__':
	while True:
		print ">",
		print HEq2TeX(raw_input())
