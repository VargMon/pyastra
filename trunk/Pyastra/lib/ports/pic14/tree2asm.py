############################################################################
# $Id$
#
# Description: pic14 tree to assemler convertor. Pyastra project.
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


import types, compiler, sys, os.path, pyastra.ports.pic14
from compiler.ast import *

class tree2asm:
    body=''
    stack=-1
    dikt={}
    no_bank_cmds=('addlw', 'andlw', 'call', 'goto', 'iorlw', 'movlw', 'retlw',
                  'sublw', 'xorlw')
    lbl_stack=[]
    label=-1
    funcs={}
    asm=0
    error='Error'
    warning='Warning'
    message='Message'
    ram_usage=0
    infunc=0
    
    def __init__(self, ICD, op_speed, PROC, say):
        self.ICD=ICD
        self.op_speed=op_speed
        self.PROC=PROC
        self.procmod = __import__('pyastra.ports.pic14.procs.%s' %PROC, globals(), locals(), '*')
        self.hdikt = self.procmod.hdikt
        self.pages = self.procmod.pages
        self.banks = self.procmod.banks
        self.shareb = self.procmod.shareb
        self.say = say
        
        self.max_ram=0
        for i in self.banks:
            self.max_ram += i[1] - i[0] + 1
        
        self.max_instr=0
        for i in self.pages:
            self.max_instr += i[1] - i[0] + 1
    
    def convert(self, node):
        self.head="""
\tprocessor\t%s
\t#include\tp%s.inc
""" % (self.PROC, self.PROC)
        self.body='\n\torg\t0x0\n'
        
        if self.ICD:
            self.body+='\tnop\n'
        
        self.body+="""
\tgoto\tmain

\torg\t%s
main
""" % hex(self.pages[0][0])
        
        if self.ICD:
            self.cvar=[0x21]
            self.instr=3
        else:
            self.cvar=[0x20]
            self.instr=2
            
        self._convert(From('builtins', [('*', None)]))
        self.asm=0
        
        self._convert(node)
        
        if self.ICD:
            self.ram_usage += 1

        self.body += '\n\tgoto\t$\n'
            
        ftest=0
        self.tail=fbuf=''
        for i in self.funcs:
            if not self.funcs[i][1]:
                print 'Undefined function call: %s' % i
            if self.funcs[i][3]:
                ftest=1
                fbuf = self.funcs[i][1]
                self.instr += self.funcs[i][2]
                
        if ftest:
            self.tail += "\n;\n; SUBROUTINES\n;\n\n%s" % fbuf
            
        self.tail += "\n\tend\n"
        
    def _convert(self, node):
        if node==None:
            return
        elif isinstance(node, list):
            for n in node:
                self._convert(n)
        elif isinstance(node, Add):
            self._convert(node.left)
            buf=self.push()
            self.app('movwf', buf)
            self._convert(node.right)
            self.app('addwf', buf, 'w')
            self.pop()
        elif isinstance(node, And):
            end_lbl=self.getLabel()
            for n in xrange(len(node.nodes)):
                self._convert(node.nodes[n])
                if n+1 != len(node.nodes):
                    self.app('btfss', 'STATUS', 'Z')
                    self.app('goto', end_lbl)
            self.app(end_lbl, verbatim=1)
#       elif isinstance(node, AssAttr):
#       elif isinstance(node, AssList):
        elif isinstance(node, AssName):
            if node.flags=='OP_ASSIGN':
                if node.name in self.hdikt:
                    name=node.name
                else:
                    name='_'+node.name
                    self.malloc(name)
                self.app('movwf', name)
            elif node.flags=='OP_DELETE':
                self.free('_'+node.name)
            else:
                self.say('%s flag is not supported while.' % node.flags, node.lineno)
