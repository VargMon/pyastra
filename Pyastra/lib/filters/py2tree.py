############################################################################
# $Id$
#
# Description: Python to tree filter. Pyastra project.
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
"""Pyastra filter: py2tree
Based on standard python AST compiler."""

import os.path, compiler, pyastralib, pyastra.ports.pic14, pyastra.ports.pic14.modules, pyastra.modules
from compiler.ast import *

converts_from='py'
converts_to='tree'

def get_ports():
    return []

def get_procs(port):
    return []

class Filter:
    modified = 1
    interrupts_on=0
    meta={}
    
    def __init__(self, root, opts):
        self.opts=opts
        self.say=self.opts['converter'].say
        self.data=self.scan(compiler.parse(root))
        self.data.interrupts_on=self.interrupts_on

    def scan(self, node, namespace=''):
        if isinstance(node, list):
            ret=[]
            for n in node:
                rnode=self.scan(n, namespace)
                if type(rnode) in (list, tuple):
                    ret += rnode
                else:
                    ret += [rnode]
            return ret
        elif isinstance(node, Assign):
            return node
        elif isinstance(node, From):
            if node.names != [('*', None)]:
                self.say('only "from <module_name> import *" input statement is supported while', ERROR, self.lineno(node))
                return
            root=self._import(node.modname)
            return self.scan(root, namespace)
        elif isinstance(node, Function):
            if node.name == 'on_interrupt':
                self.interrupts_on=1
                return node
            else:
                return node
        elif isinstance(node, Import):
            # TODO: Test it!
            ret=[]
            for name in node.names:
                iname=name[1] or name[0]
                root=self._import(name[0])
                ret += [self.scan(root, iname)]
            return ret
        elif isinstance(node, Module):
            m=Module(node.doc, self.scan(node.node, namespace))
            m.namespace=namespace
            return m
        elif isinstance(node, Stmt):
            return Stmt(self.scan(node.nodes, namespace))
        else:
            return node

    def _import(self, modname):
        name='%s.py' % (os.path.sep.join(modname.split('.')))
        if not os.path.exists(name):
            name=os.path.join(pyastra.ports.pic14.modules.__path__[0], name)
        if not os.path.exists(name):
            name=os.path.join(pyastra.modules.__path__[0], name)
        c=pyastralib.Converter(name, self.opts['caller_select'], self.say, trg_t=['tree_op'], opts=self.opts.copy(), src_t='file')
        # FIXME: Correct code for case when convert() returns more
        #        than one root
        # Fix the same code in tree_op2asm
        return c.convert()[0].data
