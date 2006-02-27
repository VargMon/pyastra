############################################################################
# $Id$
#
# Description: pic14 tree to asm convertor. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################
"""
Pic14 tree to assembler convertor.
U{Pyastra project <http://pyastra.sourceforge.net>}.


Namespaces feature implementing plan
====================================
  - Output not to assembler directly, but into object list.
  - Move all memory control to C{MemoryManager} class.
  - Add support of C{CallFunc}, C{Function} and C{Return} nodes.
  - Add support of C{Global} node.
  - Add support of C{From} node.
  - Fix C{asm()} pseudofunction.
  - Generate the head after C{_convert()}.
  - Implement algorithm that will generate the optimal static memory
    allocation.
  - Implement dynamic malloc for recursive functions.
  - Search for cases when dynamic malloc would be more effective rather.
    than static one and implement it.

@author: U{Alex Ziranov <mailto:estyler_at_users_dot_sourceforge_dot_net>}
@copyright: (C) 2004-2006 Alex Ziranov.  All rights reserved.
@license: This program is free software; you can redistribute it and/or
          modify it under the terms of the GNU General Public License as
          published by the Free Software Foundation; either version 2 of
          the License, or (at your option) any later version.
          
          This program is distributed in the hope that it will be useful,
          but WITHOUT ANY WARRANTY; without even the implied warranty of
          MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
          GNU Library General Public License for more details.
          
          You should have received a copy of the GNU General Public
          License along with this program; if not, write to the Free
          Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
          MA 02111-1307, USA.
@contact: U{http://pyastra.sourceforge.net}
@see: L{convertors}
@todo: Finish namespaces implementation.
"""

from compiler.ast import *
import types, compiler, sys, os.path, pyastra.ports.pic14, pyastra.ports.pic14.procs, pyastra
from pyastra import Option, MESSAGE, WARNING, ERROR

converts_from='tree_op'
converts_to='asm'
PORTS=['pic14']


def get_ports():
    """@return: A list of supported ports."""
    return PORTS

def get_procs(port):
    """@return: A list of supported processors."""
    if port in PORTS:
        procs=pyastra.ports.pic14.procs.__all__
        procs=filter(lambda item: item[-1]!='i', procs)
        return procs
    else:
        return []

def get_options():
    """@return: A tuple of Options that the user may send to the function."""
    return (
        Option('Enable ICD support (disabled by default)', lkey='icd'),
        Option('Disable namespaces support (pyastra 0.0.4 compatibility mode)', lkey='disable_ns')
        )

