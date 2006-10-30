############################################################################
# $Id: __init__.py 112 2006-02-26 03:42:22Z estyler $
#
# Description: pic16 processor definitions. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################
"""
Pic16 processor definitions. U{Pyastra project <http://pyastra.sourceforge.net>}.

All the processors must be listed in the C{__all__} dictionary to be
enabled. Files whose name end with "i" are definitions for processors with
ICD mode enabled.

Pyastra is shipped with C{inc2py.py} script that converts C{*.lkr} and
C{*.inc} files from the U{gputils <http://gputils.sourceforge.net>}
project into Pyastra processor definitions.

Every definition consists of:
    - B{hdikt:} Dictionary of registers. Keys are register names in
      uppercase and values are its 9-bit addresses.
    - B{pages:} Tuples with starts and ends of program memory pages.
    - B{banks:} Contains general-purpose register memory start and end
      addresses.
    - B{shareb:} Register memory addresses that are mirrored between each
      other. The tuples have the following format::
        shareb=(
            ((area11_start, area11_end), (area12_start, area12_end), ...),
            ((area21_start, area21_end), (area22_start, area22_end), ...),
            ...
        )
      Here area1 is from address C{area11_start} to C{area11_end} and its
      mirror is from address C{area12_start} to C{area12_end}.
    - B{vectors:} Tuple of interrupt vectors supported by the processor.
      Values are addresses.
    - B{maxram:} Maximal register address supported by the processor.

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

__all__ = [
        'pic18f4550',
]
