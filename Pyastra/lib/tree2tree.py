############################################################################
# $Id$
#
# Description: Port-independent optimizer. Pyastra project.
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

import sys, os.path, compiler, pyastra.ports.pic14
from compiler.ast import *
from pyastra.ports.pic14.tree2asm import tree2asm

class tree2tree:
    
    def __init__(self, root, say):
        self.root=root
        self.interrupts_on=0
        self.say=say
        #print self.root
        self.root=self.scan(self.root)
        #print self.root
        self.root=self.replace(self.root)
        self.root.interrupts_on=self.interrupts_on
        #print self.root
        #sys.exit()

    def scan(self, node):
        if isinstance(node, list):
            ret=[]
            for n in node:
                ret += [self.scan(n)]
            return ret
        elif isinstance(node, Assign):
            return node
        elif isinstance(node, From):
            name='%s.py' % node.modname
            if not os.path.exists(name):
                name=os.path.join(pyastra.ports.pic14.__path__[0], name)
            root=compiler.parseFile(name)
            return self.scan(root)
        elif isinstance(node, Function):
            if node.name == 'on_interrupt':
                self.interrupts_on=1
                return node
            else:
                return node
        elif isinstance(node, Module):
            return Module(node.doc, self.scan(node.node))
        elif isinstance(node, Stmt):
            return Stmt(self.scan(node.nodes))
        else:
            return node
        