class Convertor:
    """
    Main convertor class
    @see: L{convertors}
    
    @cvar body: List of lines in the body of the generated assembler code.
    @cvar tmp_var: Latest temporary variable number.
    @cvar uvars: User defined variables dictioinary.
    @cvar bank_cmds: Bank-sensitive commands.
    @cvar cond_br_cmds: Conditional branching commands.
    @cvar pagesel_cmds: Page-sensitive commands.
    @cvar no_bank_cmds: Bank-insensitive commands.
    @cvar bank_indep: Common bank-independent registers.
    @cvar lbl_stack: Stack of lables.
    @cvar label: Latest label number.
    @cvar funcs: Dictionary of tuples that represent functions. 
    @cvar verbatim: True if the source code includes verbatim assembler lines.
    @cvar ram_usage: Number of registers used by the compiled program.
    @cvar infunc: True if the convert function on the top is inside the
      function.
    @cvar curr_bank: Current register bank.
    @cvar del_last: Marks the last assembler instruction in the body to be
      deleted.
    @cvar last_bank: Last register bank.
    @cvar prelast_bank: The bank before the last register bank.
    @cvar interr: List of lines in the interrupt handler assembler code.
    @cvar interr_instr: Interrupt handler code instructions counter.
    @cvar in_inter: True if the convert function on the top is inside the
      interrupt handler.
    @cvar inter_ret: Label to go to to return from the interrupt.
    @ivar instr: Instruction counter.
    @cvar last_instr: Last value of the instruction counter.
    @cvar prelast_instr: Last value of the instruction counter.
    @cvar cur_page: Current program memory page.
    @ivar has_errors: True if program has errors.
    @ivar namespace: Current namespace.
    @ivar disable_ns: True if name spaces are disabled.
    @ivar ICD: True if ICD support is on.
    @ivar op_speed: True if generated code should be optimized for speed
    @ivar PROC: Current processor.
    @ivar procmod: Current processor definition module.
    @ivar hdikt: Dictionary of processor-specific register names.
    @ivar pages: Tuple of processor-specific program memory pages.
    @ivar shareb: Tuple processor-specific shared banks.
    @ivar vectors: Tuple of processor-specific ectors.
    @ivar maxram: Amount of memory available for the current processor.
    @ivar head: Header of the assembler file with definitions.
    @ivar tail: Tail of the assembler file with definitions.
    @ivar cvar: Memory map.
    @ivar namespaces_bak: Stack of previous namespaces.
    
    @todo: Refactor some of the variables ond objects (label, ram_usage,
            cvar, Memory map, etc).
    """
    ext='asm'
    meta={}

    body=[]
    tmp_var=-1
    uvars={}
    bank_cmds=('addwf', 'andwf', 'bcf', 'bsf', 'btfsc', 'btfss', 'clrf',
               'comf', 'decf', 'decfsz', 'incf', 'incfsz', 'iorwf', 'movf',
               'movwf', 'rlf', 'rrf', 'subwf', 'swapf', 'xorwf')
    cond_br_cmds=('btfsc', 'btfss', 'decfsz', 'incfsz')
    pagesel_cmds=('call', 'goto')
    no_bank_cmds=('addlw', 'andlw', 'call', 'clrw', 'clrwdt', 'goto', 'iorlw',
                  'movlw', 'nop', 'retfie', 'retlw', 'return', 'sleep',
                  'sublw', 'xorlw')
    bank_indep=('STATUS', 'FSR', 'PCLATH', 'INTCON', 'PCL')
    lbl_stack=[]
    label=-1
    funcs={}
    verbatim=False
    ram_usage=1
    infunc=False
    curr_bank=None
    del_last=False
    last_bank=prelast_bank=None
    interr = ''
    interr_instr = 0
    in_inter = False
    inter_ret=''
    last_instr=0
    prelast_instr=0
    cur_page=0

    def __init__(self, src, opts):
        global WARNING, ERROR
        self.namespace=''
        self.has_errors=False
        self.modified=False
        self.caller_say=opts['convertor'].say
        self.opts=opts
        if opts.get('port', 'pic14') != 'pic14':
            return
        procs=pyastra.ports.pic14.procs.__all__
        fprocs=filter(lambda item: item[-1]!='i', procs)
        if opts.setdefault('proc', 'pic16f877') not in fprocs:
            self.modified=False
            return
        
        self.data = src

        self.disable_ns=opts['disable_ns']
        
        PROC=opts['proc']
        if opts['icd']:
            if PROC + 'i' not in procs:
                self.say('Seems like microcontroller %s doesn\'t support ICD.' % opts['proc'], ERROR)
                return
            else:
                PROC+='i'
            
        self.ICD=opts['icd']
        self.op_speed=False
        self.PROC=PROC
        self.procmod = __import__('pyastra.ports.pic14.procs.%s' %PROC, globals(), locals(), '*')
        self.hdikt = self.procmod.hdikt
        self.pages = self.procmod.pages
        self.shareb = self.procmod.shareb
        self.vectors = self.procmod.vectors
        self.maxram = self.procmod.maxram
        
        self.max_ram=0
        for i in self.procmod.banks:
            self.max_ram += i[1] - i[0] + 1
        
        self.max_instr=0
        for i in self.pages:
            self.max_instr += i[1] - i[0] + 1
            
        self.convert(src)
        self.data=((""";
; Generated by %s
; infile: %s
;
""" % (pyastra.version, opts.get('infile', 'unknown'))) +
       ''.join([self.head] + self.body + [self.tail]))
        self.meta={
            'instr': self.instr,
            'max_instr': self.max_instr,
            'max_ram': self.max_ram,
            'ram_usage': self.ram_usage,
            'verbatim': self.verbatim
            }

        if not self.has_errors:
            # Print out some statistics
            msg="""
Peak RAM usage: %g byte(s) (%.1f%%)
Program memory usage: %g word(s) (%.1f%%)""" % \
            (self.ram_usage, self.ram_usage*100./self.max_ram,\
             self.instr, self.instr*100./self.max_instr)
            
            if self.verbatim:
                msg+="\nNOTE: statistics includes verbatim data specified in asm function!"

            if opts['icd']:
                msg+="\nNOTE: statistics includes ICD memory usage!"

            self.say(msg)
            self.modified=True

    def say(self, message, level=MESSAGE, line=None):
        global MESSAGE, ERROR
        if level==ERROR:
            self.has_errors=True
        self.caller_say(message, level, line)
    
    def convert(self, node):
        """
        Converts the given tree to assembler. Combinates all the data generated
        by L{_convert()} function.
        @param node: Tree to be converted.
        @type  node: C{Node}
        """
        global WARNING, ERROR
        proc_clean=self.PROC[3:]
        if proc_clean[-1]=='i':
            proc_clean = proc_clean[:-1]
        self.head="""
\tprocessor\t%s
\t#include\tp%s.inc

""" % (proc_clean, proc_clean)
        if self.pages[0][0]>0:
            self.instr = 1
        else:
            self.instr = 0

        self.cvar=MemoryMap(self.procmod.banks)
        if self.ICD:
            self.instr += 1
            
        # Import builtins
        name=os.path.join(pyastra.ports.pic14.__path__[0], 'builtins.py')
        c=pyastra.Pyastra(name, self.opts['caller_select'], self.say, trg_t=['tree_op'], opts=self.opts.copy(), src_t='file')
        # FIXME: Correct code for the case when convert() returns more
        #        than one root
        # Fix the same code in py2tree
        root=c.convert()[0].data
        self._convert(root)

        self.verbatim=False
        
        self.namespaces_bak=[]
        addrs=[]
        if node.interrupts_on:
            for part in self.shareb:
                #Check that part is not SFR
                addrs=[]
                in_bank = 0
                for bank in self.procmod.banks:
                    if bank[0] <= part[0][0] <= bank[1]:
                        in_bank = 1
                        break
                    
                if not in_bank or part[0][1]-part[0][0]+1 < 4:
                    continue

                in_banks_until = -1
                
                for sub in part:
                    if sub[0] >> 7 == in_banks_until + 1:
                        in_banks_until += 1
                    else:
                        break
                
                if in_banks_until == self.maxram >> 7:
                    for i in xrange(part[0][0], part[0][1]+1):
                        if not self.cvar.is_reserved(i):
                            addrs += [i]
                            if len(addrs) == 5:
                                break
                    if len(addrs) == 5:
                        break
        if len(addrs)==5:
            self.malloc('var_w_temp', addr=addrs[0])
            self.malloc('var_status_temp', addr=addrs[1])
            self.malloc('var_pclath_temp', addr=addrs[2])
            self.malloc('var_test_temp', addr=addrs[3])
            self.malloc('var_test', addr=addrs[4])
        else:
            self.malloc('var_test')

        self._convert(node)
        
        body_buf = ["""
\terrorlevel\t-302
\terrorlevel\t-306
"""]

        if self.vectors:
            body_buf += ['\n\torg\t%s\n' % hex(self.vectors[0])]
        else:
            body_buf += ['\n\torg\t0x0\n']
        
        if self.ICD:
            body_buf += ['\tnop\n']

        if self.pages[0][0]>0:
            body_buf += ["""
\tgoto\tmain\n"""]
            if self.interr_instr:
                if len(self.pages) > 1:
                    self.interr += """
        movf    var_test_temp,      W
        movwf   var_test
        movf    var_pclath_temp,    W
        movwf   PCLATH
        swapf   var_status_temp,    W
        movwf   STATUS
        swapf   var_w_temp, F
        swapf   var_w_temp, W
        retfie\n"""
                    self.interr_instr += 9
                else:
                    self.interr += """
        movf    var_test_temp,      W
        movwf   var_test
        swapf   var_status_temp,    W
        movwf   STATUS
        swapf   var_w_temp, F
        swapf   var_w_temp, W
        retfie\n"""
                    self.interr_instr += 7
                self.instr += self.interr_instr
                body_buf += ["\n\torg\t%s\n" % hex(self.vectors[1]), self.interr]
            if self.pages[0][0] > self.vectors[1]+self.interr_instr:
                body_buf += ["\n\torg\t%s" % hex(self.pages[0][0])]
            body_buf += ["\nmain\n"]

        self.body = body_buf + self.body
        
        if self.ICD:
            self.ram_usage += 1

        self.body += ['\n\tgoto\t$\n']
        self.instr += 1
            
        ftest=0
        self.tail=fbuf=''
        t_instr = self.pages[0][0]+self.instr
        for i in self.funcs:
            if not self.funcs[i].body:
                self.say('Undefined function call: %s' % i, ERROR)
                return
            if self.funcs[i].is_used:
                ftest=1
                (t_str, t_instr) = self.page_org(t_instr, self.funcs[i].instr)
                fbuf += t_str
                fbuf += self.funcs[i].body
                self.instr += self.funcs[i].instr
                
        if ftest:
            self.tail += "\n;\n; SUBROUTINES\n;\n\n%s" % fbuf
            
        self.tail += "\n\tend\n"
        self.instr=t_instr
        
    def _convert(self, node):
        """
        Recursive convert function.
        
        @param node: Node to be converted.
        @type  node: C{Node}
        @todo: Add new AST Nodes from Python 2.4 as comments.
        """
        # TODO: fix all nodes that require name_with_ns instead of
        #       some variables (usually "name")
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
        elif isinstance(node, And):
            end_lbl=self.getLabel()
            for n in xrange(len(node.nodes)):
                self._convert(node.nodes[n])
                if n+1 != len(node.nodes):
                    self.del_last=False
                    self.app('btfsc', 'STATUS', 'Z')
                    self.app('goto', end_lbl)
            self.del_last=False
            self.app(end_lbl, verbatim=True)
        elif isinstance(node, AssAttr):
            if node.flags=='OP_ASSIGN':
                name=self.get_name(node, malloc=True)
                self.malloc(name)
                self.app('movwf', name)
            else:
                self.say('%s flag is not supported while.' % node.flags, self.lineno(node), ERROR)
