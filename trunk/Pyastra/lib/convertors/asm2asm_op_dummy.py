############################################################################
# $Id$
#
# Description: Dummy assembler "optimizer". Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2005 Alex Ziranov.  All rights reserved.
#
############################################################################
"""
Dummy assembler "optimizer".
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
"""

converts_from='asm'
converts_to='asm_op'

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
    modified=True
    ext='asm'
    meta={}
    
    def __init__(self, src, opts):
        self.data = src
