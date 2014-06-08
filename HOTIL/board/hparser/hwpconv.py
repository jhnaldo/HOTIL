# -*- coding: utf-8 -*-

from heqparser import HEq2TeX
from hwp5.xmlmodel import Hwp5File
from hwp5.treeop import STARTEVENT
from hwp5.binmodel import Text, EqEdit, Paragraph

def HWPtoText(filename):
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
                l.append(p[1]['text'])
            elif p[0] is EqEdit:
                l.append("$%s$" % e[ei])
                ei += 1
        else:
            if p[0] is Paragraph:
                l.append("</p>\n")
    return ''.join(l)

if __name__ == '__main__':
    print HWPtoText('asdf.hwp')