#       elif isinstance(node, AssList):
        elif isinstance(node, AssName):
            if node.flags=='OP_ASSIGN':
                if node.name in self.hdikt:
                    name=node.name
                else:
                    name='_'+node.name
                    self.malloc(name)
                self.app('movwf', name)
            else:
                self.say('%s flag is not supported while.' % node.flags, self.lineno(node), ERROR)
#       elif isinstance(node, AssTuple):
#       elif isinstance(node, Assert):
        elif isinstance(node, Assign):
            all_names=1
            any_sscr=0
            all_sscr=1
            for n in node.nodes:
                if not (isinstance(n, AssName) or isinstance(n, AssAttr)):
                    all_names=0
                if isinstance(n, Subscript):
                    any_sscr=1
                else:
                    all_sscr=0
                    
            if all_names and isinstance(node.expr, Const) and node.expr.value == 0:
                for n in node.nodes:
                    name=self.get_name(n, malloc=True)
                        
                    self.app('clrf', name)
            elif any_sscr:
                if not all_sscr:
                    self.say('mixing bit and byte assign is not supported.', ERROR, self.lineno(node))
                elif isinstance(node.expr, Const):
                    if node.expr.value:
                        oper='bsf'
                    else:
                        oper='bcf'
                        
                    for n in node.nodes:
                        try:
                            name=self.get_name(n.expr)
                        except:
                            self.say('Bit assign may be applied to plain variables only.', ERROR, self.lineno(node))
                            break

                        for i in n.subs:
                            if isinstance(i, Const):
                                self.app(oper, name, str(i.value))
                            elif isinstance(i, Name) and i.name in self.hdikt:
                                # FIXME: Check that i.name references to a bit
                                self.app(oper, name, str(i.name))
                            elif oper=='bsf':
                                self._convert(AugAssign(n.expr, '|=', LeftShift((Const(1), i))))
                            else:
                                self._convert(AugAssign(n.expr, '&=', Invert(LeftShift((Const(1), i)))))

                elif isinstance(node.expr, Subscript) and len(node.expr.subs) == 1 and isinstance(node.expr.subs[0], Const):
                    # FIXME: expressions with a dot (like module.var) may not
                    #        work here!
                    lbl_else=self.getLabel()
                    lbl_exit=self.getLabel()

                    ename=self.get_name(node.expr.expr, malloc=True)
                    self.app('btfsc', ename, str(node.expr.subs[0].value))
                    self.app('goto', lbl_else)
                    for n in node.nodes:
                        if not (isinstance(n.expr, Name) or \
                                isinstance(n.expr, Getattr)):
                            self.say('Bit assign may be applied to plain numbers only.', ERROR, self.lineno(node))
                        else:
                            name=self.get_name(n.expr, malloc=True)
                            for i in n.subs:
                                if isinstance(i, Const):
                                    self.app('bcf', name, str(i.value))
                                elif isinstance(i, Name) and i.name in self.hdikt:
                                    self.app('bcf', name, str(i.name))
                                else:
                                    self.say('Only constant indices are supported while in some cases.', ERROR, self.lineno(node))
                                    return
                    self.app('goto', lbl_exit)
                    self.app('\n%s' % lbl_else, verbatim=True)
                    for n in node.nodes:
                        if not isinstance(n.expr, Name):
                            self.say('Bit assign may be applied to bytes only.', ERROR, self.lineno(node))
                        else:
                            name=self.get_name(n.expr, malloc=True)
                            for i in n.subs:
                                if isinstance(i, Const):
                                    self.app('bsf', name, str(i.value))
                                elif isinstance(i, Name) and i.name in self.hdikt:
                                    self.app('bsf', name, str(i.name))
                                else:
                                    self.say('Only constant indices are supported while.', ERROR, self.lineno(node))
                    self.app('\n%s' % lbl_exit, verbatim=True)
                else:
                    self._convert(If([(node.expr,
                        Stmt([Assign(node.nodes, Const(1))]))],
                        Stmt([Assign(node.nodes, Const(0))])))
            else:
                self._convert(node.expr)
                
                for n in node.nodes:
                    self._convert(n)
        elif isinstance(node, AugAssign):
                try:
                    name=self.get_name(node.node)
                except:
                    self.say('assign only to a variable is not supported while.', ERROR, self.lineno(node))

                if (name not in self.hdikt) \
                        and (name not in self.uvars):
                    self.say('variable %s not initialized' % name, ERROR, self.lineno(node))
                    
                if node.op == '+=':
                    self._convert(node.expr)
                    self.app('addwf', name, 'f')
                elif node.op == '-=':
                    self._convert(node.expr)
                    self.app('subwf', name, 'f')
                elif node.op == '*=':
                    self._convert(Mul((node.node, node.expr)))
                    self.app('movwf', name, 'f')
                elif node.op == '/=':
                    self._convert(Div((node.node, node.expr)))
                    self.app('movwf', name, 'f')
                elif node.op == '%=':
                    self._convert(Mod((node.node, node.expr)))
                    self.app('movwf', name, 'f')
                elif node.op == '**=':
                    self._convert(Power((node.node, node.expr)))
                    self.app('movwf', name, 'f')
                elif node.op == '>>=':
                    self._convert(RightShift((node.node, node.expr)))
                    self.app('movwf', name, 'f')
                elif node.op == '<<=':
                    self._convert(LeftShift((node.node, node.expr)))
                    self.app('movwf', name, 'f')
                elif node.op == '&=':
                    self._convert(node.expr)
                    self.app('andwf', name, 'f')
                elif node.op == '^=':
                    self._convert(node.expr)
                    self.app('xorwf', name, 'f')
                elif node.op == '|=':
                    self._convert(node.expr)
                    self.app('iorwf', name, 'f')
                else:
                    self.say('augmented assign %s is not supported while.' % node.op, ERROR, self.lineno(node))
                    
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
        elif isinstance(node, Bitor):
            buf=self.push()
            self._convert(node.nodes[0])
            self.app('movwf', buf)
            for n in node.nodes[1:-1]:
                self._convert(n)
                self.app('iorwf', buf, 'f')
            self._convert(node.nodes[-1])
            self.app('iorwf', buf, 'w')
        elif isinstance(node, Bitxor):
            buf=self.push()
            self._convert(node.nodes[0])
            self.app('movwf', buf)
            for n in node.nodes[1:-1]:
                self._convert(n)
                self.app('xorwf', buf, 'f')
            self._convert(node.nodes[-1])
            self.app('xorwf', buf, 'w')
        elif isinstance(node, Break):
            self.app('goto', self.lbl_stack[-1][1])
        elif isinstance(node, CallFunc):
            if node.star_args or node.dstar_args:
                self.say('*-args and **-args are not supported while', ERROR)
                
            if isinstance(node.node, Name):
                # TODO: Check whether it requires a namespace fix
                if node.node.name == 'asm':
                    err_mesg='asm function has the following syntax: asm(code [, instr_count [, (local_var1, local_var2, ...)]])'
                    if len(node.args) == 1 and isinstance(node.args[0], Const):
                        self.app('\n; -- Parsed verbatim inclusion:\n', verbatim=True)
                        prev_op=''
                        for s in node.args[0].value.splitlines(1):
                            #FIXME: bad tokenizing in case of "' '" or "','" as constants
                            op=[]
                            for op0 in s.split():
                                for op1 in op0.split(','):
                                    if op1:
                                        op += [op1]
                            comment=''
                            for wn in xrange(len(op)):
                                if op[wn][0]==';':
                                    comment=s[s.find(op[wn]):]
                                    op=op[:wn]
                                    break
                            if not op:
                                self.app(comment, verbatim=True)
                            elif len(op) > 3 or ((op[0] not in self.bank_cmds) and (op[0] not in self.no_bank_cmds)):
                                if s[0].isspace():
                                    self.say('Can\'t parse line in asm function:\n%s' % s, WARNING)
                                    self.verbatim=True
                                    self.last_bank = self.prelast_bank = self.curr_bank=None

                                self.app(s, verbatim=True)
                            else:
                                op[0]=op[0].lower()
                                    
                                if len(op) > 1 and (op[0] in self.bank_cmds or op[0] in self.no_bank_cmds) and op[0][-1] in 'fzcs':
                                    if op[1] not in self.hdikt:
                                        op[1]=self.name_with_ns(op[1])
                                        if op[1] not in self.uvars:
                                            self.malloc(op[1])

                                comment=comment[1:]
                                t_instr=self.instr
                                if len(op)==1:
                                    self.app(op[0], comment=comment)
                                elif len(op)==2:
                                    self.app(op[0], op[1], comment=comment)
                                else:
                                    self.app(op[0], op[1], op[2], comment=comment)

                                if self.instr - t_instr > 1 and prev_op in self.cond_br_cmds:
                                    last=self.body[-1]
                                    del self.body[-1]
                                    lbl_exit=self.getLabel()

                                    if prev_op=='btfsc':
                                        s=self.body[-1]
                                        self.body[-1]=s[:s.find(prev_op)]+'btfss'+s[s.find(prev_op)+5:]
                                        self.app('goto', lbl_exit)
                                    elif prev_op=='btfss':
                                        s=self.body[-1]
                                        self.body[-1]=s[:s.find(prev_op)]+'btfsc'+s[s.find(prev_op)+5:]
                                        self.app('goto', lbl_exit)
                                    else:
                                        lbl_if=self.getLabel()
                                        self.app('goto', lbl_if)
                                        self.app('goto', lbl_exit)
                                        
                                        self.app(lbl_if, verbatim=True)

                                    self.body += [last]
                                    self.app(lbl_exit, verbatim=True)
                                    
                            if op:
                                prev_op=op[0]
                        self.app('\n; -- End of parsed verbatim inclusion\n', verbatim=True)
                    elif not (2 <= len(node.args) <= 3 and isinstance(node.args[0], Const) and isinstance(node.args[1], Const)):
                        self.say(err_mesg, ERRROR)
                        return
                    else:
                        # In not parsed version, namespace isn't taken
                        # into account!
                        self.app('\n\terrorlevel\t+302\n', verbatim=True)
                        if len(node.args) > 2:
                            if not isinstance(node.args[2], Tuple):
                                self.say(err_mesg, ERROR)
                                return
                            else:
                                for i in node.args[2].nodes:
                                    if not isinstance(i, Const):
                                        self.say('Local variables names must be constant strings.', ERROR)
                                        return
                                    self.malloc(i.value, 1)
                        
                        self.app('\n; -- Verbatim inclusion:\n%s\n; -- End of verbatim inclusion\n' % node.args[0].value, verbatim=True)
                        self.instr += node.args[1].value
                        self.verbatim=True
                        self.last_bank = self.prelast_bank = self.curr_bank = None
                        self.app('\n\terrorlevel\t-302\n', verbatim=True)
                    return
                elif node.node.name == 'fbin':
                    if len(node.args) != 1 or not isinstance(node.args[0], Const) or not isinstance(node.args[0].value, str):
                        self.say('fbin(\'0101 0101\') function takes only one argument: binary number', ERROR)
                        return
                    
                    val=0
                    for i in node.args[0].value:
                        if i != ' ':
                            val=val << 1
                            if i == '1':
                                val+=int(i)
                            elif i != '0':
                                self.say('fbin(\'0101 0101\') function takes only one argument: binary number', ERROR)
                                return
                        
                    self._convert(Const(val))
                    return
                else:
                    func_name=node.node.name
                    ns_prefix=''
            elif isinstance(node.node, Getattr):
                func_name=self.get_name(node.node)
                ns_prefix='.'.join(func_name.split('.')[:-1])+'.'
            else:
                self.say('only functions are callable while', ERROR)
                return
            
            if func_name not in self.funcs:
                self.say('function %s is not defined before call (this is not supported while)' % func_name, ERROR, self.lineno(node))
                return
                args=[]
                self.funcs[func_name]=AsmFunction(node.args, is_used = True)
            else:
                self.funcs[func_name].is_used = True
                
            if  len(self.funcs[func_name].args) != len(node.args):
                self.say('function %s requires exactly %g argument(s)' % (func_name, ERROR, len(self.funcs[func_name].args)))
                return
                         
            for i in xrange(len(node.args)):
                (aname, val)=(self.funcs[func_name].args[i], node.args[i])
                self._convert(val)
                self.app('movwf', ns_prefix+'_'+aname)
            self.app('call', 'func_%s' % func_name)
                    
