############################################################################
# $Id: lowlevel.py 112 2006-02-26 03:42:22Z estyler $
#
# Description: Lowlevel routines for pic16 port. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################
"""
Lowlevel routines for pic16 port.  U{Pyastra project
<http://pyastra.sourceforge.net>}.

This module contains lowlevel functions that can be excluded from the
convertor. Is B{not} imported by default.

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
"""

def halt():
    """
    Function halts the microcontroller till the reset. (It does an
    eternal loop.)
    """
    asm("""
        bra $
    """)

def sleep():
    """
    Turns microcontroller into the sleep mode.
    """
    asm("""
        sleep
        nop
    """)

def reset():
    """
    Software device reset
    """
    asm("""
        reset
    """)