#       elif isinstance(node, AssTuple):
#       elif isinstance(node, Assert):
        elif isinstance(node, Assign):
            all_names=1
            any_sscr=0
            all_sscr=1
            for n in node.nodes:
                if not isinstance(n, AssName):
                    all_names=0
                if isinstance(n, Subscript):
                    any_sscr=1
                else:
                    all_sscr=0
                    
            if all_names and isinstance(node.expr, Const) and node.expr.value == 0:
                for n in node.nodes:
                    if n.name in self.hdikt:
                        name=n.name
                    else:
                        name='_'+n.name
                        self.malloc(name)
                    self.app('clrf', name)
            elif any_sscr:
                if not all_sscr:
                    self.say('mixing bit and byte assign is not supported.', node.lineno)
                elif not isinstance(node.expr, Const):
                    self.say('Bits are noted by constants only (0 for 0, other for 1).', node.lineno)
                else:
                    if node.expr.value:
                        oper='bsf'
                    else:
                        oper='bcf'
                        
                    for n in node.nodes:
                        if not isinstance(n.expr, Name):
                            self.say('Bit assign may be applied to bytes only.', node.lineno)
                        else:
                            name=n.expr.name
                            if name in self.hdikt:
                                pass
                            else:
                                name='_'+name
                                self.malloc(name)
                            for i in n.subs:
                                if not isinstance(i, Const):
                                    self.say('Only constant indices are supported while.', node.lineno)
                                else:
                                    self.app(oper, name, str(i.value))
            else:
                self._convert(node.expr)
                
                for n in node.nodes:
                    self._convert(n)
        elif isinstance(node, AugAssign):
                if not isinstance(node.node, Name):
                    self.say('assign only to a variable is not supported while.', node.lineno)
                    
                if node.op == '+=':
                    self._convert(node.expr)
                    self.app('addwf', node.node.name, 'f')
                if node.op == '-=':
                    self._convert(node.expr)
                    self.app('subwf', node.node.name, 'f')
                elif node.op == '*=':
                    self._convert(Mul((node.node, node.expr)))
                    self.app('movwf', node.node.name, 'f')
                elif node.op == '/=':
                    self._convert(Div((node.node, node.expr)))
                    self.app('movwf', node.node.name, 'f')
                elif node.op == '%=':
                    self._convert(Mod((node.node, node.expr)))
                    self.app('movwf', node.node.name, 'f')
                elif node.op == '**=':
                    self._convert(Power((node.node, node.expr)))
                    self.app('movwf', node.node.name, 'f')
                elif node.op == '>>=':
                    self._convert(RightShift((node.node, node.expr)))
                    self.app('movwf', node.node.name, 'f')
                elif node.op == '<<=':
                    self._convert(LeftShift((node.node, node.expr)))
                    self.app('movwf', node.node.name, 'f')
                elif node.op == '&=':
                    self._convert(node.expr)
                    self.app('andwf', node.node.name, 'f')
                elif node.op == '^=':
                    self._convert(node.expr)
                    self.app('xorwf', node.node.name, 'f')
                elif node.op == '|=':
                    self._convert(node.expr)
                    self.app('iorwf', node.node.name, 'f')
                else:
                    self.say('augmented assign %s is not supported while.' % node.op, node.lineno)
                    
