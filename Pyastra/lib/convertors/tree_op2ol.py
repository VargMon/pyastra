############################################################################
# $Id$
#
# Description: pic14 tree to object list convertor. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################
"""
Pic14 tree to object list convertor.
U{Pyastra project <http://pyastra.sourceforge.net>}.


Namespaces feature implementing plan
====================================
  - (DONE) Output not to assembler directly, but into an object list.
  - Move all memory control to C{MemoryManager} class.
  - Add support of C{CallFunc}, C{Function} and C{Return} nodes.
  - Add support of C{Global} node.
  - Add support of C{From} node.
  - Fix C{asm()} pseudofunction.
  - Generate the head after C{_convert()}.
  - Implement algorithm that will generate the optimal static memory
    allocation.
  - Implement dynamic malloc for recursive functions.
  - Search for cases when dynamic malloc would be more effective rather
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
@todo: Fix bank selection. Bank must be set to None:
    - (DONE) Call instruction.
    - (DONE) After the line that's a used label.
    - (DONE) After raw AsmObjects
    - (DONE) In the beginning of the interruption handler
    - (DONE) In the beginning of a function if it has no arguments. To the last
      argument bank otherwise.)
  Also bank shouldn't be set to None after:
    - After call instruction, if the called function allways exit with
      the required bank.
    - After the line that's a used label if the line with goto has
      the required bank.
  Also banks should be set to the bank of the last argument if the function
  has any.
@todo: uvars and cvar -> MemoryManager
@todo: Finish namespaces support
@todo: Fix problems:
    - Pages support is broken
"""

from compiler.ast import *
import types, compiler, sys, os.path, pyastra.ports.pic14, pyastra.ports.pic14.procs, pyastra
from pyastra import Option, MESSAGE, WARNING, ERROR

converts_from='tree_op'
converts_to='ol'
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
        Option('Include source code in asm file (disabled by default)', lkey='src'),
        Option('Disable namespaces support (pyastra 0.0.4 compatibility mode)', lkey='disable_ns')
        )

class Convertor:
    """
    Main convertor class
    @see: L{convertors}
    
    @cvar tmp_var: Latest temporary variable number.
    @cvar uvars: User defined variables dictioinary.
    @cvar bank_cmds: Bank-sensitive commands.
    @cvar cond_br_cmds: Conditional branching commands.
    @cvar pagesel_cmds: Page-sensitive commands.
    @cvar no_bank_cmds: Bank-insensitive commands.
    @cvar lbl_stack: Stack of lables.
    @cvar funcs: Dictionary of tuples that represent functions. 
    @cvar verbatim: True if the source code includes verbatim assembler lines.
    @cvar ram_usage: Number of registers used by the compiled program.
    @cvar infunc: True if the convert function on the top is inside the
      function.
    @cvar interr: List of lines in the interrupt handler assembler code.
    @cvar in_inter: True if the convert function on the top is inside the
      interrupt handler.
    @cvar inter_ret: Label to go to to return from the interrupt.
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
    @ivar cvar: Memory map.
    @ivar namespaces_bak: Stack of previous namespaces.
    @ivar directives: Assembler directives that should be parsed by assembler
      parser. Every Directive is represented by a dict with name as the key
      and size in program memory as the value.
    @ivar func_name: Current function name.
    
    @todo: Refactor some of the variables ond objects (ram_usage,
            cvar, Memory map, namespaces_bak, etc).
    @status: Broken.
    """
    ext='asm'
    meta={}

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
    directives = {'__config': 0, 'banksel': 2, 'pagesel': 2, 'org': 0}
    lbl_stack=[]
    funcs={}
    verbatim=False
    ram_usage=1
    infunc=False
    interr = []
    in_inter = False
    inter_ret=''

    def __init__(self, src, opts):
        global WARNING, ERROR
        self.data = []
        self.src_line = None
        self.namespace=''
        self.has_errors=False
        self.modified=False
        self.caller_say=opts['pyastra'].say
        self.opts=opts
        self.func_name = None
        self.src = None
        self.line_from = 1
        self.line_to = 0
        if opts.get('port', 'pic14') != 'pic14':
            return
        procs=pyastra.ports.pic14.procs.__all__
        fprocs=filter(lambda item: item[-1]!='i', procs)
        if opts.setdefault('proc', 'pic16f877') not in fprocs:
            self.modified=False
            return
        
        self.disable_ns=opts['disable_ns']
        self.src_en = opts['src']
        
        PROC=opts['proc']
        if opts['icd']:
            if PROC + 'i' not in procs:
                self.say('Seems like microcontroller %s doesn\'t support ICD.' % opts['proc'], ERROR)
                return
            else:
                PROC+='i'
            
        self.PROC = PROC
        self.ICD=opts['icd']
        self.op_speed=False
        self.procmod = __import__('pyastra.ports.pic14.procs.%s' %PROC, globals(), locals(), '*')
        self.vectors = self.procmod.vectors
        AsmObject.hdikt  = self.hdikt  = Variable.hdikt = self.procmod.hdikt
        AsmObject.pages  = self.pages  = self.procmod.pages
        AsmObject.shareb = self.shareb = self.procmod.shareb
        AsmObject.maxram = self.maxram = self.procmod.maxram
        AsmObject.uvars  = self.uvars
        Variable.mmap = MemoryMap(self.procmod.banks)
        
        for var_name in self.hdikt:
            var = Variable(var_name, addr = self.hdikt[var_name],
                    special = True)
            self.uvars[var_name] = var
        
        gp_ram_max = 0
        for i in self.procmod.banks:
            gp_ram_max += i[1] - i[0] + 1
        
        self.max_instr = 0
        for i in self.pages:
            self.max_instr += i[1] - i[0] + 1
            
        self.convert(src)
        
        self.meta={
            'max_instr': self.max_instr,
            'gp_ram_max': gp_ram_max,
            }
        if not self.has_errors:
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
        @todo: Correct code for the case when convert() returns more than one
          root. Fix the same code in file2tree.
        """
        global WARNING, ERROR
        
        self.cvar=MemoryMap(self.procmod.banks)
            
        # Import builtins
        name=os.path.join(pyastra.ports.pic14.__path__[0], 'builtins.py')
        c = pyastra.Pyastra(name, self.opts['caller_select'], self.say,
                trg_t = ['tree_op'], opts = self.opts.copy(), src_t = 'file')
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
            self.get_var('var_w_temp', addr=addrs[0],
                    system = True).used = True
            self.get_var('var_status_temp', addr=addrs[1],
                    system = True).used = True
            self.get_var('var_pclath_temp', addr=addrs[2],
                    system = True).used = True
            self.get_var('var_test_temp', addr=addrs[3],
                    system = True).used = True
            self.get_var('var_test', addr=addrs[4],
                    system = True).used = True
        else:
            self.get_var('var_test', system = True).used = True

        self._convert(node)
        
        body_buf = [AsmObject("""
