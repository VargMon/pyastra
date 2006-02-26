############################################################################
# $Id$
#
# Description: PIC 16F506 definition. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################

"""
Pic 16F506 definition. U{Pyastra project <http://pyastra.sourceforge.net>}.

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

hdikt={'CAL5': 0x6, 'NOT_COUT1EN': 0x6, 'ADCS0': 0x4,
       'ADCS1': 0x5, 'CAL0': 0x1, 'VRCON': 0xc,
       'CAL2': 0x3, 'CAL3': 0x4, 'NOT_PD': 0x3,
       'DC': 0x1, 'CP2REF2': 0x4, 'FSR': 0x4,
       'NOT_TO': 0x4, 'PCL': 0x2, 'PS2': 0x2,
       'ADON': 0x0, 'PS0': 0x0, 'PS1': 0x1,
       'RBWUF': 0x7, 'CAL1': 0x2, 'OSCCAL': 0x5,
       'T0SE': 0x4, 'ADRES': 0xa, 'CMP1ON': 0x3,
       'NOT_CWU2': 0x0, 'NOT_CWU1': 0x0, 'NOT_COUT2EN': 0x6,
       'VR3': 0x3, 'NOT_RBPU': 0x6, 'VROE': 0x6,
       'STATUS': 0x3, 'VR2': 0x2, 'C': 0x0,
       'VR0': 0x0, 'CHS0': 0x2, 'CHS1': 0x3,
       'NOT_RBWU': 0x7, 'VRR': 0x5, 'C2POL': 0x5,
       'CAL4': 0x5, 'PORTB': 0x6, 'PORTC': 0x7,
       'CMCON0': 0x8, 'ADCON0': 0x9, 'CN2REF': 0x2,
       'NOT_CMP1T0CS': 0x4, 'Z': 0x2, 'PA0': 0x5,
       'T0CS': 0x5, 'ANS0': 0x6, 'PSA': 0x3,
       'NOT_DONE': 0x1, 'CWUF': 0x6, 'INDF': 0x0,
       'TMR0': 0x1, 'C1POL': 0x5, 'CN1REF': 0x2,
       'CMP2ON': 0x3, }

pages=((0x0, 0x1FF), (0x200, 0x3FF), )

banks=((0x0D, 0x0F), (0x10, 0x1F), (0x30, 0x3F), (0x50, 0x5F), (0x70, 0x7F), )

shareb=(
        ((0x0D, 0x0F), (0x2D, 0x2F), (0x4D, 0x4F), (0x6D, 0x6F), ),
)

vectors=None
maxram = 0x7f