#      elif isinstance(node, Backquote):
        elif isinstance(node, Bitand):
            buf=self.push()
            self._convert(node.nodes[0])
            self.app('movwf', buf)
            for n in node.nodes[1:-1]:
                self._convert(n)
                self.app('andwf', buf, 'f')
            self._convert(node.nodes[-1])
            self.app('andwf', buf, 'w')
            self.pop()
        elif isinstance(node, Bitor):
            buf=self.push()
            self._convert(node.nodes[0])
            self.app('movwf', buf)
            for n in node.nodes[1:-1]:
                self._convert(n)
                self.app('iorwf', buf, 'f')
            self._convert(node.nodes[-1])
            self.app('iorwf', buf, 'w')
            self.pop()
        elif isinstance(node, Bitxor):
            buf=self.push()
            self._convert(node.nodes[0])
            self.app('movwf', buf)
            for n in node.nodes[1:-1]:
                self._convert(n)
                self.app('xorwf', buf, 'f')
            self._convert(node.nodes[-1])
            self.app('xorwf', buf, 'w')
            self.pop()
        elif isinstance(node, Break):
            self.app('goto', self.lbl_stack[-1][1])
        elif isinstance(node, CallFunc):
            if node.star_args or node.dstar_args:
                self.say('*-args and **-args are not supported while')
                
            if not isinstance(node.node, Name):
                self.say('only functions are callable while')

            if node.node.name == 'asm':
                if not (2 <= len(node.args) <= 3 and isinstance(node.args[0], Const) and isinstance(node.args[1], Const)):
                    self.say('asm function has the following syntax: asm(code, instr_count [, (local_var1, local_var2, ...)])', exit_status=2)
                    
                if len(node.args) > 2:
                    if not isinstance(node.args[2], Tuple):
                        self.say('asm function has the following syntax: asm(code, instr_count [, (local_var1, local_var2, ...)])', exit_status=2)
                    for i in node.args[2].nodes:
                        if not isinstance(i, Const):
                            self.say('Local variables names must be constant strings.', exit_status=2)
                        self.malloc(i.value, 1)
                    
                self.app('; -- Verbatim inclusion:\n%s\n; -- End of verbatim inclusion\n' % node.args[0].value, verbatim=1)
                self.instr += node.args[1].value
                self.asm=1
            elif node.node.name == 'halt':
                if len(node.args) != 0:
                    self.say('halt() function takes no arguments', exit_status=2)
                self.app('goto', '$')
            elif node.node.name == 'fbin':
                if len(node.args) != 1 or not isinstance(node.args[0], Const) or not isinstance(node.args[0].value, str):
                    self.say('fbin(\'0101 0101\') function takes only one argument: binary number', exit_status=2)
                
                val=0
                for i in node.args[0].value:
                    if i != ' ':
                        val=val << 1
                        if i == '1':
                            val+=int(i)
                        elif i != '0':
                            self.say('fbin(\'0101 0101\') function takes only one argument: binary number', exit_status=2)
                    
                self._convert(Const(val))
            else:
                if node.node.name not in self.funcs:
                    self.say('function %s is not defined before call (this is not supported while)' % node.node.name, node.lineno, exit_status=1)
                    args=[]
                    self.funcs[node.node.name]=[node.args, None, None, 1, '']
                else:
                    self.funcs[node.node.name][3]=1
                    
                if  len(self.funcs[node.node.name][0]) != len(node.args):
                    self.say('function %s takes exactly %g argument(s)' % (node.name, len(self.funcs[node.name][0])), exit_status=2)
                             
                for i in xrange(len(node.args)):
                    (aname, val)=(self.funcs[node.node.name][0][i], node.args[i])
                    self._convert(val)
                    self.app('movwf', '_'+aname)
                self.app('call', 'func_%s' % node.node.name)
                    
