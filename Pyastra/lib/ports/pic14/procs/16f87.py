############################################################################
# $Id$
#
# Description: PIC 16F87 definition. Pyastra project.
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

hdikt={'RCIF': 0x5, 'NOT_T1SYNC': 0x2, 'BF': 0x0,
       'RCIE': 0x5, 'CVR0': 0x0, 'CM0': 0x0,
       'C1INV': 0x4, 'CKP': 0x4, 'T2CON': 0x12,
       'T1CON': 0x10, 'CVR2': 0x2, 'T0SE': 0x4,
       'SPBRG': 0x99, 'OSCCON': 0x8f, 'RX9': 0x6,
       'CVREN': 0x7, 'CVRR': 0x5, 'PIE2': 0x8d,
       'PIE1': 0x8c, 'TMR1ON': 0x0, 'D': 0x5,
       'CVRCON': 0x9d, 'PORTB': 0x6, 'PORTA': 0x5,
       'P': 0x4, 'GIE': 0x7, 'NOT_A': 0x5,
       'PR2': 0x92, 'CVR1': 0x1, 'INTEDG': 0x6,
       'CVR3': 0x3, 'SMP': 0x7, 'OSCTUNE': 0x90,
       'C2INV': 0x5, 'T0CS': 0x5, 'EECON1': 0x18c,
       'EECON2': 0x18d, 'SSPBUF': 0x13, 'TXIF': 0x4,
       'TXIE': 0x4, 'SPEN': 0x7, 'WDTPS3': 0x4,
       'WDTPS0': 0x1, 'WDTPS1': 0x2, 'WDTPS2': 0x3,
       'TXSTA': 0x98, 'INTE': 0x4, 'PEIE': 0x6,
       'SREN': 0x5, 'SSPIE': 0x3, 'SSPIF': 0x3,
       'CMIF': 0x6, 'T2CKPS0': 0x0, 'T2CKPS1': 0x1,
       'INTCON': 0xb, 'PCL': 0x2, 'PS2': 0x2,
       'PS0': 0x0, 'TMR1H': 0xf, 'TMR1L': 0xe,
       'CCP1M2': 0x2, 'CCP1M3': 0x3, 'CCP1M0': 0x0,
       'CCP1M1': 0x1, 'CVROE': 0x6, 'ADDEN': 0x3,
       'TMR1CS': 0x1, 'IRP': 0x7, 'NOT_RBPU': 0x7,
       'SWDTE': 0x0, 'C': 0x0, 'TRISB': 0x86,
       'TRISA': 0x85, 'OPTION_REG': 0x81, 'WR': 0x1,
       'PIR2': 0xd, 'PIR1': 0xc, 'IRCF0': 0x4,
       'OERR': 0x1, 'RP1': 0x6, 'PSA': 0x3,
       'S': 0x3, 'I2C_READ': 0x2, 'CREN': 0x4,
       'UA': 0x1, 'RBIF': 0x0, 'RBIE': 0x3,
       'TXREG': 0x19, 'T1OSCEN': 0x3, 'PCLATH': 0xa,
       'SSPSTAT': 0x94, 'PCON': 0x8e, 'OSTS': 0x3,
       'TOUTPS2': 0x5, 'TOUTPS3': 0x6, 'TOUTPS0': 0x3,
       'TOUTPS1': 0x4, 'FSR': 0x4, 'T1RUN': 0x6,
       'NOT_W': 0x2, 'RX9D': 0x0, 'SSPOV': 0x6,
       'I2C_STOP': 0x4, 'RD': 0x0, 'CCP1CON': 0x17,
       'RCREG': 0x1a, 'EEDATH': 0x10e, 'CKE': 0x6,
       'EEDATA': 0x10c, 'IRCF2': 0x6, 'C1OUT': 0x6,
       'IRCF1': 0x5, 'D_A': 0x5, 'WREN': 0x2,
       'SCS1': 0x1, 'SCS0': 0x0, 'EEADRH': 0x10f,
       'TMR2IE': 0x1, 'TMR2IF': 0x1, 'SYNC': 0x4,
       'NOT_BO': 0x0, 'R': 0x2, 'CMIE': 0x6,
       'Z': 0x2, 'C2OUT': 0x7, 'NOT_WRITE': 0x2,
       'SSPADD': 0x93, 'T1CKPS0': 0x4, 'TXEN': 0x5,
       'NOT_TO': 0x4, 'SSPCON': 0x14, 'TMR2': 0x11,
       'TMR0': 0x1, 'IOFS': 0x2, 'BRGH': 0x2,
       'CCPR1L': 0x15, 'READ_WRITE': 0x2, 'CCPR1H': 0x16,
       'NOT_PD': 0x3, 'DC': 0x1, 'CIS': 0x3,
       'FERR': 0x2, 'RCSTA': 0x18, 'R_W': 0x2,
       'EEADR': 0x10d, 'TRMT': 0x1, 'PS1': 0x1,
       'SSPEN': 0x5, 'TUN3': 0x3, 'TUN2': 0x2,
       'TUN1': 0x1, 'TUN0': 0x0, 'CMCON': 0x9c,
       'TUN5': 0x5, 'TUN4': 0x4, 'TMR0IF': 0x2,
       'TMR0IE': 0x5, 'SWDTEN': 0x0, 'WCOL': 0x7,
       'NOT_POR': 0x1, 'STATUS': 0x3, 'RP0': 0x5,
       'T1CKPS1': 0x5, 'INTF': 0x1, 'EEIE': 0x4,
       'EEPGD': 0x7, 'EEIF': 0x4, 'CCP1IF': 0x2,
       'CCP1IE': 0x2, 'CCP1X': 0x5, 'CCP1Y': 0x4,
       'WRERR': 0x3, 'CSRC': 0x7, 'FREE': 0x4,
       'TX9': 0x6, 'TMR2ON': 0x2, 'TMR1IF': 0x0,
       'TMR1IE': 0x0, 'WDTCON': 0x105, 'SSPM0': 0x0,
       'SSPM1': 0x1, 'SSPM2': 0x2, 'SSPM3': 0x3,
       'DATA_ADDRESS': 0x5, 'I2C_START': 0x3, 'NOT_ADDRESS': 0x5,
       'CM2': 0x2, 'INDF': 0x0, 'OSFIF': 0x7,
       'CM1': 0x1, 'OSFIE': 0x7, 'TX9D': 0x0,
       'I2C_DATA': 0x5, }

pages=((0x5, 0x7FF), (0x800, 0xFFF), )

banks=((0x20, 0x6F), (0x70, 0x7F), (0xA0, 0xEF), (0x110, 0x16F), (0x190, 0x1EF), )

shareb=(
        ((0x70, 0x7F), (0xF0, 0xFF), (0x170, 0x17F), (0x1F0, 0x1FF), ),
)

vectors=(0x0, 0x4)
maxram = 0x1ff