##      elif isinstance(node, Class):
        elif isinstance(node, Compare):
            if len(node.ops) != 1:
                self.say('Currently multiple comparisions are not supported', ERROR, self.lineno(node))
            buf = self.push()
            nodes=node.ops
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
                self.app(lbl_false, verbatim=True)
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
                self.app(lbl_false, verbatim=True)
                self.app('bsf', 'STATUS', 'Z') # false
            elif nodes[0][0]=='==':
                self._convert(node.expr)
                self.app('movwf', buf)
                self._convert(nodes[0][1])
                self.app('subwf', buf, 'w')
                self.app('movf', 'STATUS', 'w')
                self.app('xorlw', '1 << Z')
                self.app('movwf', 'STATUS')
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
                self.app(lbl_true, verbatim=True)
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
                self.app(lbl_true, verbatim=True)
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
                self.say('comparision %s is not supported while.' % node.op, ERROR, self.lineno(node))
                    
        elif isinstance(node, Const):
            self.app('movlw', self.formatConst(node.value))
            self.test()
        elif isinstance(node, Continue):
            self.app('goto', self.lbl_stack[-1][0])
##      elif isinstance(node, Dict):
        elif isinstance(node, Discard):
            if isinstance(node.expr, Const) and node.expr.value==None:
                return
            else:
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
                self.say('only "for <var> in xrange(<from>, <to>)" for statement is supported while', ERROR, self.lineno(node))
                return
            cntr = node.assign.name
            if cntr not in self.hdikt:
                cntr = '_'+cntr
            self._convert(Assign([node.assign], node.list.args[0]))
            
            lbl_beg=self.getLabel()
            lbl_else=self.getLabel()
            lbl_cont=self.getLabel()
            if node.else_ != None:
                lbl_end=self.getLabel()
            else:
                lbl_end=lbl_else

            self.lbl_stack.append((lbl_cont, lbl_end))
                
            if isinstance(node.list.args[1], Const) and node.list.args[1].value==256:
                #skip whole loop if cntr==255
                self.app('movf', cntr, 'w')
                self.app('sublw', '0xff')
                self.app('btfsc', 'STATUS', 'Z')
                self.app('goto', lbl_else)
                
                self.app('\n%s' % lbl_beg, verbatim=True)
                
                self._convert(node.body)
                
                self.app('\n%s' % lbl_cont, verbatim=True)
                
                self.app('incf', cntr, 'f')

                self.app('movf', cntr, 'f')
                self.app('btfss', 'STATUS', 'Z')
                self.app('goto', lbl_beg)
            else:
                limit = self.push()
                self._convert(node.list.args[1])
                self.app('movwf', limit)
                
                self.app('\n%s' % lbl_beg, verbatim=True)
                
                self.app('movf', limit, 'w')
                self.app('subwf', cntr, 'w')
                self.app('btfsc', 'STATUS', 'Z') #skip if cntr - limit != 0
                self.app('goto', lbl_else)
                self.app('btfsc', 'STATUS', 'C') #skip if cntr - limit  < 0
                self.app('goto', lbl_else)
                
                self._convert(node.body)
                
                self.app('\n%s' % lbl_cont, verbatim=True)
                
                self.app('incf', cntr, 'f')
                self.app('goto', lbl_beg)
            
            if node.else_ != None:
                self.app('\n%s' % lbl_else, verbatim=True)
                self._convert(node.else_)
            
            self.app('\n%s' % lbl_end, verbatim=True)
            del self.lbl_stack[-1]
        elif isinstance(node, Function):
            is_used=False
            if self.namespace and node.name != 'on_interrupt':
                func_name='%s._%s' % (self.namespace, node.name)
            else:
                func_name=node.name
                
            if (func_name in self.funcs):
                if self.funcs[func_name].body:
                    self.say('function %s is already defined.' % func_name, ERROR)
                    return
                else:
                    if len(self.funcs[func_name].args)==len(node.argnames):
                        self.say('function %s takes exactly %g arguments' % (func_name, len(node.argnames)), ERROR)
                        return
                    is_used=True
                    
            if node.flags:
                self.say('function flags are not supported while.', ERROR)
                
            if node.defaults:
                self.say('function defaults are not supported while.', ERROR)
                
            for a in node.argnames:
                self.malloc('_'+a, 1)
                
            tbody=self.body
            tinstr=self.instr
            tcurr_bank=self.curr_bank
            tlast_bank=self.last_bank
            tprelast_bank=self.prelast_bank
            
            self.infunc = True
            self.curr_bank = None
            self.last_bank = None
            self.prelast_bank = None
            if func_name == 'on_interrupt':
                self.in_inter=True
                if not self.vectors:
                    self.say('Selected processor does not support interrupts!', ERROR)
                    return
                if not self.uvars.has_key('var_w_temp'):
                    self.say('Pyastra doesn\'t suppoort interrupts for selected processor while.', ERROR)
                    return
                self.inter_ret=self.getLabel()
                if self.interr:
                    self.say('One or more interrupt handlers already defined. New one is appended to the previous.', ERROR)
                    self.body = []
                else:
                    if len(self.pages) > 1:
                        self.body = ["""
        movwf   var_w_temp
        swapf   STATUS, W
        movwf   var_status_temp
        movf    PCLATH, W
        movwf   var_pclath_temp
        movf    var_test, W
        movwf   var_test_temp
        bcf     PCLATH, 3
        bcf     PCLATH, 4
        """]
                        self.instr = 9
                    else:
                        self.body = ["""
        movwf   var_w_temp
        swapf   STATUS, W
        movwf   var_status_temp
        movf    var_test, W
        movwf   var_test_temp
        """]
                        self.instr = 5
                self.body += ['\n;\n; * Interrupts handler *\n;\n']
            else:
                self.body=['\n;\n; * Function %s *\n;\n' % func_name]
                self.app('func_%s\n' % func_name, verbatim=True)
                self.instr=0
            self._convert(node.code)
            
            if not isinstance(node.code.nodes[-1], Return) and func_name != 'on_interrupt':

                self.app('return')
                
            self.prelast_bank = None
            if func_name == 'on_interrupt':
                self.app(self.inter_ret, verbatim=True)
                self.app(';\n; * End of interrups handler *\n;', verbatim=True)
                body_joined=''.join(self.body)
                self.interr += body_joined
                self.interr_instr += self.instr
            else:
                self.app(';\n; * End of function %s *\n;' % func_name, verbatim=True)
                body_joined=''.join(self.body)
                self.funcs[func_name]=AsmFunction(node.argnames, body_joined,
                        self.instr, is_used, self.head)
            self.infunc=self.in_inter=False
            self.instr=tinstr
            self.curr_bank=tcurr_bank
            self.last_bank=tlast_bank
            self.prelast_bank=tprelast_bank
            self.body=tbody
        elif isinstance(node, Getattr):
            name=self.get_name(node)
            if name:
                self._convert(Name(name))