##      elif isinstance(node, Class):
        elif isinstance(node, Compare):
            if len(node.expr.ops) != 1:
                self.say('Currently multiple comparisions are not supported', node.lineno)
            buf = self.push()
            nodes=node.expr.ops
            if nodes[0][0]=='<':
                lbl_false=self.getLabel()
                self._convert(node.expr)
                self.app('movwf', buf)
                self._convert(nodes[0][1])
                self.app('subwf', buf, 'w') # node.expr - nodes[0][1] should be < 0 (Z=0 and C=0)
                self.app('btfsc', 'STATUS', 'Z')
                self.app('goto', lbl_false) # node.expr = nodes[0][1]
                self.app('bcf', 'STATUS', 'Z') # true
                self.app('btfsc', 'STATUS', 'C')
                self.app(lbl_false, verbatim=1)
                self.app('bsf', 'STATUS', 'Z') # false
            elif nodes[0][0]=='>':
                lbl_false=self.getLabel()
                self._convert(node.expr)
                self.app('movwf', buf)
                self._convert(nodes[0][1])
                self.app('subwf', buf, 'w') # node.expr - nodes[0][1] should be > 0 (Z=0 and C=1)
                self.app('btfsc', 'STATUS', 'Z')
                self.app('goto', lbl_false) # node.expr = nodes[0][1]
                self.app('bcf', 'STATUS', 'Z') # true
                self.app('btfss', 'STATUS', 'C')
                self.app(lbl_false, verbatim=1)
                self.app('bsf', 'STATUS', 'Z') # false
            elif nodes[0][0]=='==':
                self._convert(node.expr)
                self.app('movwf', buf)
                self._convert(nodes[0][1])
                self.app('subwf', buf, 'w')
                self.app('comf', buf, 'w')
            elif nodes[0][0]=='<=':
                lbl_true=self.getLabel()
                self._convert(node.expr)
                self.app('movwf', buf)
                self._convert(nodes[0][1])
                self.app('subwf', buf, 'w') # node.expr - nodes[0][1] should be <= 0 (Z=1 or C=0)
                self.app('btfsc', 'STATUS', 'Z')
                self.app('goto', lbl_true) # node.expr = nodes[0][1]
                self.app('bsf', 'STATUS', 'Z') # false
                self.app('btfss', 'STATUS', 'C')
                self.app(lbl_true, verbatim=1)
                self.app('bcf', 'STATUS', 'Z') # true
            elif nodes[0][0]=='>=':
                lbl_true=self.getLabel()
                self._convert(node.expr)
                self.app('movwf', buf)
                self._convert(nodes[0][1])
                self.app('subwf', buf, 'w') # node.expr - nodes[0][1] should be >= 0 (Z=1 or C=1)
                self.app('btfsc', 'STATUS', 'Z')
                self.app('goto', lbl_true) # node.expr = nodes[0][1]
                self.app('bsf', 'STATUS', 'Z') # false
                self.app('btfsc', 'STATUS', 'C')
                self.app(lbl_true, verbatim=1)
                self.app('bcf', 'STATUS', 'Z') # true
            elif nodes[0][0]=='!=':
                self._convert(node.expr)
                self.app('movwf', buf)
                self._convert(nodes[0][1])
                self.app('subwf', buf, 'w')
##            elif nodes[0][0]=='is':
##            elif nodes[0][0]=='is not':
##            elif nodes[0][0]=='in':
##            elif nodes[0][0]=='not in':
            else:
                self.say('comparision %s is not supported while.' % node.op, node.lineno)
                    
            self.pop()
        elif isinstance(node, Const):
            self.app('movlw', self.formatConst(node.value))
            buf=self.push()
            self.app('movwf', buf)
            self.pop()
        elif isinstance(node, Continue):
            self.app('goto', self.lbl_stack[-1][0])
##      elif isinstance(node, Dict):
        elif isinstance(node, Discard):
            self._convert(node.expr)
        elif isinstance(node, Div):
            self._convert(Discard(CallFunc(Name('div'), [node.left, node.right], None, None)))
