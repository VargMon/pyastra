############################################################################
# $Id$
#
# Description: PIC 16CE623 definition. Pyastra project.
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

hdikt={'RP1': 0x6, 'PEIE': 0x6, 'PCLATH': 0xa,
       'T0IF': 0x2, 'T0IE': 0x5, 'VR2': 0x2,
       'PCON': 0x8e, 'VRCON': 0x9f, 'VR0': 0x0,
       'NOT_PD': 0x3, 'DC': 0x1, 'CMIE': 0x6,
       'EESDA': 0x1, 'CIS': 0x3, 'FSR': 0x4,
       'NOT_TO': 0x4, 'INTCON': 0xb, 'VREN': 0x7,
       'PCL': 0x2, 'PS2': 0x2, 'PS0': 0x0,
       'PS1': 0x1, 'VRR': 0x5, 'T0SE': 0x4,
       'EESCL': 0x2, 'NOT_POR': 0x1, 'CMCON': 0x1f,
       'CMIF': 0x6, 'C1OUT': 0x6, 'NOT_RBPU': 0x7,
       'VROE': 0x6, 'PIE1': 0x8c, 'STATUS': 0x3,
       'RP0': 0x5, 'C': 0x0, 'INTF': 0x1,
       'IRP': 0x7, 'TRISB': 0x86, 'TRISA': 0x85,
       'PORTB': 0x6, 'PORTA': 0x5, 'NOT_BO': 0x0,
       'OPTION_REG': 0x81, 'EEVDD': 0x0, 'INTEDG': 0x6,
       'Z': 0x2, 'C2OUT': 0x7, 'PIR1': 0xc,
       'EEINTF': 0x90, 'NOT_BOR': 0x0, 'T0CS': 0x5,
       'INTE': 0x4, 'VR3': 0x3, 'PSA': 0x3,
       'VR1': 0x1, 'GIE': 0x7, 'CM2': 0x2,
       'INDF': 0x0, 'CM1': 0x1, 'TMR0': 0x1,
       'RBIF': 0x0, 'RBIE': 0x3, 'CM0': 0x0,
       }

pages=((0x5, 0x1FF), )

banks=((0x20, 0x6F), (0x70, 0x7F), )

shareb=(
        ((0x70, 0x7F), (0xF0, 0xFF), ),
)
