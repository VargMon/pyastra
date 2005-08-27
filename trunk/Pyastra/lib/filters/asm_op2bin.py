############################################################################
# $Id$
#
# Description: pic14 assembler to hex filter. Pyastra project.
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
"Pyastra filter: asm_op2bin"
import os, os.path, pyastralib

converts_from='asm_op'
converts_to='bin'

def get_ports():
    return []

def get_procs(port):
    return []

class Filter:
    ext='hex'
    ASSEMBLERS=(('gpasm', ''), ('gpasm.exe', ''), ('mpasm.exe', ''), ('mpasmwin.exe', ''),)
    meta={}

    def __init__(self, src, opts):
        say=opts['converter'].say
        self.modified=0
        infile=opts.get('infile')
        if infile:
            asm_fn=os.path.splitext(infile)[0]
        else:
            try:
                asm_fn=self.tmp_asm()
            except:
                say("Can't find appropriate temporary file name!", level=pyastralib.ERROR)
                return
        asm_file=file(asm_fn+'.asm', 'w')
        asm_file.write(src)
        asm_file.close()

        if os.environ.has_key('PATH'):
            paths=os.environ['PATH']
        else:
            paths=os.path.defpath

        asm_path=None
        for path in paths.split(os.pathsep):
            if path[0]==path[-1] and path[0] in ('"', '\''):
                path=path[1:-1]
            for fn, args in self.ASSEMBLERS:
                if os.access(os.path.join(path, fn), os.X_OK):
                    asm_path = os.path.join(path, fn)
                    asm = fn
                    asm_args = args
                    break

            if asm_path:
                break

        if asm_path:
            say('Assembling %s.asm with %s...' % (asm_fn, asm,))
            if os.system('"%s" %s.asm %s' % (asm_path, asm_fn, asm_args)):
                say('Assembling failed.', level=pyastralib.ERROR)
                return
            hex_file=file(asm_fn+'.hex')
            self.data=hex_file.read()
            hex_file.close()
            self.modified=1
        else:
            msg='No assembler found. Supported assemblers are:\n'
            for a in self.ASSEMBLERS:
                msg+='    %s\n' % a[0]

            say(msg, level=pyastralib.ERROR)
            

        try:
            os.remove(asm_fn+'.asm')
            os.remove(asm_fn+'.hex')
        except OSError:
            pass

    def tmp_asm(self):
        for i in xrange(100000):
            if not (os.path.exists('tmp%05i.asm' % i) or os.path.exists('tmp%05i.hex' % i)):
                return 'tmp%05i' % i
        raise "Can't find appropriate temporary file name!"