##      elif isinstance(node, Ellipsis):
##      elif isinstance(node, Exec):
        elif isinstance(node, For):
            if not (isinstance(node.list, CallFunc) and
                    isinstance(node.list.node, Name) and
                    node.list.node.name=='xrange' and
                    len(node.list.args)==2 and
                    node.list.star_args==None and
                    node.list.dstar_args==None):
                self.say('only "for <var> in xrange(<from>, <to>)" for statement is supported while', node.lineno)
                return
            cntr = node.assign.name
            if cntr not in self.hdikt:
                cntr = '_'+cntr
            self._convert(Assign([node.assign], node.list.args[0]))
            limit = self.push()
            self._convert(node.list.args[1])
            self.app('movwf', limit)
            
            lbl_beg=self.getLabel()
            lbl_else=self.getLabel()
            lbl_cont=self.getLabel()
            if node.else_ != None:
                lbl_end=self.getLabel()
            else:
                lbl_end=lbl_else
            self.lbl_stack.append((lbl_cont, lbl_end))
            self.app('\n%s' % lbl_beg, verbatim=1)
            
            self.app('movf', limit, 'w')
            self.app('subwf', cntr, 'w')
            self.app('btfsc', 'STATUS', 'Z')
            self.app('goto', lbl_end)
            self.app('btfsc', 'STATUS', 'C') #skip if cntr - limit <= 0
            self.app('goto', lbl_else)
            
            self._convert(node.body)
            
            self.app('\n%s' % lbl_cont, verbatim=1)
            
            self.app('incf', cntr, 'f')
            self.app('goto', lbl_beg)
            
            if node.else_ != None:
                self.app('\n%s' % lbl_else, verbatim=1)
                self._convert(node.else_)
            
            self.app('\n%s' % lbl_end, verbatim=1)
            self.pop()
            del self.lbl_stack[-1]
        elif isinstance(node, From):
            if node.names != [('*', None)]:
                self.say('only "from <module_name> import *" input statement is supported while', node.lineno)
                return
            name='%s.py' % node.modname
            if not os.path.exists(name):
                name=os.path.join(pyastra.ports.pic14.__path__[0], name)
            root=compiler.parseFile(name)
            self._convert(root)
        elif isinstance(node, Function):
            used=0
            if (node.name in self.funcs):
                if self.funcs[node.name][1]:
                    self.say('function %s is already defined.' % node.name, exit_status=2)
                else:
                    if len(self.funcs[node.name][0])==len(node.argnames):
                        self.say('function %s takes exactly %g arguments' % (node.name, len(node.argnames)), exit_status=2)
                    used=1
                    
            if node.flags:
                self.say('function flags are not supported while.')
                
            if node.defaults:
                self.say('function defaults are not supported while.')
                
            for a in node.argnames:
                self.malloc('_'+a, 1)
                
            self.tbody=self.body
            self.tinstr=self.instr
            self.infunc=1
            self.body='\n;\n; * Function %s *\n;\n' % node.name
            self.instr=0
            self.app('func_%s\n' % node.name, verbatim=1)
            self._convert(node.code)
            
            if not isinstance(node.code.nodes[-1], Return):
                self.app('return')
                
            self.app(';\n; * End of function %s *\n;' % node.name, verbatim=1)
            self.infunc=0
            self.funcs[node.name]=[node.argnames, self.body, self.instr, used, self.head]
            self.instr=self.tinstr
            self.body=self.tbody
            del self.tinstr, self.tbody
#       elif isinstance(node, Getattr):
#       elif isinstance(node, Global):
        elif isinstance(node, If):
            self.app(verbatim=1)
            
            for n in node.tests:
                self._convert(n[0])
                label=self.getLabel()
                self.app('btfsc', 'STATUS', 'Z')
                self.app('goto', label)
                self._convert(n[1])
                self.app('%s' % label, verbatim=1)
            self._convert(node.else_)
#       elif isinstance(node, Import):
        elif isinstance(node, Invert):
            self._convert(node.expr)
            buf=self.push()
            self.app('movwf', buf)
            self.app('comf', buf, 'w')
            self.pop()
#       elif isinstance(node, Keyword):
#       elif isinstance(node, Lambda):
        elif isinstance(node, LeftShift):
            if isinstance(node.right, Const) and self.op_speed:
                buf=self.push()
                self._convert(node.left)
                self.app('movwf', buf)
                for i in xrange(node.right.value[:-1]):
                    self.app('rlf', buf, 'f')
                self.app('rlf', buf, 'w')
                self.pop()
            else:
                self._convert(Discard(CallFunc(Name('lshift'), [node.left, node.right], None, None)))
                
