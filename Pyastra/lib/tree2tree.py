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

import os.path, compiler
from compiler.ast import *

class tree2tree:
    
    def __init__(self, root):
        self.root=root
        self.root.interrupts_on=0
        self.scan(self.root)

    def scan(self, node):
        if isinstance(node, list):
            for n in node:
                self.scan(n)
        elif isinstance(node, From):
            name='%s.py' % node.modname
            if not os.path.exists(name):
                name=os.path.join(pyastra.ports.pic14.__path__[0], name)
            root=compiler.parseFile(name)
            self.scan(root)
        elif isinstance(node, Function):
            if node.name == 'on_interrupt':
                self.root.interrupts_on=1
                return
        elif isinstance(node, Module):
            self.scan(node.node)
        elif isinstance(node, Stmt):
            self.scan(node.nodes)
        else:
            return
        
