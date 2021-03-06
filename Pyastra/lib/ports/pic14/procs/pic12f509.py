############################################################################
# $Id$
#
# Description: PIC 12F509 definition. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################

"""
Pic 12F509 definition. U{Pyastra project <http://pyastra.sourceforge.net>}.

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

hdikt={'NOT_GPPU': 0x6, 'CAL0': 0x1, 'CAL1': 0x2,
       'CAL2': 0x3, 'CAL3': 0x4, 'NOT_PD': 0x3,
       'DC': 0x1, 'CAL6': 0x7, 'FSR': 0x4,
       'NOT_TO': 0x4, 'GPWUF': 0x7, 'PCL': 0x2,
       'PS2': 0x2, 'GPIO': 0x6, 'PS0': 0x0,
       'PS1': 0x1, 'OSCCAL': 0x5, 'T0SE': 0x4,
       'STATUS': 0x3, 'C': 0x0, 'CAL4': 0x5,
       'NOT_GPWU': 0x7, 'CAL5': 0x6, 'Z': 0x2,
       'PA0': 0x5, 'T0CS': 0x5, 'PSA': 0x3,
       'INDF': 0x0, 'TMR0': 0x1, }

pages=((0x0, 0x1FF), (0x200, 0x3FF), )

banks=((0x07, 0x0F), (0x10, 0x1F), (0x30, 0x3F), )

shareb=(
        ((0x07, 0x0F), (0x27, 0x2F), ),
)

vectors=None
maxram = 0x3f