#       elif isinstance(node, Global):
        elif isinstance(node, If):
            self.app(verbatim=True)
            exit_lbl=self.getLabel()
            
            for n in node.tests:
                self._convert(n[0])
                self.del_last=False
                label=self.getLabel()
                self.app('btfsc', 'STATUS', 'Z')
                self.app('goto', label)
                self._convert(n[1])
                self.app('goto', exit_lbl)
                self.app('%s' % label, verbatim=True)
            self._convert(node.else_)
            self.app('%s' % exit_lbl, verbatim=True)
        elif isinstance(node, Invert):
            self._convert(node.expr)
            buf=self.push()
            self.app('movwf', buf)
            self.app('comf', buf, 'w')
#       elif isinstance(node, Keyword):
#       elif isinstance(node, Lambda):
        elif isinstance(node, LeftShift):
            if isinstance(node.right, Const) and self.formatConst(node.right.value)!=-1 and (node.right.value < 8 or self.op_speed):
                buf=self.push()
                self._convert(node.left)
                self.app('movwf', buf)
                for i in xrange(node.right.value-1):
                    self.app('rlf', buf, 'f')
                self.app('rlf', buf, 'w')
            else:
                self._convert(Discard(CallFunc(Name('lshift'), [node.left, node.right], None, None)))
                
