############################################################################
# $Id$
#
# Description: PIC 16F627 definition. Pyastra project.
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

hdikt={'RCIF': 0x5, 'NOT_T1SYNC': 0x2, 'RCIE': 0x5,
       'C1INV': 0x4, 'WR': 0x1, 'T2CON': 0x12,
       'T1CON': 0x10, 'T0SE': 0x4, 'SPBRG': 0x99,
       'RX9': 0x6, 'PIE1': 0x8c, 'TMR1ON': 0x0,
       'TRMT': 0x1, 'WRERR': 0x3, 'PORTB': 0x6,
       'PORTA': 0x5, 'GIE': 0x7, 'PR2': 0x92,
       'INTEDG': 0x6, 'C2INV': 0x5, 'T0CS': 0x5,
       'EECON1': 0x9c, 'EECON2': 0x9d, 'TXIF': 0x4,
       'TXIE': 0x4, 'SPEN': 0x7, 'TXSTA': 0x98,
       'INTE': 0x4, 'PEIE': 0x6, 'SREN': 0x5,
       'WREN': 0x2, 'CMIF': 0x6, 'T2CKPS0': 0x0,
       'T2CKPS1': 0x1, 'INTCON': 0xb, 'VREN': 0x7,
       'PCL': 0x2, 'PS2': 0x2, 'PS0': 0x0,
       'TMR1H': 0xf, 'TMR1L': 0xe, 'CCP1M2': 0x2,
       'CCP1M3': 0x3, 'CCP1M0': 0x0, 'CCP1M1': 0x1,
       'TMR1CS': 0x1, 'IRP': 0x7, 'NOT_RBPU': 0x7,
       'C': 0x0, 'VRR': 0x5, 'TRISB': 0x86,
       'TRISA': 0x85, 'OPTION_REG': 0x81, 'PIR1': 0xc,
       'OERR': 0x1, 'RP1': 0x6, 'PSA': 0x3,
       'CREN': 0x4, 'OSCF': 0x3, 'RBIF': 0x0,
       'RBIE': 0x3, 'TXREG': 0x19, 'T1OSCEN': 0x3,
       'PCLATH': 0xa, 'PCON': 0x8e, 'TOUTPS2': 0x5,
       'TOUTPS3': 0x6, 'TOUTPS0': 0x3, 'TOUTPS1': 0x4,
       'FSR': 0x4, 'RX9D': 0x0, 'T0IF': 0x2,
       'RD': 0x0, 'CCP1CON': 0x17, 'RCREG': 0x1a,
       'NOT_BOD': 0x0, 'EEDATA': 0x9a, 'C1OUT': 0x6,
       'VROE': 0x6, 'VR3': 0x3, 'VR2': 0x2,
       'VR1': 0x1, 'VR0': 0x0, 'TMR2IE': 0x1,
       'TMR2IF': 0x1, 'SYNC': 0x4, 'NOT_BO': 0x0,
       'CMIE': 0x6, 'Z': 0x2, 'C2OUT': 0x7,
       'NOT_BOR': 0x0, 'T1CKPS0': 0x4, 'TXEN': 0x5,
       'NOT_TO': 0x4, 'TMR2': 0x11, 'TMR0': 0x1,
       'BRGH': 0x2, 'CCPR1L': 0x15, 'CCPR1H': 0x16,
       'T0IE': 0x5, 'VRCON': 0x9f, 'NOT_PD': 0x3,
       'DC': 0x1, 'CIS': 0x3, 'FERR': 0x2,
       'RCSTA': 0x18, 'EEADR': 0x9b, 'PS1': 0x1,
       'CMCON': 0x1f, 'TX9D': 0x0, 'ADEN': 0x3,
       'STATUS': 0x3, 'RP0': 0x5, 'T1CKPS1': 0x5,
       'INTF': 0x1, 'EEIE': 0x7, 'EEIF': 0x7,
       'CCP1IF': 0x2, 'CCP1IE': 0x2, 'CCP1X': 0x5,
       'CCP1Y': 0x4, 'CSRC': 0x7, 'TX9': 0x6,
       'TMR2ON': 0x2, 'TMR1IF': 0x0, 'TMR1IE': 0x0,
       'CM2': 0x2, 'INDF': 0x0, 'NOT_POR': 0x1,
       'CM1': 0x1, 'CM0': 0x0, }

pages=((0x5, 0x3FF), )

banks=((0x20, 0x6F), (0x70, 0x7F), (0xA0, 0xEF), (0x120, 0x14F), )

shareb=(
        ((0x70, 0x7F), (0xF0, 0xFF), (0x170, 0x17F), (0x1F0, 0x1FF), ),
)
maxram = 0x1ff