\terrorlevel\t-302
\terrorlevel\t-306
""", verbatim = True)]

        if self.vectors:
            body_buf += [AsmObject('org', hex(self.vectors[0]))]
        else:
            body_buf += [AsmObject('org', '0x0')]
        
        if self.ICD:
            body_buf += [AsmObject('nop')]

        if self.pages[0][0]>0:
            body_buf += [AsmObject('goto', 'main')]
            if self.interr:
                if len(self.pages) > 1:
                    ao = AsmObject("""
        movf    var_test_temp,      W
        movwf   var_test
        movf    var_pclath_temp,    W
        movwf   PCLATH
        swapf   var_status_temp,    W
        movwf   STATUS
        swapf   var_w_temp, F
        swapf   var_w_temp, W
        retfie\n""", verbatim = True)
                    ao.pmem = 9
                else:
                    ao = AsmObject("""
        movf    var_test_temp,      W
        movwf   var_test
        swapf   var_status_temp,    W
        movwf   STATUS
        swapf   var_w_temp, F
        swapf   var_w_temp, W
        retfie\n""", verbatim = True)
                    ao.pmem = 7
                self.interr += [ao]
                
                body_buf += ([AsmObject("org", hex(self.vectors[1]))]
                        + self.interr)
            else:
                body_buf += [AsmObject("org", hex(self.pages[0][0]))]
            body_buf += [AsmObject("\nmain\n", verbatim = True)]
            
        self.data = body_buf + self.data

        if self.ICD:
            self.ram_usage += 1

        self.data += [AsmObject('goto', '$')]
            
        fbuf = []
        
        used = used_last = []
        unknown = []
        
        for f in self.funcs.itervalues():
            if None in f.callers or 'on_interrupt' in f.callers:
                used += [f]
            else:
                unknown += [f]
        
        if used and not(len(used) == 1 and used == 'on_interrupt'):
            self.data += [AsmObject("\n;\n; SUBROUTINES\n;\n\n",
                    verbatim = True)]
            
        while unknown and used_last:
            ul_new = []
            uk_new = []
            for f in unknown:
                for uf in f.callers:
                    if uf in used_last:
                        ul_new += [f]
                        break
                if not ul_new or f != ul_new[-1]:
                    uk_new += [f]
            used_last = ul_new
            used += used_last
            unknown = uk_new
            
        for f in used:
            fbuf += f.body
            
        self.data += fbuf + [AsmObject("\n\tend\n", verbatim = True)]
        
    def _convert(self, node):
        """
        Recursive convert function.
        
        @param node: Node to be converted.
        @type  node: C{Node}
        @todo: Add new AST Nodes from Python 2.4 as comments.
        """
        # TODO: fix all nodes that require name_with_ns instead of
        #       some variables (usually "name")
        if (not isinstance(node, list)
                and node != None
                and self.src
                and node.lineno):
            self.line_to = node.lineno
            
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
            end_lbl=Label('and_end')
            for n in xrange(len(node.nodes)):
                self._convert(node.nodes[n])
                if n+1 != len(node.nodes):
                    self.data[-1].fix_test_enabled = True
                    self.app('btfsc', 'STATUS', 'Z')
                    self.app('goto', end_lbl)
            self.data[-1].fix_test_enabled = True
            self.app(end_lbl)
        elif isinstance(node, AssAttr):
            if node.flags == 'OP_ASSIGN':
                self.app('movwf', self.get_var(node))
            else:
                self.say('%s flag is not supported while.' % node.flags, ERROR,
                        self.lineno(node))
#       elif isinstance(node, AssList):
        elif isinstance(node, AssName):
            if node.flags=='OP_ASSIGN':
                self.app('movwf', self.get_var(node))
            else:
                self.say('%s flag is not supported while.' % node.flags,
                        ERROR, self.lineno(node))
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
                    
            if (all_names
                    and isinstance(node.expr, Const)
                    and node.expr.value == 0):
                for n in node.nodes:
                    self.app('clrf', self.get_var(n))
            elif any_sscr:
                if not all_sscr:
                    self.say('mixing bit and byte assign is not supported.',
                            ERROR, self.lineno(node))
                elif isinstance(node.expr, Const):
                    if node.expr.value:
                        oper='bsf'
                    else:
                        oper='bcf'
                        
                    for n in node.nodes:
                        try:
                            var = self.get_var(n.expr)
                        except:
                            self.say('Bit assign may be applied to plain variables only.', ERROR, self.lineno(node))
                            break

                        for i in n.subs:
                            if isinstance(i, Const):
                                self.app(oper, var, str(i.value))
                            elif isinstance(i, Name) and i.name in self.hdikt:
                                # FIXME: Check that i.name references to a bit
                                self.app(oper, var, str(i.name))
                            elif oper=='bsf':
                                self._convert(AugAssign(n.expr, '|=', LeftShift((Const(1), i))))
                            else:
                                self._convert(AugAssign(n.expr, '&=', Invert(LeftShift((Const(1), i)))))

                elif isinstance(node.expr, Subscript) and len(node.expr.subs) == 1 and isinstance(node.expr.subs[0], Const):
                    # FIXME: expressions with a dot (like module.var) may not
                    #        work here!
                    lbl_else = Label('sub_else')
                    lbl_exit = Label('sub_exit')

                    evar = self.get_var(node.expr.expr)
                    self.app('btfsc', evar, str(node.expr.subs[0].value))
                    self.app('goto', lbl_else)
                    for n in node.nodes:
                        if not (isinstance(n.expr, Name) or
                                isinstance(n.expr, Getattr)):
                            self.say('Bit assign may be applied to plain numbers only.', ERROR, self.lineno(node))
                        else:
                            var = self.get_var(n.expr)
                            for i in n.subs:
                                if isinstance(i, Const):
                                    self.app('bcf', var, str(i.value))
                                elif isinstance(i, Name) and i.name in self.hdikt:
                                    self.app('bcf', var, str(i.name))
                                else:
                                    self.say('Only constant indices are supported while in some cases.', ERROR, self.lineno(node))
                                    return
                    self.app('goto', lbl_exit)
                    self.app(lbl_else)
                    for n in node.nodes:
                        if not isinstance(n.expr, Name):
                            self.say('Bit assign may be applied to bytes only.', ERROR, self.lineno(node))
                        else:
                            var=self.get_var(n.expr)
                            for i in n.subs:
                                if isinstance(i, Const):
                                    self.app('bsf', var, str(i.value))
                                elif isinstance(i, Name) and i.name in self.hdikt:
                                    self.app('bsf', var, str(i.name))
                                else:
                                    self.say('Only constant indices are supported while.', ERROR, self.lineno(node))
                    self.app(lbl_exit)
                else:
                    self._convert(If([(node.expr,
                        Stmt([Assign(node.nodes, Const(1))]))],
                        Stmt([Assign(node.nodes, Const(0))])))
            else:
                self._convert(node.expr)
                
                for n in node.nodes:
                    self._convert(n)
        elif isinstance(node, AugAssign):
                var=self.get_var(node.node, check = True)
                    
                if node.op == '+=':
                    self._convert(node.expr)
                    self.app('addwf', var, 'f')
                elif node.op == '-=':
                    self._convert(node.expr)
                    self.app('subwf', var, 'f')
                elif node.op == '*=':
                    self._convert(Mul((node.node, node.expr)))
                    self.app('movwf', var, 'f')
                elif node.op == '/=':
                    self._convert(Div((node.node, node.expr)))
                    self.app('movwf', var, 'f')
                elif node.op == '%=':
                    self._convert(Mod((node.node, node.expr)))
                    self.app('movwf', var, 'f')
                elif node.op == '**=':
                    self._convert(Power((node.node, node.expr)))
                    self.app('movwf', var, 'f')
                elif node.op == '>>=':
                    self._convert(RightShift((node.node, node.expr)))
                    self.app('movwf', var, 'f')
                elif node.op == '<<=':
                    self._convert(LeftShift((node.node, node.expr)))
                    self.app('movwf', var, 'f')
                elif node.op == '&=':
                    self._convert(node.expr)
                    self.app('andwf', var, 'f')
                elif node.op == '^=':
                    self._convert(node.expr)
                    self.app('xorwf', var, 'f')
                elif node.op == '|=':
                    self._convert(node.expr)
                    self.app('iorwf', var, 'f')
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
                        for s in node.args[0].value.splitlines(True):
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
                            elif op[0].lower() in self.directives:
                                self.app(op[0], ' '.join(op[1:]),
                                        comment = comment,
                                        pmem = self.directives[op[0].lower()])
                            elif (len(op) > 3
                                    or ((op[0].lower() not in self.bank_cmds)
                                        and (op[0].lower()
                                            not in self.no_bank_cmds))):
                                if s[0].isspace():
                                    self.say('Can\'t parse line in asm function:\n%sIncluding the line unparsed.' % s, WARNING)
                                    raw = True
                                    prev_op = ''
                                    force_bank = False
                                else:
                                    raw = False
                                    force_bank = None

                                self.app(s, raw=raw, verbatim = True,
                                        force_bank = force_bank)
                            else:
                                op[0]=op[0].lower()
                                    
                                if (len(op) > 1 and (op[0] in self.bank_cmds
                                    or op[0] in self.no_bank_cmds)
                                    and op[0][-1] in 'fzcs'):
                                    
                                    op[1] = self.get_var(op[1], system = True)

                                fix_cond_br = prev_op in self.cond_br_cmds
                                comment=comment[1:]
                                if len(op)==1:
                                    self.app(op[0], comment=comment,
                                            fix_cond_br = fix_cond_br)

                                elif len(op)==2:
                                    self.app(op[0], op[1], comment=comment,
                                            fix_cond_br = fix_cond_br)
                                else:
                                    self.app(op[0], op[1], op[2],
                                            comment=comment,
                                            fix_cond_br = fix_cond_br)
                                    
                                if op:
                                    prev_op=op[0]
                        self.app('\n; -- End of parsed verbatim inclusion\n', verbatim=True)
                    elif not (2 <= len(node.args) <= 3 and isinstance(node.args[0], Const) and isinstance(node.args[1], Const)):
                        self.say(err_mesg, ERRROR)
                        return
                    else:
                        # In raw version, namespace isn't taken
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
                                    self.get_var(i.value)
                        
                        self.app('\n; -- Verbatim inclusion:\n%s\n; -- End of verbatim inclusion\n' % node.args[0].value, raw = True, pmem = node.args[1].value)
                        self.app('\n\terrorlevel\t-302\n', verbatim=True)
                    return
                elif node.node.name == 'fbin':
                    if (len(node.args) != 1
                            or not isinstance(node.args[0], Const)
                            or not isinstance(node.args[0].value, str)):
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
            elif isinstance(node.node, Getattr):
                func_name = self.name_with_ns(node.node, func = True)
            else:
                self.say('only functions are callable while', ERROR)
                return
            
            if func_name not in self.funcs:
                self.say('function %s is not defined before call (this is not supported while)' % func_name, ERROR, self.lineno(node))
                return
            else:
                self.funcs[func_name].add_caller(self.curr_func)
                
            if  len(self.funcs[func_name].args) != len(node.args):
                self.say('function %s requires exactly %g argument(s)' % (func_name, ERROR, len(self.funcs[func_name].args)))
                return
                         
            for i in xrange(len(node.args)):
                (arg, val)=(self.funcs[func_name].args[i], node.args[i])
                self._convert(val)
                self.app('movwf', arg)
            self.app('call', 'func_%s' % func_name)
                    
##      elif isinstance(node, Class):
        elif isinstance(node, Compare):
            if len(node.ops) != 1:
                self.say('Currently multiple comparisons are not supported', ERROR, self.lineno(node))
            buf = self.push()
            nodes=node.ops
            if nodes[0][0]=='<':
                lbl_false=Label('compare_false')
                self._convert(node.expr)
                self.app('movwf', buf)
                self._convert(nodes[0][1])
                self.app('subwf', buf, 'w') # node.expr - nodes[0][1] should be < 0 (Z=0 and C=0)
                self.app('btfsc', 'STATUS', 'Z')
                self.app('goto', lbl_false) # node.expr = nodes[0][1]
                self.app('bcf', 'STATUS', 'Z') # true
                self.app('btfsc', 'STATUS', 'C')
                self.app(lbl_false)
                self.app('bsf', 'STATUS', 'Z') # false
            elif nodes[0][0]=='>':
                lbl_false=Label('compare_false')
                self._convert(node.expr)
                self.app('movwf', buf)
                self._convert(nodes[0][1])
                self.app('subwf', buf, 'w') # node.expr - nodes[0][1] should be > 0 (Z=0 and C=1)
                self.app('btfsc', 'STATUS', 'Z')
                self.app('goto', lbl_false) # node.expr = nodes[0][1]
                self.app('bcf', 'STATUS', 'Z') # true
                self.app('btfss', 'STATUS', 'C')
                self.app(lbl_false)
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
                lbl_true=Label('compare_true')
                self._convert(node.expr)
                self.app('movwf', buf)
                self._convert(nodes[0][1])
                self.app('subwf', buf, 'w') # node.expr - nodes[0][1] should be <= 0 (Z=1 or C=0)
                self.app('btfsc', 'STATUS', 'Z')
                self.app('goto', lbl_true) # node.expr = nodes[0][1]
                self.app('bsf', 'STATUS', 'Z') # false
                self.app('btfss', 'STATUS', 'C')
                self.app(lbl_true)
                self.app('bcf', 'STATUS', 'Z') # true
            elif nodes[0][0]=='>=':
                lbl_true=Label('compare_true')
                self._convert(node.expr)
                self.app('movwf', buf)
                self._convert(nodes[0][1])
                self.app('subwf', buf, 'w') # node.expr - nodes[0][1] should be >= 0 (Z=1 or C=1)
                self.app('btfsc', 'STATUS', 'Z')
                self.app('goto', lbl_true) # node.expr = nodes[0][1]
                self.app('bsf', 'STATUS', 'Z') # false
                self.app('btfsc', 'STATUS', 'C')
                self.app(lbl_true)
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
                self.say('comparison %s is not supported while.' % node.op, ERROR, self.lineno(node))
                    
        elif isinstance(node, Const):
            self.app('movlw', self.formatConst(node.value), fix_test = True)
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
                    node.list.node.name in ('xrange' or 'range') and
                    len(node.list.args)==2 and
                    node.list.star_args==None and
                    node.list.dstar_args==None):
                self.say('only "for <var> in xrange(<from>, <to>)" or "for <var> in range(<from>, <to>)" for statement is supported while', ERROR, self.lineno(node))
                return
            cntr = self.get_var(node.assign.name)
            self._convert(Assign([node.assign], node.list.args[0]))
            
            lbl_beg=Label('for_begin')
            lbl_else=Label('for_else')
            lbl_cont=Label('for_continue')
            if node.else_ != None:
                lbl_end=Label('for_end')
            else:
                lbl_end=lbl_else

            self.lbl_stack.append((lbl_cont, lbl_end))
                
            if (isinstance(node.list.args[1], Const)
                    and node.list.args[1].value==256):
                #skip whole loop if cntr==255
                self.app('movf', cntr, 'w')
                self.app('sublw', '0xff')
                self.app('btfsc', 'STATUS', 'Z')
                self.app('goto', lbl_else)
                
                self.app(lbl_beg)
                
                self._convert(node.body)
                
                self.app(lbl_cont)
                
                self.app('incf', cntr, 'f')

                self.app('movf', cntr, 'f')
                self.app('btfss', 'STATUS', 'Z')
                self.app('goto', lbl_beg)
            else:
                limit = self.push()
                self._convert(node.list.args[1])
                self.app('movwf', limit)
                
                self.app(lbl_beg)
                
                self.app('movf', limit, 'w')
                self.app('subwf', cntr, 'w')
                self.app('btfsc', 'STATUS', 'Z') #skip if cntr - limit != 0
                self.app('goto', lbl_else)
                self.app('btfsc', 'STATUS', 'C') #skip if cntr - limit  < 0
                self.app('goto', lbl_else)
                
                self._convert(node.body)
                
                self.app(lbl_cont)
                
                self.app('incf', cntr, 'f')
                self.app('goto', lbl_beg)
            
            if node.else_ != None:
                self.app(lbl_else)
                self._convert(node.else_)
            
            self.app(lbl_end)
            del self.lbl_stack[-1]
        elif isinstance(node, Function):
            if self.namespace and node.name != 'on_interrupt':
                func_name='_%s.%s' % (self.namespace, node.name)
            else:
                func_name=node.name
                
            if (func_name in self.funcs):
                self.say('function %s is already defined.' % func_name, ERROR)
                return
                    
            if node.flags:
                self.say('function flags are not supported while.', ERROR)
                
            if node.defaults:
                self.say('function defaults are not supported while.', ERROR)
                
            args = []
            for a in node.argnames:
                args += [self.get_var(a)]
                
            tdata=self.data
            
            self.infunc = True
            if func_name == 'on_interrupt':
                self.in_inter=True
                self.curr_func = 'on_interrupt'
                if not self.vectors:
                    self.say('Selected processor does not support interrupts!', ERROR)
                    return
                if not self.uvars.has_key('var_w_temp'):
                    self.say('Pyastra doesn\'t suppoort interrupts for selected processor while.', ERROR)
                    return
                self.inter_ret=Label('interr_return')
                self.data = []
                if self.interr:
                    self.say('One or more interrupt handlers already defined. New one is appended to the previous.', MESSAGE)
                else:
                    if len(self.pages) > 1:
                        oa = AsmObject("""
        movwf   var_w_temp
        swapf   STATUS, W
        movwf   var_status_temp
        movf    PCLATH, W
        movwf   var_pclath_temp
        movf    var_test, W
        movwf   var_test_temp
        bcf     PCLATH, 3
        bcf     PCLATH, 4
        """, verbatim = True)
                        oa.pmem = 9
                    else:
                        oa = AsmObject("""
        movwf   var_w_temp
        swapf   STATUS, W
        movwf   var_status_temp
        movf    var_test, W
        movwf   var_test_temp
        """, verbatim = True)
                        oa.pmem = 5
                    oa.force_bank = None
                    self.data += [oa]
                self.app('\n;\n; * Interrupts handler *\n;\n', verbatim = True)
            else:
                self.data = []
                self.curr_func = AsmFunction()
                self.app('\n;\n; * Function %s *\n;\n' % func_name, verbatim = True)
                self.app('func_%s\n' % func_name, verbatim = True,
                        org_enabled = True)
                
            self._convert(node.code)
            
            if (not isinstance(node.code.nodes[-1], Return)
                    and func_name != 'on_interrupt'):
                self.app('return')
                
            if func_name == 'on_interrupt':
                self.app(self.inter_ret, verbatim=True)
                self.app(';\n; * End of interrups handler *\n;', verbatim=True)
                self.interr += self.data
            else:
                self.app(';\n; * End of function %s *\n;' % func_name,
                        verbatim=True)
                self.curr_func.args = args
                self.curr_func.body = self.data
                self.funcs[func_name] = self.curr_func
            self.curr_func = None
            self.infunc=self.in_inter=False
            self.data=tdata
        elif isinstance(node, Getattr):
            name=self.get_var(node)
            if name:
                self._convert(Name(name))
#       elif isinstance(node, Global):
        elif isinstance(node, If):
            self.app(verbatim=True)
            exit_lbl=Label('if_end')
            
            for n in node.tests:
                self._convert(n[0])
                self.data[-1].fix_test_enabled = True
                label=Label('if_next_test')
                self.app('btfsc', 'STATUS', 'Z')
                self.app('goto', label)
                self._convert(n[1])
                self.app('goto', exit_lbl)
                self.app(label)
            self._convert(node.else_)
            self.app(exit_lbl)
        elif isinstance(node, Invert):
            self._convert(node.expr)
            buf=self.push()
            self.app('movwf', buf)
            self.app('comf', buf, 'w')
#       elif isinstance(node, Keyword):
#       elif isinstance(node, Lambda):
        elif isinstance(node, LeftShift):
            if (isinstance(node.right, Const)
                    and self.formatConst(node.right.value)!=-1
                    and (node.right.value < 8 or self.op_speed)):
                buf=self.push()
                self._convert(node.left)
                self.app('movwf', buf)
                for i in xrange(node.right.value-1):
                    self.app('rlf', buf, 'f')
                self.app('rlf', buf, 'w')
            else:
                self._convert(Discard(CallFunc(Name('lshift'), [node.left,
                    node.right], None, None)))
                
#       elif isinstance(node, List):
#       elif isinstance(node, ListComp):
#       elif isinstance(node, ListCompFor):
#       elif isinstance(node, ListCompIf):
        elif isinstance(node, Mod):
            self._convert(Discard(CallFunc(Name('mod'), [node.left, node.right], None, None)))
        elif isinstance(node, Module):
            tmp_src   = self.src
            line_from = self.line_from
            line_to   = self.line_to
            
            if hasattr(node, 'src'):
                self.src = node.src.splitlines()
                self.line_from = 1
                self.line_to = 0
            else:
                self.src = None
                
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
                
            self.src       = tmp_src
            self.line_from = line_from
            self.line_to   = line_to
        elif isinstance(node, Mul):
            self._convert(Discard(CallFunc(Name('mul'), [node.left, node.right], None, None)))
        elif isinstance(node, Name):
            self.app('movf', self.get_var(node), 'w')
        elif isinstance(node, Not):
            lbl1=Label('not_set_true')
            lbl_end=Label('not_end')
            self._convert(node.expr)
            self.data[-1].fix_test_enabled = True
            self.app('btfsc', 'STATUS', 'Z')
            self.app('goto', lbl1)
            self.app('movlw', '0')
            self.app('goto', lbl_end)
            self.app(lbl1)
            self.app('movlw', '1')
            self.app(lbl_end, fix_test=True)
        elif isinstance(node, Or):
            lbl_end=Label('or_end')
            for n in xrange(len(node.nodes)):
                self._convert(node.nodes[n])
                self.data[-1].fix_test_enabled = True
                if n+1 != len(node.nodes):
                    self.app('btfss', 'STATUS', 'Z')
                    self.app('goto', lbl_end)
            self.app(lbl_end)
        elif isinstance(node, Pass):
            pass
        elif isinstance(node, Power):
            self._convert(Discard(CallFunc(Name('mul'), [node.left, node.right], None, None)))
#       elif isinstance(node, Print):
#       elif isinstance(node, Printnl):
#       elif isinstance(node, Raise):
        elif isinstance(node, Return):
            if not (isinstance(node.value, Const) and node.value.value==None):
                if self.in_inter:
                    self.say('Interrupt handler can not return any values! Ignoring...', WARNING)
                else:
                    self._convert(node.value)
                    self.data[-1].fix_test_enabled = True
            
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
                name=self.get_var(node.expr)
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
                self.data[-1].fix_test = True
#       elif isinstance(node, TryExcept):
#       elif isinstance(node, TryFinally):
#       elif isinstance(node, Tuple):
        elif isinstance(node, UnaryAdd):
            self._convert(node.expr)
#       elif isinstance(node, UnarySub):
        elif isinstance(node, While):
            lbl_beg=Label('while_begin')
            lbl_end=Label('while_end')
            if node.else_ != None:
                lbl_else=Label('while_else')
            else:
                lbl_else = lbl_end
            self.lbl_stack.append((lbl_beg, lbl_end))
            self.app(lbl_beg)
            self._convert(node.test)
            self.data[-1].fix_test_enabled = True
            self.app('btfsc', 'STATUS', 'Z')
            self.app('goto', lbl_else)
            self._convert(node.body)
            self.app('goto', lbl_beg)
            if node.else_ != None:
                self.app(lbl_else)
                self._convert(node.else_)
            self.app(lbl_end)
            del self.lbl_stack[-1]
#       elif isinstance(node, Yield):
        else:
            self.say('"%s" node is not supported while.' % node.__class__.__name__, ERROR, self.lineno(node))
            
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
        self.uvars[name] = Variable(name)
        return self.uvars[name]
    
    def get_var(self, obj, check = False, addr = None, system = False):
        """
        Returns variable by its name or an AST object.
        
        @param obj: Name of the variable to be created or an AST object
          that contains one.
        @param check: True if the variable should be already initialized.
        @param addr: Memory address that should be allocated.
        @param system: True if the variable is system and the name shouldn't
          be changed.
        """
        global WARNING, ERROR
        
        if system:
            name = self.name_with_ns(obj, func = True)
        else:
            name = self.name_with_ns(obj)
        
        if name not in self.uvars:
            if check:
                self.say("Variable %s must be initialized before use!" % name,
                        ERROR)
                return
            self.uvars[name] = Variable(name, addr = addr)
        
        return self.uvars[name]

    def name_with_ns(self, obj, func = False):
        """
        Get name of a variable from the current namespace.
        
        @param obj: Name of the variable to be created or an AST object
          that contains one.
        @param func: True if returned name is the name of a function.
        @returns: Name of the given variable with namespace modifier.
        @todo: Replace func argument with storing ns in AsmFunction.
        """
        global WARNING, ERROR
        
        if isinstance(obj, Name) or isinstance(obj, AssName):
            name = obj.name
            if name not in self.hdikt:
                if self.namespace:
                    name = self.namespace + '.' + name
                if not func:
                    name = '_' + name
        elif isinstance(obj, Getattr) or isinstance(obj, AssAttr):
            expr = obj.expr
            name = obj.attrname
            while isinstance(expr, Getattr):
                name=expr.attrname+'.'+name
                expr=expr.expr
                
            if isinstance(expr, Name):
                self.say('Getattr and AssAttr is supported in current version for module attributes access only!', ERROR)
                return
            
            name = expr.name + '.' + name
            if not func:
                name = '_' + name
        elif isinstance(obj, str):
            name = obj
            if name not in self.hdikt:
                if self.namespace:
                    name = self.namespace + '.' + name
                if not func:
                    name = '_' + name
        else:
            self.say('Object %s not supported!' % str(obj.__class__), ERROR)
            return
        return name

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
    
    def app(self, cmd = '', op1 = None, op2 = None, verbatim = False,
            comment = '', fix_test = False, raw = False, pmem = None,
            fix_cond_br = False, org_enabled = False, force_bank = False):
        """
        Creates an L{AsmObject} and appends it to L{self.data}.

        @param cmd: Instruction name or verbatim code to be included.
        @param op1: First operand of instruction.
        @param op2: Second operand of instruction.
        @param verbatim: True if cmd is verbatim assembler code.
        @param comment: Comment to be appended after the instruction.
        @param fix_test: True if C{W == 0} code should be emitted after
          instruction.
        @param raw: True if cmd is raw assembler code.
        @param pmem: Program memory required by the object. If not set, the
          value will be counted automatically.
        """
        if self.src_en and self.src and self.line_to >= self.line_from:
            srclist = ''
            for line in xrange(self.line_from - 1,
                    min(self.line_to, len(self.src))):
                srclist += ';%04i: %s\n' % (line + 1, self.src[line])

            if srclist:
                ao = AsmObject(srclist, verbatim = True)
                self.data += [ao]
                
            self.line_from = self.line_to + 1
            
        if cmd.__class__ == Label:
            ao = cmd
            ao.fix_test = fix_test
        else:
            ao = AsmObject(cmd, op1, op2, verbatim, comment, fix_test, raw,
                    fix_cond_br, org_enabled)
            ao.namespace = self.namespace
            ao.force_bank = force_bank
            if pmem != None:
                ao.pmem = pmem
        self.data += [ao]

class AsmFunction:
    """
    Represents a python function.
    
    @ivar args: Arguments of the function.
    @ivar body: Body of the functions.
    @type body: C{list} of C{AsmObject}s
    @ivar callsers: Functions that use this function
    """
    def __init__(self):
        self.args = []
        self.body = None
        self.callers = []
        
    def add_caller(self, caller):
        if caller not in self.callers:
            self.callers += [caller]
        
class AsmObject:
    """
    Represents an assembler instruction and its retinue.

    Life cycle of the object:
      - Initialization: C{o = AsmObj()}.
      - Definition of variables required for next steps (e.g. banks before
        instruction execution).
      - Fields preparation: C{o.prepare()}.
      - Code generation: C{o.finalize()}.
    
    @cvar no_bank_cmds: Bank-insensitive commands.
    @cvar bank_indep: Common bank-independent registers.
    @cvar hdikt: Dictionary of processor-specific register names.
    @cvar pages: Tuple of processor-specific program memory pages.
    @cvar shareb: Tuple processor-specific shared banks.
    @cvar maxram: Amount of memory available for the current processor.
    @cvar uvars: User defined variables dictioinary.
    @cvar label_cmds: Instructions that may have L{Label} as its L{cmd}.
    
    @ivar cmd: Instruction name or verbatim code to be included.
    @ivar op1: First operand of instruction.
    @ivar op2: Second operand of instruction.
    @ivar verbatim: True if cmd should be included verbatim.
    @ivar comment: Comment to be appended after the instruction.
    @ivar fix_test: True if C{W == 0} code should be emitted after instruction
      (should be confirmed by L{fix_test_enabled}).
    @ivar bank_before: Bank before the instruction execution.
    @ivar bank_after: Bank after the instruction execution.
    @ivar body: Assembler code's body generated by the object.
    @ivar pmem: Real program memory required by the object.
    @ivar fix_test_enabled: Enable C{W == 0} code emittion. Works only
      in conjunction with L{fix_test}.
    @ivar raw: True if cmd is raw assembler code.
    @ivar force_bank: A forced value of a bank to be after the instruction
      execution.
      
    @todo: New pages mechanism.
    """
    no_bank_cmds = ('addlw', 'andlw', 'call', 'clrw', 'clrwdt', 'goto',
                    'iorlw', 'movlw', 'nop', 'retfie', 'retlw', 'return',
                    'sleep', 'sublw', 'xorlw')
    bank_indep = ('status', 'fsr', 'pclath', 'intcon', 'pcl')
    label_cmds = ('call', 'goto')
    directives = {'__config': 0, 'banksel': 2, 'pagesel': 2, 'org': 0}
    
    def __init__(self, cmd = '', op1 = None, op2 = None, verbatim = False,
            comment = '', fix_test = False, raw = False, fix_cond_br = False,
            org_enabled = False):
        """
        @param cmd: Instruction name or verbatim code to be included.
        @param op1: First operand of instruction.
        @param op2: Second operand of instruction.
        @param verbatim: True if cmd should be included verbatim.
        @param comment: Comment to be appended after the instruction.
        @param fix_test: True if C{W == 0} code should be emitted after
          instruction.
        @param raw: True if cmd is raw assembler code.
        """
        self.cmd = cmd
        self.op1 = op1
        self.op2 = op2
        self.verbatim = verbatim or raw
        self.comment = comment
        self.fix_test = fix_test
        self.bank_before = None
        self.fix_test_enabled = False
        self.raw = raw
        self.force_bank = False
        self.fix_cond_br = fix_cond_br
        self.org_enabled = org_enabled
        self.pmem = 0

    def prepare(self):
        if (not self.verbatim
                and self.cmd in self.label_cmds
                and self.cmd.__class__ == Label):
            self.cmd.used = True
            
        if isinstance(self.op1, Variable) or isinstance(self.op1, Label):
            self.op1.used = True

    def finalize(self):
        """
        Generated code and update variables. Raises errors if some needed
        variables are not defined.
        
        @todo: More intelligent verbatim code analyzing.
        @todo: Count verbatim code size.
        @todo: Intelligent page select.
        """
        self.body = ''
        if self.org_enabled:
            self.bank_after = None
        else:
            self.bank_after = self.bank_before
        
        if self.force_bank != False:
            self.bank_after = self.force_bank
            
        if self.raw:
            for line in self.cmd.splitlines():
                if line:
                    s = line.split()
                    if s and s[0] != ';':
                        self.bank_after = None
                        break

        if self.op1.__class__ == Label:
            self.op1 = self.op1.get_label()
        elif self.cmd == 'call':
            self.bank_after = None
            
        if self.verbatim:
            self.body += '%s\n' % self.cmd
        else:
            if self.comment:
                self.comment = '\t;%s' % self.comment
                
            if (self.op1 and (self.cmd not in self.no_bank_cmds)
                    and (self.cmd.lower() not in self.directives)):
                if self.op1.__class__ == str:
                    self.op1 = self.uvars[self.op1]
                self.body = self.op1.get_bank(self)
                self.op1 = self.op1.name

            if len(self.pages) > 1 and self.op1 and self.cmd == 'call':
                self.body += '\tpagesel %s\n' % self.op1
                self.pmem += 2

            if self.op2 != None:
                self.body += '\t%s\t%s,\t%s' % (self.cmd, self.op1, self.op2)
            elif self.op1 != None:
                self.body += '\t%s\t%s' % (self.cmd, self.op1)
            else:
                self.body += '\t%s' % (self.cmd,)
                
            if self.cmd.lower() not in self.directives:
                self.pmem += 1
            
            if len(self.pages) > 1 and self.op1 and self.cmd == 'call':
                self.body += '\n\tpagesel $+1'
                self.pmem += 2

            self.body += self.comment+'\n'

        if self.fix_test and self.fix_test_enabled:
            self.body += self.uvars['var_test'].get_bank(self)
            self.body += '\tmovwf\tvar_test\n'
            self.body += '\tmovf\tvar_test,\tf\n'
            self.pmem += 2
            
        if self.fix_cond_br and self.pmem > 1:
            lbl_if = Label('ao_if', used = True).get_label()
            lbl_exit = Label('ao_exit', used = True).get_label()
            
            self.body = (
                      ('\tgoto\t%s\n' % lbl_if)
                    + ('\tgoto\t%s\n' % lbl_exit)
                    + lbl_if + '\n'
                    + self.body
                    + lbl_exit + '\n')
            
            self.bank_after = None
            
            self.pmem += 2

    def __str__(self):
        return 'AsmObject(cmd=%s, op1=%s, op2=%s, verbatim=%s)' % (
                repr(self.cmd),
                repr(self.op1),
                repr(self.op2),
                repr(self.verbatim))
    
class Label(AsmObject):
    next_id = 0
    
    def __init__(self, prefix = 'label', fix_test = False, used = False):
        self.used = used
        self.prefix = prefix
        self.uid = None
        AsmObject.__init__(self, verbatim = True)
        self.fix_test = fix_test
        self.fix_test_enabled = False
        self.pmem = 0

    def finalize(self):
        self.bank_after = None
        
        if self.used:
            self.set_uid()
            self.body = '%s\n' % self.get_label()
            bank_after = None
        else:
            self.body = ''

        if self.fix_test and self.fix_test_enabled:
            self.body += self.uvars['var_test'].get_bank(self)
            self.body += '\tmovwf\tvar_test\n'
            self.body += '\tmovf\tvar_test,\tf\n'
            self.pmem += 2

    def get_label(self):
        self.set_uid()
        return '%s_%i' % (self.prefix, self.uid)
    
    def set_uid(self):
        if self.uid == None:
            self.uid = Label.next_id
            Label.next_id += 1

#     def __str__(self):
#         return self.get_label()+' ;label'

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

class Variable:
    """
    Represents a variable or special register.

    Variable lifecycle:
      - Reserve a name.
      - Approve that the variable is used.
      - Statically allocate memory for the variable.

    @ivar special: True if variable is a special file register.

    @cvar mmap: Memory map.
    @cvar hdikt: Dictionary of processor-specific register names.
    """
    def __init__(self, name, addr = None, used = False, special = False):
        """
        @param name: Name of the variable to be created.
        @param care: True if the function should warn if the variable is
          already defined.
        @param addr: Memory address that should be allocated.
        @param special: True if variable is a special file register.
        """
        global ERROR
        
        self.used = used
        self.addr = addr
        self.name = name
        self.special = special
        
        if not special and addr != None:
            try:
                self.mmap.reserve_byte(addr)
            except:
                self.say("address %i is not allocatable" % addr, WARNING)
                return
            
    def get_addr(self):
        global ERROR
        if self.addr == None:
            try:
                self.addr=self.mmap.reserve_byte()
            except:
                self.say("program does not fit RAM.", ERROR)
                self.uvars[name]=None
                return
        
        return self.addr
            
    def get_bank(self, ao):
        """
        Get assembler code that switches banks to the variable bank.
        """
        addr = self.addr
        if self.name in self.hdikt:
            if self.name.lower() in ao.bank_indep:
                return ''
            addr = self.hdikt[self.name]

        bank = addr >> 7
        addr7 = addr & 0x7f

        if ao.maxram < 0x80 or (not 'RP0' in self.hdikt):
            return ''
        
        ret=''
        if ao.bank_before != None:
            for block in ao.shareb:
                addr_in_block = False
                curr_block_has = False
            
                for sub in block:
                    if sub[0] <= addr <= sub[1]:
                        addr_in_block = True
                    
                    if sub[0] <= (addr7 | (sub[0] >> 7 << 7)) <= sub[1]:
                        curr_block_has = True
                
                if addr_in_block and curr_block_has:
                    return ''
        else:
            for block in ao.shareb:
                addr_in_block = False
                curr_block_has = True
            
                for sub in block:
                    if sub[0] <= addr7 <= sub[1]:
                        addr_in_block = True
                    
                    if  not (sub[0] <= (addr7 | (sub[0] >> 7 << 7)) <= sub[1]):
                        curr_block_has = False
                
                if addr_in_block:
                    if curr_block_has:
                        return ''
                    else:
                        break
            
        if ((ao.bank_before == None or (bank & 1) ^ (ao.bank_before & 1))):
            if bank & 1:
                ret += '\tbsf\tSTATUS,\tRP0\n'
            else:
                ret += '\tbcf\tSTATUS,\tRP0\n'
            ao.pmem += 1
           
        if ((ao.bank_before == None or ((bank & 2) ^ (ao.bank_before & 2)))
                and 'RP1' in self.hdikt):
            if bank & 2:
                ret += '\tbsf\tSTATUS,\tRP1\n'
            else:
                ret += '\tbcf\tSTATUS,\tRP1\n'
            ao.pmem += 1
            
        ao.bank_after = bank
        return ret

