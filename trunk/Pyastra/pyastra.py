#!/usr/bin/python
############################################################################
#
# Description: Tree to assemler convertor. Pyastra project.
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

#Exit codes:
# 0 - ok
# 1 - unsupported feature request
# 2 - syntax error
# 3 - hardware limitations error
# 4 - arguments error
#
#Built-in functions:
# asm - include verbatim asm text
# halt - halt the system
#
#TODO:
# * Check bank_sels
# ? Change generation style ("return str" instead of "self.body += ...")

import sys, os.path, compiler
from tree2asm import tree2asm

NFO='pypic 0.1.0'
PROC='16f877'
ICD = 1
#
# By default optimises for size,
# but if op_speed=1 than optimises for speed.
# 
op_speed = 0

print

if len(sys.argv) < 2:
    print '%s usage:\npypic.py infile [outfile]' % (NFO,)
    sys.exit(4)

root=compiler.parseFile(sys.argv[1])

if len(sys.argv) == 2:
    out_name=os.path.splitext(sys.argv[1])[0]+'.asm'
else:
    out_name=sys.argv[2]

p=tree2asm(ICD, op_speed)
p.convert(root)

pstr = 'Compiler has found'
ptest = 0
if p.errors:
    pstr += ' %g errors' % p.errors
if p.warnings:
    if ptest:
        pstr +=','
    pstr += '%g warnings' % p.warnings
if p.messages:
    if ptest:
        pstr +=','
    pstr += '%g messages' % p.messages

if ptest:
    print pstr+'.'

if p.errors:
    print 'No asm code generated.'
    sys.exit(1)

out=open(out_name, 'w')

out.write(""";
; Generated by %s
; infile: %s
;

\tprocessor\t%s
\t#include\tp%s.inc
        
""" % (NFO, sys.argv[1], PROC, PROC))

out.write(p.head)
out.write('\n\torg\t0x0\n')
if ICD:
    out.write('\tnop\n')
out.write("""\tgoto\tmain

\torg\t0x4
main
""")
out.write(p.body)

ftest=0
fbuf=''
for i in p.funcs:
    if not p.funcs[i][1]:
        print 'Undefined function call: %s' % i
    if p.funcs[i][3]:
        ftest=1
        fbuf+= p.funcs[i][1]
        p.instr += p.funcs[i][2]
        
out.write('\n\tgoto\t$\n')

if ftest:
    out.write("\n;\n; SUBROUTINES\n;\n\n%s" % fbuf)
    
out.write("\n\tend\n")
out.close()

l=p.ram_usage
if ICD:
    l += 1

print "Peak RAM usage: %g byte(s) (%.1g%%)" % (l, l*100/368.)
print "Program memory usage: %g word(s) (%.1g%%)" % (p.instr, p.instr*100/8192.)
if p.asm:
    print "NOTE: statistics includes data specified in asm function!"
if ICD:
    print "NOTE: statistics includes ICD memory usage!"

print
