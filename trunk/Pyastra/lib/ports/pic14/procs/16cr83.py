############################################################################
# $Id$
#
# Description: PIC 16CR83 definition. Pyastra project.
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

hdikt={'RP1': 0x6, 'PCLATH': 0xa, 'T0IF': 0x2,
       'T0IE': 0x5, 'WREN': 0x2, 'NOT_PD': 0x3,
       'DC': 0x1, 'FSR': 0x4, 'NOT_TO': 0x4,
       'INTCON': 0xb, 'WR': 0x1, 'PCL': 0x2,
       'PS2': 0x2, 'PS0': 0x0, 'PS1': 0x1,
       'EEADR': 0x9, 'T0SE': 0x4, 'EEDATA': 0x8,
       'RD': 0x0, 'NOT_RBPU': 0x7, 'STATUS': 0x3,
       'RP0': 0x5, 'C': 0x0, 'INTF': 0x1,
       'EEIE': 0x6, 'EEIF': 0x4, 'IRP': 0x7,
       'TRISB': 0x86, 'TRISA': 0x85, 'PORTB': 0x6,
       'PORTA': 0x5, 'OPTION_REG': 0x81, 'INTEDG': 0x6,
       'Z': 0x2, 'WRERR': 0x3, 'T0CS': 0x5,
       'INTE': 0x4, 'EECON1': 0x88, 'EECON2': 0x89,
       'PSA': 0x3, 'GIE': 0x7, 'INDF': 0x0,
       'TMR0': 0x1, 'RBIF': 0x0, 'RBIE': 0x3,
       }

pages=((0x5, 0x1FF), )

banks=((0xC, 0x2F), )

shareb=(
)
