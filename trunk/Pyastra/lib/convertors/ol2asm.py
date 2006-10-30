############################################################################
# $Id$
#
# Description: pic14 assembler objects list to assembler convertor.
#              Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2005 Alex Ziranov.  All rights reserved.
#
############################################################################
"""
Pic14 assembler objects list to assembler convertor.
U{Pyastra project <http://pyastra.sourceforge.net>}.

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
@todo: To be finished.
@todo: Create new instruction counter that will take in account the pages.
@todo: Allocate banks in the following order (by banks): 0, 1, 3, 2 to
  decrease bank switching.
"""
import pyastra
from tree2ol import AsmObject, Label

converts_from = 'ol'
converts_to = 'asm'

def get_ports():
    """@return: A list of supported ports."""
    return []

def get_procs(port):
    """@return: A list of supported processors."""
    return []

class Convertor:
    """
    Main convertor class
    @see: L{convertors}
    """
    modified = False
    meta = {}
    ext = "asm"
    
    def __init__(self, src, opts):
        mem = src[0].uvars
        proc = opts['proc'][3:]
        self.data = """;
; Generated by %s
; infile: %s
;

\tprocessor\t%s
\t#include\tp%s.inc

""" % (pyastra.version, opts.get('infile', 'unknown'),
        proc, proc)
        
        for ao in src:
            ao.prepare()
        
        rmem = 0
        addr = 0
        
        for name in mem:
            var = mem[name]
            if var.used and not var.special:
                addr = var.get_addr()
                self.data += '%s\tequ\t%s\t;bank %g\n' % (name, hex(addr),
                        addr >> 7)
                rmem += 1

        curr_bank = None
        raw = False
        pmem = 0
        block_org = 0
        shift_org = 0
        block = ''
        page = 0
            
        for ao in src:
            if ao.org_enabled:
                self.data += block
                block = ''
                block_org += shift_org
                shift_org = 0
                
            ao.bank_before = curr_bank
            ao.pmem_before = pmem
            
            if opts['debug']:
                block += '\t;bank %s\n' % str(curr_bank)
                block += '\t;pmem %s\n' % hex(pmem)
                block += '\t;org %s + %s = %s\n'  % (hex(block_org),
                        hex(shift_org), hex(block_org + shift_org))
            ao.addr_max = addr
            ao.finalize()
            
            pmem += ao.pmem
            shift_org += ao.pmem

            if ao.cmd == 'org':
                new_org = int(ao.op1[2:], 16)
                if new_org < shift_org + block_org:
                    opts['pyastra'].say('Some parts of code overlap because of incorrect org directive usage',
                            pyastra.ERROR)
                    return
                shift_org = new_org - block_org
                
            if ao.raw:
                raw = True
                
            block += ao.body
            curr_bank = ao.bank_after
            if AsmObject.pages[page][1] < shift_org + block_org:
                page += 1
                if page >= len(AsmObject.pages):
                    opts['pyastra'].say('Program doesn\'t fit program memory!',
                            pyastra.ERROR)
                    return
                page_org = AsmObject.pages[page][0]
                block_org = page_org
                block = ('\torg\t%s\n' % hex(block_org)) + block

        self.data += block
        
        self.meta = {
            'pmem': pmem,
            'rmem': rmem,
            'raw': raw
            }
            
        self.modified = True

        # Print out some statistics
#         msg="""
# Peak RAM usage: %g byte(s) (%.1f%%)
# Program memory usage: %g word(s) (%.1f%%)""" % \
#         (self.ram_usage, self.ram_usage * 100. / gp_ram_max,
#          self.instr, self.instr * 100. / self.max_instr)
#         
#         if self.verbatim:
#             msg += "\nNOTE: statistics includes verbatim data specified in asm function!"

#         if opts['icd']:
#             msg += "\nNOTE: statistics includes ICD memory usage!"

#         opts['pyastra'].say(msg)
