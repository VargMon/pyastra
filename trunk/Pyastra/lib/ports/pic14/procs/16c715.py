############################################################################
# $Id$
#
# Description: PIC 16C715 definition. Pyastra project.
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
       'T0IF': 0x2, 'T0IE': 0x5, 'ADCS1': 0x7,
       'PCON': 0x8e, 'NOT_PD': 0x3, 'DC': 0x1,
       'NOT_MPE': 0x2, 'FSR': 0x4, 'NOT_TO': 0x4,
       'INTCON': 0xb, 'PCL': 0x2, 'PS2': 0x2,
       'ADON': 0x0, 'PS0': 0x0, 'PS1': 0x1,
       'PORTB': 0x6, 'T0SE': 0x4, 'ADCS0': 0x6,
       'ADRES': 0x1e, 'NOT_POR': 0x1, 'GO_DONE': 0x2,
       'NOT_RBPU': 0x7, 'PCFG1': 0x1, 'PCFG0': 0x0,
       'PIE1': 0x8c, 'STATUS': 0x3, 'RP0': 0x5,
       'C': 0x0, 'INTF': 0x1, 'CHS0': 0x3,
       'CHS1': 0x4, 'CHS2': 0x5, 'IRP': 0x7,
       'TRISB': 0x86, 'TRISA': 0x85, 'ADCON1': 0x9f,
       'ADCON0': 0x1f, 'PORTA': 0x5, 'NOT_BO': 0x0,
       'OPTION_REG': 0x81, 'ADIE': 0x6, 'ADIF': 0x6,
       'GO': 0x2, 'INTEDG': 0x6, 'Z': 0x2,
       'PIR1': 0xc, 'NOT_BOR': 0x0, 'T0CS': 0x5,
       'INTE': 0x4, 'PSA': 0x3, 'GIE': 0x7,
       'NOT_DONE': 0x2, 'INDF': 0x0, 'TMR0': 0x1,
       'RBIF': 0x0, 'RBIE': 0x3, }

pages=((0x5, 0x7FF), )

banks=((0x20, 0x7F), (0xA0, 0xBF), )

shareb=(
)
maxram = 0x7ff