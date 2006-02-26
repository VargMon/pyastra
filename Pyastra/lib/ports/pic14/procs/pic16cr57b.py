############################################################################
# $Id$
#
# Description: PIC 16CR57B definition. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################

"""
Pic 16CR57B definition. U{Pyastra project <http://pyastra.sourceforge.net>}.

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

hdikt={'NOT_PD': 0x3, 'DC': 0x1, 'FSR': 0x4,
       'NOT_TO': 0x4, 'PCL': 0x2, 'PS2': 0x2,
       'PS0': 0x0, 'PS1': 0x1, 'T0SE': 0x4,
       'PORTC': 0x7, 'STATUS': 0x3, 'C': 0x0,
       'PORTB': 0x6, 'T0CS': 0x5, 'PORTA': 0x5,
       'Z': 0x2, 'PA0': 0x5, 'PA1': 0x6,
       'PA2': 0x7, 'PSA': 0x3, 'INDF': 0x0,
       'TMR0': 0x1, }

pages=((0x0, 0x1FF), (0x200, 0x3FF), (0x400, 0x5FF), (0x600, 0x7FF), )

banks=((0x8, 0xF), (0x10, 0x1F), (0x30, 0x3F), (0x50, 0x5F), (0x70, 0x7F), )

shareb=(
        ((0x8, 0xF), (0x28, 0x2F), (0x48, 0x4F), (0x68, 0x6F), ),
)

vectors=None
maxram = 0x7f