#       elif isinstance(node, List):
#       elif isinstance(node, ListComp):
#       elif isinstance(node, ListCompFor):
#       elif isinstance(node, ListCompIf):
        elif isinstance(node, Mod):
            self._convert(Discard(CallFunc(Name('mod'), [node.left, node.right], None, None)))
        elif isinstance(node, Module):
            if node.namespace:
                astks='*'*(len(node.namespace)+11)
                self.app('\n\n; %s\n; * Module %s *\n; %s\n' % (astks,
                    node.namespace, astks), verbatim=True)
                self.push_ns(node.namespace)
                self._convert(node.node)
                self.pop_ns()
                astks='*'*(len(node.namespace)+18)
                self.app('\n; %s\n; * End of module %s *\n; %s\n\n' % (astks,
                    node.namespace, astks), verbatim=True)
            else:
                self._convert(node.node)
        elif isinstance(node, Mul):
            self._convert(Discard(CallFunc(Name('mul'), [node.left, node.right], None, None)))
        elif isinstance(node, Name):
            if self.name_with_ns('_'+node.name) in self.uvars:
                self.app('movf', '_'+node.name, 'w')
            elif (node.name in self.hdikt) or \
                 ('.' in node.name and node.name in self.uvars):
                self.app('movf', node.name, 'w')
            else:
                self.say('variable %s not initialized' % node.name, ERROR, self.lineno(node))
        elif isinstance(node, Not):
            lbl1=self.getLabel()
            lbl_end=self.getLabel()
            self._convert(node.expr)
            self.del_last=False
            self.app('btfsc', 'STATUS', 'Z')
            self.app('goto', lbl1)
            self.app('movlw', '0')
            self.app('goto', lbl_end)
            self.app(lbl1, verbatim=True)
            self.app('movlw', '1')
            self.app(lbl_end, verbatim=True)
            self.test()
        elif isinstance(node, Or):
            lbl_end=self.getLabel()
            for n in xrange(len(node.nodes)):
                self._convert(node.nodes[n])
                self.del_last=False
                if n+1 != len(node.nodes):
                    self.app('btfss', 'STATUS', 'Z')
                    self.app('goto', lbl_end)
            self.app(lbl_end, verbatim=True)
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
                if self.in_inter:
                    self.say('Interrupt handler can not return any values! Ignoring...', ERROR, level=self.warning)
                else:
                    self._convert(node.value)
                    self.del_last = False
            
            if self.in_inter:
                self.app('goto', self.inter_ret)
            else:
                self.app('return')
        elif isinstance(node, RightShift):
            if isinstance(node.right, Const) and self.formatConst(node.right.value)!=-1 and (node.right.value < 8 or self.op_speed):
                buf=self.push()
                self._convert(node.left)
                self.app('movwf', buf)
                for i in xrange(node.right.value-1):
                    self.app('rrf', buf, 'w')
                    
                self.app('rrf', buf, 'f')
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
        elif isinstance(node, Subscript):
            if not (isinstance(node.expr, Name) or
                    isinstance(node.expr, Getattr)):
                self.say('Bit assign may be applied to bytes only.', ERROR, self.lineno(node))
            elif len(node.subs) != 1:
                self.say('More than one subscripts are not fully supported while.', ERROR, self.lineno(node))
            elif not node.flags=='OP_APPLY':
                self.say('Unsupported flag: %s.' % node.flags, ERROR, self.lineno(node))
            else:
                name=self.get_name(node.expr, malloc=True)
                if isinstance(node.subs[0], Const):
                    self.app('movlw', '.0')
                    self.app('btfsc', name, str(node.subs[0].value))
                    self.app('movlw', '.1')
                elif isinstance(node.subs[0], Name):
                    if node.subs[0].name in self.hdikt:
                        self.app('movlw', '.0')
                        self.app('btfsc', name, node.subs[0].name)
                        self.app('movlw', '.1')
                    else:
                        self._convert(Bitand([node.expr, LeftShift((Const(1), node.subs[0]))]))
                else:
                    self.say('Only constant indices are supported while.', ERROR, self.lineno(node))
                self.test()
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
            self.app('\n%s' % lbl_beg, verbatim=True)
            self._convert(node.test)
            self.del_last=False
            self.app('btfsc', 'STATUS', 'Z')
            self.app('goto', '%s\n' % lbl_else)
            self._convert(node.body)
            self.app('goto', lbl_beg)
            if node.else_ != None:
                self.app('\n%s' % lbl_else, verbatim=True)
                self._convert(node.else_)
            self.app('\n%s' % lbl_end, verbatim=True)
            del self.lbl_stack[-1]