#       elif isinstance(node, List):
#       elif isinstance(node, ListComp):
#       elif isinstance(node, ListCompFor):
#       elif isinstance(node, ListCompIf):
        elif isinstance(node, Mod):
            self._convert(Discard(CallFunc(Name('mod'), [node.left, node.right], None, None)))
        elif isinstance(node, Module):
            self._convert(node.node)
        elif isinstance(node, Mul):
            self._convert(Discard(CallFunc(Name('mul'), [node.left, node.right], None, None)))
        elif isinstance(node, Name):
            if '_'+node.name in self.dikt:
                self.app('movf', '_'+node.name, 'w')
            elif node.name in self.hdikt:
                self.app('movf', node.name, 'w')
            else:
                self.say('variable %s not initialized' % node.name, node.lineno)
        elif isinstance(node, Not):
            lbl1=self.getLabel()
            lbl_end=self.getLabel()
            self._convert(node.expr)
            self.app('btfsc', 'STATUS', 'Z')
            self.app('goto', lbl1)
            self.app('movlw', '0')
            self.app('goto', lbl_end)
            self.app(lbl1, verbatim=1)
            self.app('movlw', '1')
            self.app(lbl_end, verbatim=1)
        elif isinstance(node, Or):
            lbl_end=self.getLabel()
            for n in xrange(len(node.nodes)):
                self._convert(node.nodes[n])
                if n+1 != len(node.nodes):
                    self.app('btfsc', 'STATUS', 'Z')
                    self.app('goto', lbl_end)
            self.app(lbl_end, verbatim=1)
        elif isinstance(node, Pass):
            #self.app('nop')
            pass
        elif isinstance(node, Power):
            self._convert(Discard(CallFunc(Name('mul'), [node.left, node.right], None, None)))
#       elif isinstance(node, Print):
#       elif isinstance(node, Printnl):
#       elif isinstance(node, Raise):
        elif isinstance(node, Return):
            if not (isinstance(node.value, Const) and node.value.value==None):
                self._convert(node.value)
            self.app('return')
        elif isinstance(node, RightShift):
            if isinstance(node.right, Const) and self.formatConst(node.right.value)!=-1 and (node.right.value < 8 or self.op_speed):
                buf=self.push()
                self._convert(node.left)
                self.app('movwf', buf)
                for i in xrange(node.right.value):
                    self.app('rrf', buf, 'w')
                    
                self.app('rrf', buf, 'f')
                self.pop()
            else:
                self._convert(Discard(CallFunc(Name('rshift'), [node.left, node.right], None, None)))
#       elif isinstance(node, Slice):
#       elif isinstance(node, Sliceobj):
        elif isinstance(node, Stmt):
            self._convert(node.nodes)
        elif isinstance(node, Sub):
            self._convert(node.left)
            buf=self.push()
            self.app('movwf', buf)
            self._convert(node.right)
            self.app('subwf', buf, 'w')
            self.pop()
        elif isinstance(node, Subscript):
            if not isinstance(node.expr, Name):
                self.say('Bit assign may be applied to bytes only.', node.lineno)
            elif len(node.subs) != 1:
                self.say('More than one subscripts are not fully supported while.', node.lineno)
            elif not node.flags=='OP_APPLY':
                self.say('Unsupported flag: %s.' % node.flags, node.lineno)
            else:
                name=node.expr.name
                if name in self.hdikt:
                    pass
                else:
                    name='_'+name
                    self.malloc(name)
                if not isinstance(node.subs[0], Const):
                    self.say('Only constant indices are supported while.', node.lineno)
                else:
                    self.app('movlw', '.0')
                    self.app('btfsc', name, str(node.subs[0].value))
                    self.app('movlw', '.1')
#       elif isinstance(node, TryExcept):
#       elif isinstance(node, TryFinally):
#       elif isinstance(node, Tuple):
        elif isinstance(node, UnaryAdd):
            self._convert(node.expr)
