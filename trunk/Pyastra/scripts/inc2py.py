#!/usr/bin/python
############################################################################
# $Id$
#
# Description: inc to python compiler. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
############################################################################

#
# TODO:
# shared banks should be added to databanks too (if they aren't already)
#

import sys, os, os.path

HEADER="""############################################################################
# $"""+'Id'+"""$
#
# Description: PIC %s definition. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
############################################################################

"""

whites=(' ', '\t')
maxram=0

def main():
    global maxram
    
    if len(sys.argv) < 3:
        print 'usage:\ninc2py.py dir proc1 [proc2 [...]]'
        sys.exit(4)
        
    proclist=''
    diry=sys.argv[1]

    for proc_name_ in sys.argv[2:]:
        if proc_name_[-1]=='x':
            names=[]
            for i in os.listdir(os.path.join(diry, 'lkr')):
                ii=os.path.splitext(i)[0]
                if ii[:-1]==proc_name_[:-1]:
                    names.append(ii)
        else:
            names=[proc_name_,]
            
        for proc_name in names:
            maxram=0
            in_name=os.path.join(diry, 'header', 'p%s.inc' % proc_name_)
            in2_name=os.path.join(diry, 'lkr', '%s.lkr' % proc_name)
            out_name='%s.py' % proc_name
            
            out=open(out_name, 'wb')
            
            inp=open(in_name)
            inc2py(inp, out, proc_name)
            inp.close()
            
            inp=open(in2_name)
            lkr2py(inp, out, proc_name)
            inp.close()
            
            out.write('maxram = %s' % hex(maxram))
            
            out.close()
            proclist += "'%s', " % proc_name
        
    print "Added processors:\n%s" % proclist[:-2]

def inc2py(inp, out, proc_name):
    global maxram
    out.write(HEADER % proc_name.upper())
    ch=1
    ignore=0
    buf=['', '', '']
    lmn=0
    b={}
##    bits=0

    while ch:
        ch=inp.read(1)
        if ch=='\n' or not ch:
            if (not ignore) and buf[1]=='EQU' and buf[0][0] != '_' and not (buf[0] in ('F', 'W')):
                a=int(buf[2][2:-1], 16)
                if b not in buf:
                    b[buf[0]]= "%s" % (hex(a), )
                    if a>maxram:
                        maxram=a
                    
            ignore=0
            buf=['', '', '']
            lmn=0
        elif not ignore:
            if ch==';':
                ignore=1
            elif ch in whites:
                if lmn==0 and not buf[0]:
                    ignore=1
                elif buf[lmn]:
                    if lmn<2:
                        lmn += 1
                    else:
                        ignore=1
            else:
                buf[lmn] += ch
##        elif (not bits) and ch=='B':
##            tmpl='Bits'
##            while tmpl[0]==ch:
##                tmpl=tmpl[1:]
##                if not tmpl:
##                    bits=1
##                    break
##                ch=inp.read(1)
    
    out.write('hdikt={')

    b=b.items()
    b0=map(lambda it: it[0], b)
    for i in ('RP0', 'RP1', 'STATUS', 'Z', 'C'):
        if i not in b0:
            print 'WARNING: %s doesn\'t have register or bit %s' % ( proc_name, i)
        
    for i in xrange(len(b)/3):
        if i:
            out.write('       ')
        out.write("'%s': %s, '%s': %s, '%s': %s,\n" %
                  (b[i*3  ][0], b[i*3  ][1],
                   b[i*3+1][0], b[i*3+1][1],
                   b[i*3+2][0], b[i*3+2][1]))
        
    out.write('       ')
    
    for i in xrange((len(b)/3)*3, len(b)):
        out.write("'%s': %s, " % b[i])
        
    out.write('}\n')
    
def lkr2py(inp, out, proc_name):
    global maxram
    ch=1
    ignore=0
    buf=['', '', '', '', '']
    lmn=0
    back=''
    pages=[]
    banks=[]
    vectors=None
    shareb={}
    
    while ch:
        if back:
            ch=back
            back=''
        else:
            ch=inp.read(1)
            
        if ch=='\n' or not ch:
            if not ignore and lmn>0:
                if buf[0]=='CODEPAGE':
                    if buf[4]!='PROTECTED':
                        pages.append((buf[2][6:], buf[3][4:]))
                    elif buf[1]=='NAME=vectors':
                        vectors=(buf[2][6:], buf[3][4:])
                elif buf[0]=='DATABANK':
                    if buf[4]!='PROTECTED':
                        banks.append((buf[2][6:], buf[3][4:]))
                        if eval(buf[3][4:]) > maxram:
                            maxram=eval(buf[3][4:])
                elif buf[0]=='SHAREBANK':
                    if buf[4]!='PROTECTED':
                        grp=buf[1][5:]
                        if grp not in shareb:
                            shareb[grp]=[]
                        shareb[grp].append((buf[2][6:], buf[3][4:]))
                        if eval(buf[3][4:]) > maxram:
                            maxram=eval(buf[3][4:])
                elif buf[0] not in ('LIBPATH', 'SECTION'):
                    print 'WARNING: unsupported keyword: %s' % buf[0]
            
            ignore=0
            buf=['', '', '', '', '']
            lmn=0
        elif not ignore:
            if ch=='/':
                ch=inp.read(1)
                if ch=='/':
                    ignore=1
                else:
                    back=ch
            elif ch in whites:
                if buf[lmn]:
                    lmn += 1
            else:
                buf[lmn] += ch

    for i in shareb.iterkeys():
        new=1
        for j in shareb[i]:
            for k in banks:
                if j[0]==k[0] and j[1]==k[1]:
                    new -= 1
                elif eval(k[0]) <= eval(j[0]) <= eval(k[1]) or eval(k[0]) <= eval(j[1]) <= eval(k[1]):
                    print "FIXME: proc %s: some of shared banks are subsequences of banks or vice versa" % proc_name
                    break
        if new == 1:
            banks.append(shareb[i][0])
        elif new < 0:
            print "FIXME: proc %s: some of shared banks are multiply representet in banks." % proc_name

    cmp0 = lambda x,y: cmp(eval(x[0]), eval(y[0]))
    
    pages.sort(cmp0)
    out.write('\npages=(')
    for i in pages:
        out.write('(%s, %s), ' % (i[0], i[1]))
    out.write(')\n')
                
    banks.sort(cmp0)
    out.write('\nbanks=(')
    for i in banks:
        out.write('(%s, %s), ' % (i[0], i[1]))
    out.write(')\n')

    out.write('\nshareb=(\n')
    for i in shareb.iterkeys():
        out.write('        (')
        for j in shareb[i]:
            out.write('(%s, %s), ' % (j[0], j[1]))
        out.write('),\n')
    out.write(')\n')
    if vectors:
        out.write('\nvectors=(%s, %s)\n' % (vectors[0], vectors[1]))
    else:
        out.write('\nvectors=None\n')

main()