#       elif isinstance(node, Yield):
        else:
            self.say('"%s" node is not supported while.' % node.__class__.__name__, ERROR, self.lineno(node))
            
    def get_name(self, obj, malloc=False):
        """
        Adds modificators to the object's name and returns it in flat assembler
        form.
        
        @param obj: Object whose assembler name is to be returned.
        @type  obj: C{AsmObject}
        @param malloc: Try to allocate memory for a variable if it did not
          exist before.
        @type  malloc: C{bool}
        @return: Name of the object for assembler code.
        @rtype:  C{str}
        """
        if isinstance(obj, Name) or isinstance(obj, AssName):
            name=obj.name
            if name not in self.hdikt:
                name='_'+name
                if self.namespace:
                    name=self.namespace+'.'+name
        elif isinstance(obj, Getattr) or isinstance(obj, AssAttr):
            expr=obj.expr
            name='_'+obj.attrname
            while isinstance(expr, Getattr):
                name=expr.attrname+'.'+name
                expr=expr.expr
                
            if isinstance(expr, Name):
                name=expr.name+'.'+name
            else:
                raise 'Getattr and AssAttr is supported in current version for module attributes access only!'
        else:
            self.say('Object %s not supported!' % str(obj.__class__), ERROR)
            return
            
        if malloc and (name not in self.hdikt):
            self.malloc(name)

        return name
            
    def formatConst(self, c):
        """
        Formats a constant for assembler code. Supports characters and bytes.
        @param c: Constant to be formatted.
        @return: Formatted constant
        @rtype:  C{str}
        """
        global ERROR
        if type(c) == types.IntType and 0 <= int(c) <= 0xff:
            return hex(c)
        elif type(c) == types.StringType and len(c)==1:
            return "'%s'" % c
        else:
            self.say('%s type constant is not supported while.' % c.__class__.__name__, ERROR)
            return c

    def lineno(self, node):
        """
        @param node: Node to be analyzed.
        @return: Number of line that the given node belongs to or C{None} if
          the node doesn't contain such information.
        """
        if hasattr(node, 'lineno'):
            return node.lineno
        else:
            return None
            
    def push(self):
        """
        Create a new temporary variable.
        
        @return: Name of the new temporary variable.
        
        @todo: Give a more proper name.
        """
        self.tmp_var += 1
        name='temp%g' % self.tmp_var
        self.malloc(name)
        return name
        
    def getLabel(self):
        """
        Create a new label.
        
        @return: Name of the new label.
        """
        self.label += 1
        return 'label%i' % self.label
    
    def malloc(self, name, care=False, addr=None):
        """
        Allocate static memory cell for a variable.
        
        @param name: Name of the variable to be created.
        @param care: True if the function should warn if the variable is
          already defined.
        @param addr: Memory address that should be allocated.
        """
        global ERROR
        name=self.name_with_ns(name)
            
        if name not in self.uvars:
            if addr == None:
                try:
                    addr=self.cvar.reserve_byte()
                except:
                    self.say("program does not fit RAM.", ERROR)
                    self.uvars[name]=None
                    return
            else:
                try:
                    self.cvar.reserve_byte(addr)
                except:
                    self.say("address %i is not allocatable" % addr, WARNING)
                    return
            
            self.uvars[name]=addr
            if len(self.uvars) > self.ram_usage:
                self.ram_usage=len(self.uvars)
                
            self.head += '%s\tequ\t%s\t;bank %g\n' % (name, hex(addr), addr >> 7)
        elif care:
            self.say("name %s is defined twice!" % name, WARNING)

    def name_with_ns(self, name):
        """
        Get name of a variable from the current namespace.
        
        @param name: Name of the variable without namespace modifier.
        @returns: Name of the given variable with namespace modifier.
        """
        if self.namespace and (name not in self.hdikt):
            name='%s.%s' % (self.namespace, name)
        return name