#    def replace(self, node):
#        if isinstance(node, list):
#            ret=[]
#            for n in node:
#                ret += [self.replace(n)]
#            return ret
#        elif isinstance(node, Add):
#            return Add((self.replace(node.left), self.replace(node.right)))
#        elif isinstance(node, And):
#            return And(self.replace(node.nodes))
#        elif isinstance(node, AssAttr):
#            return AssAttr(self.replace(node.expr), self.replace(node.attrname), node.flags)
#        elif isinstance(node, AssList):
#            return AssList(self.replace(node.nodes))
#        elif isinstance(node, AssName):
#            if node.name in self.aliases:
#                repl=self.aliases[node.name]
#                if isinstance(repl, Name):
#                    return AssName(repl.name, node.flags)
#                elif isinstance(repl, Subscript):
#                    return Subscript(repl.expr, node.flags, repl.subs)
#                else:
#                    self.say('Invalid context for alias %s!' % node.name, node.lineno, exit_status=1)
#            else:
#                return AssName(self.replace(node.name), self.replace(node.flags))
#        elif isinstance(node, AssTuple):
#            return AssTuple(self.replace(node.nodes))
#        elif isinstance(node, Assert):
#            return Assert(self.replace(node.test), self.replace(node.fail))
#        elif isinstance(node, Assign):
#            return Assign(self.replace(node.nodes), self.replace(node.expr))
#        elif isinstance(node, AugAssign):
#            return AugAssign(self.replace(node.node), self.replace(node.op), self.replace(node.expr))
#        elif isinstance(node, Backquote):
#            return Backquote(self.replace(node.expr))
#        elif isinstance(node, Bitand):
#            return Bitand(self.replace(node.nodes))
#        elif isinstance(node, Bitor):
#            return Bitor(self.replace(node.nodes))
#        elif isinstance(node, Bitxor):
#            return Bitxor(self.replace(node.nodes))
##        elif isinstance(node, Break):
#        elif isinstance(node, CallFunc):
#            return CallFunc(self.replace(node.node), self.replace(node.args), self.replace(node.star_args), self.replace(node.dstar_args))
#        elif isinstance(node, Class):
#            return Class(self.replace(node.name), self.replace(node.bases), node.doc, self.replace(node.code))
#        elif isinstance(node, Compare):
#            return Compare(self.replace(node.expr), self.replace(node.ops))
##        elif isinstance(node, Const):
##        elif isinstance(node, Continue):
#        elif isinstance(node, Dict):
#            return Dict(self.replace(node.items))
#        elif isinstance(node, Discard):
#            return Discard(self.replace(node.expr))
#        elif isinstance(node, Div):
#            return Div((self.replace(node.left), self.replace(node.right)))
##        elif isinstance(node, Ellipsis):
#        elif isinstance(node, Exec):
#            return Exec(self.replace(node.expr), self.replace(node.locals), self.replace(node.globals))
#        elif isinstance(node, For):
#            return For(self.replace(node.assign), self.replace(node.list), self.replace(node.body), self.replace(node.else_))
#        elif isinstance(node, From):
#            name='%s.py' % node.modname
#            if not os.path.exists(name):
#                name=os.path.join(pyastra.ports.pic14.__path__[0], name)
#            root=compiler.parseFile(name)
#            return self.replace(root)
#        elif isinstance(node, Function):
#            return Function(self.replace(node.name), self.replace(node.argnames), self.replace(node.defaults), node.flags, node.doc, self.replace(node.code))
#        elif isinstance(node, Getattr):
#            return Getattr(self.replace(node.expr), self.replace(node.attrname))
#        elif isinstance(node, Global):
#            return Global(self.replace(node.names))
#        elif isinstance(node, If):
#            return If(self.replace(node.tests), self.replace(node.else_))
#        elif isinstance(node, Import):
#            return Import(self.replace(node.names))
#        elif isinstance(node, Invert):
#            return Invert(self.replace(node.expr))
#        elif isinstance(node, Keyword):
#            return Keyword(self.replace(node.name), self.replace(node.expr))
#        elif isinstance(node, Lambda):
#            return Lambda(self.replace(node.argnames), self.replace(node.defaults), node.flags, self.replace(node.code))
#        elif isinstance(node, LeftShift):
#            return LeftShift((self.replace(node.left), self.replace(node.right)))
#        elif isinstance(node, List):
#            return List(self.replace(node.nodes))
#        elif isinstance(node, ListComp):
#            return ListComp(self.replace(node.expr), self.replace(node.quals))
#        elif isinstance(node, ListCompFor):
#            return ListCompFor(self.replace(node.assign), self.replace(node.list), self.replace(node.ifs))
#        elif isinstance(node, ListCompIf):
#            return ListCompIf(self.replace(node.test))
#        elif isinstance(node, Mod):
#            return Mod((self.replace(node.left), self.replace(node.right)))
#        elif isinstance(node, Module):
#            return Module(node.doc, self.replace(node.node))
#        elif isinstance(node, Mul):
#            return Mul((self.replace(node.left), self.replace(node.right)))
#        elif isinstance(node, Name):
#            if node.name in self.aliases:
#                return Name(self.aliases[node.name])
#            else:
#                return Name(self.replace(node.name))
#        elif isinstance(node, Not):
#            return Not(self.replace(node.expr))
#        elif isinstance(node, Or):
#            return Or(self.replace(node.nodes))
##        elif isinstance(node, Pass):
#        elif isinstance(node, Power):
#            return Power((self.replace(node.left), self.replace(node.right)))
#        elif isinstance(node, Print):
#            return Print(self.replace(node.nodes), self.replace(node.dest))
#        elif isinstance(node, Printnl):
#            return Printnl(self.replace(node.nodes), self.replace(node.dest))
#        elif isinstance(node, Raise):
#            return Raise(self.replace(node.expr1), self.replace(node.expr2), self.replace(node.expr3))
#        elif isinstance(node, Return):
#            return Return(self.replace(node.value))
#        elif isinstance(node, RightShift):
#            return RightShift((self.replace(node.left), self.replace(node.right)))
#        elif isinstance(node, Slice):
#            return Slice(self.replace(node.expr), node.flags, self.replace(node.lower), self.replace(node.upper))
#        elif isinstance(node, Sliceobj):
#            return Sliceobj(self.replace(node.nodes))
#        elif isinstance(node, Stmt):
#            return Stmt(self.replace(node.nodes))
#        elif isinstance(node, Sub):
#            return Sub((self.replace(node.left), self.replace(node.right)))
#        elif isinstance(node, Subscript):
#            return Subscript(self.replace(node.expr), node.flags, self.replace(node.subs))
#        elif isinstance(node, TryExcept):
#            return TryExcept(self.replace(node.body), self.replace(node.handlers), self.replace(node.else_))
#        elif isinstance(node, TryFinally):
#            return TryFinally(self.replace(node.body), self.replace(node.final))
#        elif isinstance(node, Tuple):
#            return Tuple(self.replace(node.nodes))
#        elif isinstance(node, UnaryAdd):
#            return UnaryAdd(self.replace(node.expr))
#        elif isinstance(node, UnarySub):
#            return UnarySub(self.replace(node.expr))
#        elif isinstance(node, While):
#            return While(self.replace(node.test), self.replace(node.body), self.replace(node.else_))
#        elif isinstance(node, Yield):
#            return Yield(self.replace(node.value))
#        else:
#            return node
        
