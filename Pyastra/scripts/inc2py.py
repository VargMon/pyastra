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

def main():
    if len(sys.argv) < 3:
        print 'usage:\ninc2py.py dir proc1 [proc2 [...]]'
        sys.exit(4)
        
    proclist=''
    diry=sys.argv[1]

    for proc_name in sys.argv[2:]:
        in_name=os.path.join(diry, 'header', 'p%s.inc' % proc_name)
        in2_name=os.path.join(diry, 'lkr', '%s.lkr' % proc_name)
        out_name='%s.py' % proc_name
        
        out=open(out_name, 'wb')
        
        inp=open(in_name)
        inc2py(inp, out, proc_name)
        inp.close()
        
        inp=open(in2_name)
        lkr2py(inp, out, proc_name)
        inp.close()
        
        out.close()
        proclist += "'%s', " % proc_name
        
    print "Added processors:\n%s" % proclist[:-2]

def inc2py(inp, out, proc_name):
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
    ch=1
    ignore=0
    buf=['', '', '', '', '']
    lmn=0
    back=''
    pages=[]
    banks=[]
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
                elif buf[0]=='DATABANK':
                    if buf[4]!='PROTECTED':
                        banks.append((buf[2][6:], buf[3][4:]))
                elif buf[0]=='SHAREBANK':
                    grp=buf[1][5:]
                    if grp not in shareb:
                        shareb[grp]=[]
                    shareb[grp].append((buf[2][6:], buf[3][4:]))
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
                
    out.write('\npages=(')
    for i in pages:
        out.write('(%s, %s), ' % (i[0], i[1]))
    out.write(')\n')
                
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

main()
