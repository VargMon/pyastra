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

##from compiler.ast import *
##from pyastra.ports.pic14.16f877 import *

class tree2tree:
##    consts={}
##    nconsts=[]
##    global hdikt
    
    def __init__(self, root):
        self.root=root
##        self.findConsts(self.root)
##        del self.nconsts
##        self.replaceAll(self.root)
##        
##    def findConsts(self, node):
##        if node==None:
##            return
##        elif isinstance(node, AssName):
##            if node.name in hdikt or node.name in self.nconsts:
##                return
##            if node.flags=='OP_ASSIGN':
##                if node.name in self.consts:
##                    self.nconsts.append(node.name)
##                    del self.consts[node.name]
##                else:
##                    
##                
##    def replaceAll(self, node):
##        print self.consts
