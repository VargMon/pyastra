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

import sys, os, os.path

HEADER="""############################################################################
# $Id$
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
    if len(sys.argv) < 2:
        print 'usage:\ninc2py.py file1 [file2 [...]]'
        sys.exit(4)
        
    proclist=''

    for in_name in sys.argv[1:]:
        proc_name=os.path.split(in_name)[1][1:-4]
        out_name='%s.py' % proc_name
        
        inp=open(in_name)
        out=open(out_name, 'wb')
        inc2py(inp, out, proc_name)
        proclist += "'%s', " % proc_name
        
    print "Added processors:\n%s" % proclist[:-2]

def inc2py(inp, out, proc_name):
    out.write(HEADER % proc_name.upper())
    ch=1
    ignore=0
    buf=['', '', '']
    b={}
    lmn=0

    while ch:
        ch=inp.read(1)
        if ch=='\n' or not ch:
            if buf and buf[1]=='EQU' and buf[0][0] != '_' and not (buf[0] in ('F', 'W')):
                a=int(buf[2][2:-1], 16)
                adr=a & 0x7f
                if buf[0] in ('STATUS', 'FSR', 'PCL'):
                    bank=-1
                else:
                    bank=(a & 0x180) >> 7
                if b not in buf:
                    b[buf[0]]= "(%s, %g)" % (hex(adr), bank)
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

    out.write('hdikt={')

    b=b.items()
    for i in xrange(len(b)/3):
        out.write("'%s': %s, '%s': %s, '%s': %s,\n" %
                  (b[i*3  ][0], b[i*3  ][1],
                   b[i*3+1][0], b[i*3+1][1],
                   b[i*3+2][0], b[i*3+2][1]))

    for i in xrange((len(b)/3)*3, len(b)):
        out.write("'%s': %s, " % b[i])
        
    out.write('}\n')

    inp.close()
    out.close()

main()
