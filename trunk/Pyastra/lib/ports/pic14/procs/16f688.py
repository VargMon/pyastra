############################################################################
# $Id$
#
# Description: PIC 16F688 definition. Pyastra project.
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
       'T1IF': 0x0, 'T1IE': 0x0, 'C1INV': 0x4,
       'WR': 0x1, 'BAUDCTL': 0x11, 'T0SE': 0x4,
       'SPBRG': 0x13, 'OSCCON': 0x8f, 'RX9': 0x6,
       'IOCA': 0x96, 'IOC': 0x96, 'PIE1': 0x8c,
       'TMR1ON': 0x0, 'TRMT': 0x1, 'WRERR': 0x3,
       'IOC1': 0x1, 'IOC0': 0x0, 'IOC3': 0x3,
       'IOC2': 0x2, 'IOC5': 0x5, 'PORTC': 0x7,
       'PORTA': 0x5, 'GIE': 0x7, 'GO': 0x1,
       'INTEDG': 0x6, 'OSCTUNE': 0x90, 'C2INV': 0x5,
       'T0CS': 0x5, 'ABDEN': 0x0, 'EECON1': 0x9c,
       'EECON2': 0x9d, 'TXIF': 0x1, 'TXIE': 0x1,
       'SPEN': 0x7, 'WDTPS3': 0x4, 'WDTPS0': 0x1,
       'WDTPS1': 0x2, 'WUE': 0x1, 'TXSTA': 0x16,
       'STATUS': 0x3, 'PEIE': 0x6, 'SREN': 0x5,
       'WREN': 0x2, 'SYNC': 0x4, 'ULPWUE': 0x5,
       'INTCON': 0xb, 'NOT_DONE': 0x1, 'PCL': 0x2,
       'PS2': 0x2, 'ADON': 0x0, 'PS0': 0x0,
       'PS1': 0x1, 'WDTPS2': 0x3, 'EEPGD': 0x7,
       'ADDEN': 0x3, 'TMR1CS': 0x1, 'VR3': 0x3,
       'ABDOVF': 0x7, 'SCS': 0x0, 'C': 0x0,
       'CHS0': 0x2, 'CHS1': 0x3, 'CHS2': 0x4,
       'TRISC': 0x87, 'VCFG': 0x6, 'TRISA': 0x85,
       'ADCON1': 0x9f, 'OPTION_REG': 0x81, 'IRCF2': 0x6,
       'PIR1': 0xc, 'IRCF0': 0x4, 'INTE': 0x4,
       'OERR': 0x1, 'C2IE': 0x4, 'C2IF': 0x4,
       'PSA': 0x3, 'VR1': 0x1, 'ADFM': 0x7,
       'HTS': 0x2, 'SBODEN': 0x4, 'CREN': 0x4,
       'RD': 0x0, 'CM2': 0x2, 'CM1': 0x1,
       'TX9D': 0x0, 'T1OSCEN': 0x3, 'PCLATH': 0xa,
       'PCON': 0x8e, 'OSTS': 0x3, 'IOC4': 0x4,
       'T1GINV': 0x7, 'FSR': 0x4, 'RX9D': 0x0,
       'IOCA4': 0x4, 'VRR': 0x5, 'RCREG': 0x14,
       'EEDATH': 0x97, 'WPU': 0x95, 'CM0': 0x0,
       'C1OUT': 0x6, 'BRG16': 0x3, 'IRCF1': 0x5,
       'LTS': 0x1, 'VR2': 0x2, 'ANSEL': 0x91,
       'VR0': 0x0, 'EEADRH': 0x98, 'NOT_BOD': 0x0,
       'ADIE': 0x6, 'ADIF': 0x6, 'Z': 0x2,
       'C2OUT': 0x7, 'ADCS2': 0x6, 'T1CKPS0': 0x4,
       'TXEN': 0x5, 'NOT_TO': 0x4, 'TMR0': 0x1,
       'SCKP': 0x4, 'BRGH': 0x2, 'VREN': 0x7,
       'IOCA1': 0x1, 'IOCA0': 0x0, 'IOCA3': 0x3,
       'IOCA2': 0x2, 'IOCA5': 0x5, 'T0IF': 0x2,
       'T0IE': 0x5, 'ADCS1': 0x5, 'VRCON': 0x99,
       'NOT_PD': 0x3, 'DC': 0x1, 'CIS': 0x3,
       'FERR': 0x2, 'RCSTA': 0x17, 'C2SYNC': 0x0,
       'C1IF': 0x3, 'C1IE': 0x3, 'ADCS0': 0x4,
       'TUN3': 0x3, 'TUN2': 0x2, 'GO_DONE': 0x1,
       'TUN0': 0x0, 'TUN4': 0x4, 'TMR1GE': 0x6,
       'SWDTEN': 0x0, 'WPUA': 0x95, 'NOT_RAPU': 0x7,
       'NOT_POR': 0x1, 'RP1': 0x6, 'RP0': 0x5,
       'T1CKPS1': 0x5, 'INTF': 0x1, 'EEIE': 0x7,
       'RAIE': 0x3, 'RAIF': 0x0, 'EEIF': 0x7,
       'IRP': 0x7, 'SPBRGH': 0x12, 'T1GSS': 0x1,
       'CSRC': 0x7, 'TX9': 0x6, 'RCIDL': 0x6,
       'TMR1IF': 0x0, 'TMR1IE': 0x0, 'WDTCON': 0x18,
       'ANS0': 0x0, 'ANS1': 0x1, 'ANS2': 0x2,
       'ANS3': 0x3, 'ANS4': 0x4, 'ANS5': 0x5,
       'ANS6': 0x6, 'ANS7': 0x7, 'INDF': 0x0,
       'OSFIF': 0x2, 'OSFIE': 0x2, 'SENDB': 0x3,
       'TXREG': 0x15, 'TUN1': 0x1, }

pages=((0x5, 0x7FF), (0x800, 0xFFF), )

banks=((0x20, 0x6F), (0x70, 0x7F), (0xA0, 0xEF), (0x120, 0x16F), )

shareb=(
        ((0x70, 0x7F), (0xF0, 0xFF), (0x170, 0x17F), (0x1F0, 0x1FF), ),
)
maxram = 0xfff