#       elif isinstance(node, UnarySub):
        elif isinstance(node, While):
            lbl_beg=self.getLabel()
            lbl_else=self.getLabel()
            if node.else_ != None:
                lbl_end=self.getLabel()
            else:
                lbl_end=lbl_else
            self.lbl_stack.append((lbl_beg, lbl_end))
            self.app('\n%s' % lbl_beg, verbatim=1)
            self._convert(node.test)
            self.app('btfsc', 'STATUS', 'Z')
            self.app('goto', '%s\n' % lbl_else)
            self._convert(node.body)
            self.app('goto', lbl_beg)
            if node.else_ != None:
                self.app('\n%s' % lbl_else, verbatim=1)
                self._convert(node.else_)
            self.app('\n%s' % lbl_end, verbatim=1)
            del self.lbl_stack[-1]
#       elif isinstance(node, Yield):
        else:
            self.say('"%s" node is not supported while.' % node.__class__.__name__, node.lineno)
            
    def formatConst(self, c):
        if type(c) == types.IntType and 0 <= int(c) <= 0xff:
            return hex(c)
        elif type(c) == types.StringType and len(c)==1:
            return "'%s'" % c
        else:
            self.say('%s type constant is not supported while.' % c.__class__.__name__)
            return c
            
    def push(self):
        self.stack += 1
        name='stack%g' % self.stack
        self.malloc(name)
        return name
        
    def pop(self):
        pass # this feature is temporary off due to bugs it causes in some cases
        #self.stack -= 1
        #self.free('stack%g' % self.stack)
        
    def getLabel(self):
        self.label += 1
        return 'label%i' % self.label
    
    def malloc(self, name, care=0):
        if name not in self.dikt:
            self.dikt[name]=self.cvar[0]
            if len(self.dikt) > self.ram_usage:
                self.ram_usage=len(self.dikt)
                
            self.head += '%s\tequ\t%s\t;bank %g\n' % (name, hex(self.cvar[0] & 0x7f), self.cvar[0] >> 7 << 7)

            if len(self.cvar) > 1:
                del self.cvar[0]
            else:
                self.cvar[0] += 1
                for i in self.banks:
                    if i[0] <= self.cvar <= i[1]:
                        break
                    elif i[0] > self.cvar:
                        self.cvar=i[0]
                if self.cvar[0] > self.banks[-1][1]:
                    self.say("program does not fit RAM.", exit_status=3)
        elif care:
            self.say("name %s is defined twice!" % name, level=self.warning)

    def free(self, name, care=1):
        if name in self.dikt:
            self.cvar.insert(0, self.dikt[name])
            del self.dikt[name]
        elif care:
            self.say("variable %s can't be deleted before assign!" % name, level=self.warning)

    def bank_by_name(self, name):
        if name in self.dikt:
            self.bank_sel(self.dikt[name] >> 7 << 7)
        elif name in self.hdikt:
            self.bank_sel(self.hdikt[name] >> 7 << 7)
            
    def bank_sel(self, bank):
        if bank and 1:
            self.body += '\tbsf\tSTATUS,\tRP0\n'
        else:
            self.body += '\tbcf\tSTATUS,\tRP0\n'
            
        if bank and 2:
            self.body += '\tbsf\tSTATUS,\tRP1\n'
        else:
            self.body += '\tbcf\tSTATUS,\tRP1\n'
            
        self.instr += 2
        
    def app(self, cmd='', op1=None, op2=None, verbatim=0):
        if verbatim:
            self.body += '%s\n' % (cmd,)
            return
        
        if op1 and (cmd not in self.no_bank_cmds):
            self.bank_by_name(op1)
            
        if op2 != None:
            self.body += '\t%s\t%s,\t%s\n' % (cmd, op1, op2)
        elif op1 != None:
            self.body += '\t%s\t%s\n' % (cmd, op1)
        else:
            self.body += '\t%s\n' % (cmd,)
        self.instr += 1

        if self.instr == self.pages[0][1]:
            self.say('Program does not fit ROM (maybe because while only first ROM page is supported).')
            
    def get_asm(self):
        return self.head + self.body + self.tail
