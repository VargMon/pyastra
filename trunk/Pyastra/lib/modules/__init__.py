############################################################################
# $Id$
#
# Description: port-independent modules. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################
"""
Port-independent modules. U{Pyastra project <http://pyastra.sourceforge.net>}.

This package contains all modules that can be compiled for any target port. At the moment, these modules have to include no inline assembler conde and don't to use any port-specific variables.

In the future versions of Pyastra meta variables are planned to be provided by the compiler. These variables will let the programmer to make multi-target code. It will be something like that::

    if pyastra.port == 'pic16':
        asm(\"""
            btfsc   STATUS, Z
            goto    cont
            incf    _my_var1
            decf    _my_var2
        cont
        \""")
    elif port == 'pic18':
        asm(\"""
            bz      cont
            incf    _my_var1
            decf    _my_var2
        cont
        \""")
    else:
        raise pyastra.InlineException('Platform %s is not supported by the module!' % pyastra.port)

All port-specific modules are stored in port's package.

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

