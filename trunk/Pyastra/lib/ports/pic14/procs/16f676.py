############################################################################
# $Id$
#
# Description: PIC 16F676 definition. Pyastra project.
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

hdikt={'NOT_T1SYNC': 0x2, 'T1IF': 0x0, 'T1IE': 0x0,
       'WR': 0x1, 'T0SE': 0x4, 'NOT_POR': 0x1,
       'RD': 0x0, 'IOCA': 0x96, 'IOC': 0x96,
       'PIE1': 0x8c, 'TMR1ON': 0x0, 'PORTC': 0x7,
       'PORTA': 0x5, 'GIE': 0x7, 'GO': 0x1,
       'INTEDG': 0x6, 'WRERR': 0x3, 'T0CS': 0x5,
       'EECON1': 0x9c, 'EECON2': 0x9d, 'GO_DONE': 0x1,
       'CINV': 0x4, 'STATUS': 0x3, 'PEIE': 0x6,
       'COUT': 0x6, 'WREN': 0x2, 'CMIF': 0x3,
       'CMIE': 0x3, 'INTCON': 0xb, 'VREN': 0x7,
       'PCL': 0x2, 'PS2': 0x2, 'ADON': 0x0,
       'PS0': 0x0, 'PS1': 0x1, 'OSCCAL': 0x90,
       'TMR1CS': 0x1, 'T1CKPS0': 0x4, 'C': 0x0,
       'CHS0': 0x2, 'CHS1': 0x3, 'CHS2': 0x4,
       'TRISC': 0x87, 'ADCON1': 0x9f, 'TRISA': 0x85,
       'VCFG': 0x6, 'OPTION_REG': 0x81, 'PIR1': 0xc,
       'INTE': 0x4, 'PSA': 0x3, 'ADFM': 0x7,
       'CM2': 0x2, 'CM1': 0x1, 'CM0': 0x0,
       'T1OSCEN': 0x3, 'PCLATH': 0xa, 'PCON': 0x8e,
       'FSR': 0x4, 'VRR': 0x5, 'NOT_BOD': 0x0,
       'WPU': 0x95, 'CAL1': 0x3, 'VR3': 0x3,
       'VR2': 0x2, 'VR1': 0x1, 'VR0': 0x0,
       'CAL4': 0x6, 'CAL5': 0x7, 'ADIE': 0x6,
       'ADIF': 0x6, 'Z': 0x2, 'NOT_DONE': 0x1,
       'NOT_TO': 0x4, 'TMR0': 0x1, 'NOT_GPPU': 0x7,
       'ADCS2': 0x6, 'T0IF': 0x2, 'T0IE': 0x5,
       'ADCS1': 0x5, 'CAL0': 0x2, 'VRCON': 0x99,
       'CAL2': 0x4, 'CAL3': 0x5, 'NOT_PD': 0x3,
       'DC': 0x1, 'CIS': 0x3, 'ADCS0': 0x4,
       'TMR1GE': 0x6, 'WPUA': 0x95, 'RP1': 0x6,
       'RP0': 0x5, 'T1CKPS1': 0x5, 'INTF': 0x1,
       'EEIE': 0x7, 'RAIE': 0x3, 'RAIF': 0x0,
       'EEIF': 0x7, 'IRP': 0x7, 'TMR1IF': 0x0,
       'TMR1IE': 0x0, 'ANS0': 0x0, 'ANS1': 0x1,
       'ANS2': 0x2, 'ANS3': 0x3, 'ANS4': 0x4,
       'ANS5': 0x5, 'ANS6': 0x6, 'ANS7': 0x7,
       'INDF': 0x0, }

pages=((0x5, 0x3FE), )

banks=((0x20, 0x5F), )

shareb=(
        ((0x20, 0x5F), (0xA0, 0xDF), ),
)
maxram = 0xdf