#    def free(self, name, care=1):
#        if name in self.uvars:
#            self.cvar.insert(0, self.uvars[name])
#            del self.uvars[name]
#        elif care:
#            pyastra.say("variable %s can't be deleted before assign!" % name, level=self.warning)

    def bank_by_name(self, name):
        """
        Emit assembler code that switches banks to the given variable bank.

        @param name: Variable name.
        """
        if name in self.uvars:
            addr = self.uvars[name]
        elif name in self.hdikt:
            if name in self.bank_indep:
                return ''
            addr = self.hdikt[name]
        else:
            return ''

        bank = addr >> 7
        addr7 = addr & 0x7f

        if self.maxram < 0x80 or (not 'RP0' in self.hdikt):
            return ''
        
        ret=''
        if self.curr_bank != None:
            for block in self.shareb:
                addr_in_block = 0
                curr_block_has = 0
            
                for sub in block:
                    if sub[0] <= addr <= sub[1]:
                        addr_in_block = 1
                    
                    if sub[0] <= (addr7 | (sub[0] >> 7 << 7)) <= sub[1]:
                        curr_block_has = 1
                
                if addr_in_block and curr_block_has:
                    self.prelast_bank=self.last_bank
                    self.last_bank=self.curr_bank
                    return ''
        else:
            for block in self.shareb:
                addr_in_block = 0
                curr_block_has = 1
            
                for sub in block:
                    if sub[0] <= addr7 <= sub[1]:
                        addr_in_block = 1
                    
                    if  not (sub[0] <= (addr7 | (sub[0] >> 7 << 7)) <= sub[1]):
                        curr_block_has = 0
                
                if addr_in_block:
                    if curr_block_has:
                        self.prelast_bank=self.last_bank
                        self.last_bank=self.curr_bank
                        return ''
                    else:
                        break
            
        if self.curr_bank==None or ((bank & 1) ^ (self.curr_bank & 1)):
            if bank & 1:
                ret += '\tbsf\tSTATUS,\tRP0\n'
            else:
                ret += '\tbcf\tSTATUS,\tRP0\n'
            self.instr += 1
           
        if self.curr_bank==None or (((bank & 2) ^ (self.curr_bank & 2))) and self.maxram > 0xff and 'RP1' in self.hdikt:
            if bank & 2:
                ret += '\tbsf\tSTATUS,\tRP1\n'
            else:
                ret += '\tbcf\tSTATUS,\tRP1\n'
            self.instr += 1
            
        self.prelast_bank=self.last_bank
        self.last_bank=self.curr_bank
        self.curr_bank=bank
        return ret

    def push_ns(self, suffix):
        """
        Pushes current namespace to the stack and sets new namespace
        as current.

        @param suffix: New namespace name.
        """
        if not self.disable_ns:
            self.namespaces_bak += [self.namespace]
            if self.namespace:
                self.namespace += '.'
            self.namespace += suffix

    def pop_ns(self):
        """
        Pops a previous namespace.
        """
        if not self.disable_ns:
            self.namespace = self.namespaces_bak.pop()

    def page_org(self, instr, f_instr):
        """
        Determine a program memory page for a function and generate the
        required code.
        
        @param instr: Current instruction counter value.
        @param f_instr: Functon's instruction count.
        @return: A tuple:
          - [0] is the code to start the function on a new program page.
          - [1] is the state of instruction counter after function.
        """
        global ERROR
        if self.pages[self.cur_page][1] >= instr + f_instr:
            return ('', instr+f_instr)
        else:
            self.cur_page += 1
            if len(self.pages)==self.cur_page:
                if not self.has_errors:
                    self.say('Program doesn\'t fit program memory.', ERROR)
                return
            return ('\torg\t%s\n' % hex(self.pages[self.cur_page][0]), self.pages[self.cur_page][0]+f_instr)
    
    def test(self):
        """
        Emit code for C{W == 0} test.
        """
        self.app('movwf', 'var_test')
        self.app('movf', 'var_test', 'f')
        self.del_last=True

    def app(self, cmd='', op1=None, op2=None, verbatim=False, comment=''):
        """
        Properly append the given assembler code to the result.
        Caresof banks if needed.

        @param cmd: Instruction name or verbatim code to be included.
        @param op1: First operand of instruction.
        @param op2: Second operand of instruction.
        @param verbatim: True if cmd is verbatim assembler code.
        @param comment: Comment to be appended after the instruction.
        """
        if self.del_last:
            del self.body[-2:]
            self.del_last=False
            self.curr_bank=self.prelast_bank
            self.instr = self.prelast_instr
            self.prelast_bank=self.last_bank = None

        self.prelast_instr=self.last_instr
        self.last_instr=self.instr
       #FIXME: more intelligent verbatim code analyzing
        if verbatim:
            for line in cmd.splitlines():
                if line:
                    s=line.split()
                    if s and s[0] != ';':
                        self.last_bank = self.prelast_bank = self.curr_bank = None
                        break
        
        if cmd=='call':
            self.last_bank = self.prelast_bank = self.curr_bank= None
            
        if verbatim:
            self.body += ['%s\n' % (cmd,)]
            return

        bodys=''
        if comment:
            comment='\t;%s' % comment
        if op1 and (cmd not in self.no_bank_cmds):
            op1=self.name_with_ns(op1)
            bodys += self.bank_by_name(op1)

        if len(self.pages) > 1 and op1 and cmd=='call':#(cmd in self.pagesel_cmds):
            #has_dollar=0
            #for ch in op1:
            #    if ch=='$':
            #        has_dollar=1
            #        break
            #if not has_dollar:
                bodys += '\tpagesel %s\n' % op1
                self.instr += 2

        if op2 != None:
            bodys += '\t%s\t%s,\t%s' % (cmd, op1, op2)
        elif op1 != None:
            bodys += '\t%s\t%s' % (cmd, op1)
        else:
            bodys += '\t%s' % (cmd,)
        self.instr += 1
        
        if len(self.pages) > 1 and op1 and cmd=='call':#(cmd in self.pagesel_cmds):
            bodys += '\n\tpagesel $+1'
            self.instr += 2


        self.body += [bodys+comment+'\n']

class AsmFunction:
    """
    Represents a python function.
    """
    def __init__(self, args, body = None, instr = None, is_used = False,
            head = None):
        self.args = args
        self.body = body
        self.instr = instr
        self.is_used = is_used
        self.head = head
        
class AsmObj:
    """
    Represents an assembler instruction.
    
    @todo: Finish.
    """
    def __init__(self, cmd='', op1=None, op2=None, verbatim=False, comment=''):
        """
        @param cmd: Instruction name or verbatim code to be included.
        @param op1: First operand of instruction.
        @param op2: Second operand of instruction.
        @param verbatim: True if cmd is verbatim assembler code.
        @param comment: Comment to be appended after the instruction.
        """
        self.cmd=cmd
        self.op1=op1
        self.op2=op2
        self.verbatim=verbatim
        self.comment=comment

    def __str__(self):
        pass
        
class MemoryManager:
    """
    Manages memory allocation.
        
    @todo: Finish.
    """
    def __init__(self):
        pass

class MemoryMap:
    """
    Represents register memory map.
    
    @ivar mmap: Dictionary that stores memory allocation information. Keys
      are addresses, values contains a C{True} value if the memory cell
      is allocatable.
    """
    def __init__(self, banks):
        """
        @param banks: Register memory start and end addresses.
        """
        self.mmap={}
        for bank in banks:
            for addr in xrange(bank[0], bank[1]+1):
                self.mmap[addr] = True
                
    def reserve_byte(self, addr=None):
        """
        Reserve the given address.

        @param addr: Address of the cell to be reserved.
        """
        if not len(self.mmap):
            raise 'Program does not fit the RAM!'
        
        if addr == None:
            k=self.mmap.keys()
            k.sort()
            addr=k[0]
        elif not self.mmap.has_key(addr):
            raise 'Address %i is reserved or is not allocatable!' % addr
        
        del self.mmap[addr]
        return addr

    def is_reserved(self, addr):
        """
        Check whether the cell is reserved or it's not.
        
        @param addr: Address of a cell.
        @returns: Whether addres is reserved (C{True}) or no (C{False}).
        """
        return not self.mmap.has_key(addr)
    
    def free_byte(self, addr):
        """
        Free the given address.

        @param addr: Address of the cell to be freed.
        """
        self.mmap[addr] = True

