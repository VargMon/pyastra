############################################################################
# $Id$
#
# Description: PIC 16F877 default namespace. Pyastra project.
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

hdikt={'RCIF': (0x5, 0), 'NOT_T1SYNC': (0x2, 0), 'BF': (0x0, 0),
'RCIE': (0x5, 0), 'ACKSTAT': (0x6, 0), 'TMR1ON': (0x0, 0),
'CKP': (0x4, 0), 'T2CON': (0x12, 0), 'RCEN': (0x3, 0),
'T1CON': (0x10, 0), 'Z': (0x2, 0), 'T0SE': (0x4, 0),
'SPBRG': (0x19, 1), 'RX9': (0x6, 0), 'PCFG3': (0x3, 0),
'NOT_TX8': (0x6, 0), 'PCFG1': (0x1, 0), 'PCFG0': (0x0, 0),
'PIE2': (0xd, 1), 'PIE1': (0xc, 1), 'CCPR2H': (0x1c, 0),
'CCP2CON': (0x1d, 0), 'CCPR2L': (0x1b, 0), 'D': (0x5, 0),
'PORTD': (0x8, 0), 'PORTE': (0x9, 0), 'PORTB': (0x6, 0),
'PORTC': (0x7, 0), 'PORTA': (0x5, 0), 'P': (0x4, 0),
'GIE': (0x7, 0), 'TX8_9': (0x6, 0), 'NOT_A': (0x5, 0),
'PR2': (0x12, 1), 'GO': (0x2, 0), 'INTEDG': (0x6, 0),
'SMP': (0x7, 0), 'GCEN': (0x7, 0), 'WRERR': (0x3, 0),
'T0CS': (0x5, 0), 'ADRESL': (0x1e, 1), 'EECON1': (0xc, 3),
'EECON2': (0xd, 3), 'SSPBUF': (0x13, 0), 'ADRESH': (0x1e, 0),
'TXIF': (0x4, 0), 'TXIE': (0x4, 0), 'SPEN': (0x7, 0),
'RSEN': (0x1, 0), 'ACKDT': (0x5, 0), 'TXSTA': (0x18, 1),
'INTE': (0x4, 0), 'PEIE': (0x6, 0), 'SREN': (0x5, 0),
'SSPIE': (0x3, 0), 'SSPIF': (0x3, 0), 'TXD8': (0x0, 0),
'T1CKPS1': (0x5, 0), 'T2CKPS0': (0x0, 0), 'T2CKPS1': (0x1, 0),
'NOT_TO': (0x4, 0), 'CCP2Y': (0x4, 0), 'CCP2X': (0x5, 0),
'PCL': (0x2, -1), 'PS2': (0x2, 0), 'CHS0': (0x3, 0),
'PS0': (0x0, 0), 'PS1': (0x1, 0), 'TMR1L': (0xe, 0),
'CCP1M2': (0x2, 0), 'CCP1M3': (0x3, 0), 'CCP1M0': (0x0, 0),
'CCP1M1': (0x1, 0), 'TMR1IE': (0x0, 0), 'ADDEN': (0x3, 0),
'TMR1CS': (0x1, 0), 'CCP1IF': (0x2, 0), 'NOT_RBPU': (0x7, 0),
'I2C_STOP': (0x4, 0), 'BCLIE': (0x3, 0), 'C': (0x0, 0),
'BCLIF': (0x3, 0), 'ADON': (0x0, 0), 'CHS1': (0x4, 0),
'CHS2': (0x5, 0), 'TRISC': (0x7, 1), 'TRISB': (0x6, 1),
'TRISA': (0x5, 1), 'ADCON1': (0x1f, 1), 'ADCON0': (0x1f, 0),
'TRISE': (0x9, 1), 'TRISD': (0x8, 1), 'OPTION_REG': (0x1, 1),
'WR': (0x1, 0), 'PIR2': (0xd, 0), 'PIR1': (0xc, 0),
'SSPCON2': (0x11, 1), 'PSPIF': (0x7, 0), 'PSPIE': (0x7, 0),
'OERR': (0x1, 0), 'RP1': (0x6, 0), 'PSA': (0x3, 0),
'S': (0x3, 0), 'I2C_READ': (0x2, 0), 'ADFM': (0x7, 0),
'CREN': (0x4, 0), 'CCP2M1': (0x1, 0), 'CCP2M0': (0x0, 0),
'CCP2M3': (0x3, 0), 'CCP2M2': (0x2, 0), 'UA': (0x1, 0),
'RBIF': (0x0, 0), 'RBIE': (0x3, 0), 'TXREG': (0x19, 0),
'T1OSCEN': (0x3, 0), 'PCLATH': (0xa, 0), 'SSPSTAT': (0x14, 1),
'PCON': (0xe, 1), 'TOUTPS2': (0x5, 0), 'TOUTPS3': (0x6, 0),
'TOUTPS0': (0x3, 0), 'TOUTPS1': (0x4, 0), 'FSR': (0x4, -1),
'TRISE2': (0x2, 0), 'TRISE1': (0x1, 0), 'TRISE0': (0x0, 0),
'NOT_W': (0x2, 0), 'RX9D': (0x0, 0), 'SSPOV': (0x6, 0),
'CCPR1H': (0x16, 0), 'RD': (0x0, 0), 'CCP1CON': (0x17, 0),
'RCREG': (0x1a, 0), 'EEDATH': (0xe, 2), 'CKE': (0x6, 0),
'EEDATA': (0xc, 2), 'DATA_ADDRESS': (0x5, 0), 'NOT_RC8': (0x6, 0),
'SEN': (0x0, 0), 'D_A': (0x5, 0), 'WREN': (0x2, 0),
'INTF': (0x1, 0), 'EEADRH': (0xf, 2), 'OBF': (0x6, 0),
'TMR2IE': (0x1, 0), 'TMR2IF': (0x1, 0), 'T1INSYNC': (0x2, 0),
'SYNC': (0x4, 0), 'NOT_BO': (0x0, 0), 'R': (0x2, 0),
'ADIE': (0x6, 0), 'ADIF': (0x6, 0), 'PCFG2': (0x2, 0),
'PSPMODE': (0x4, 0), 'NOT_WRITE': (0x2, 0), 'SSPADD': (0x13, 1),
'NOT_DONE': (0x2, 0), 'TXEN': (0x5, 0), 'INTCON': (0xb, 0),
'SSPCON': (0x14, 0), 'TMR2': (0x11, 0), 'TMR0': (0x1, 0),
'BRGH': (0x2, 0), 'CCP2IE': (0x0, 0), 'CCPR1L': (0x15, 0),
'READ_WRITE': (0x2, 0), 'CCP2IF': (0x0, 0), 'T0IF': (0x2, 0),
'ADCS0': (0x6, 0), 'ADCS1': (0x7, 0), 'PEN': (0x2, 0),
'NOT_PD': (0x3, 0), 'DC': (0x1, 0), 'IBF': (0x7, 0),
'NOT_BOR': (0x0, 0), 'FERR': (0x2, 0), 'RCSTA': (0x18, 0),
'T0IE': (0x5, 0), 'R_W': (0x2, 0), 'EEADR': (0xd, 2),
'TRMT': (0x1, 0), 'TMR1H': (0xf, 0), 'SSPEN': (0x5, 0),
'ACKEN': (0x4, 0), 'GO_DONE': (0x2, 0), 'RCD8': (0x0, 0),
'WCOL': (0x7, 0), 'STATUS': (0x3, -1), 'RP0': (0x5, 0),
'RC8_9': (0x6, 0), 'T1CKPS0': (0x4, 0), 'EEIE': (0x4, 0),
'EEPGD': (0x7, 0), 'EEIF': (0x4, 0), 'IRP': (0x7, 0),
'CCP1IE': (0x2, 0), 'CCP1X': (0x5, 0), 'CCP1Y': (0x4, 0),
'T1SYNC': (0x2, 0), 'CSRC': (0x7, 0), 'TX9': (0x6, 0),
'TMR2ON': (0x2, 0), 'TMR1IF': (0x0, 0), 'IBOV': (0x5, 0),
'SSPM0': (0x0, 0), 'SSPM1': (0x1, 0), 'SSPM2': (0x2, 0),
'SSPM3': (0x3, 0), 'RC9': (0x6, 0), 'I2C_START': (0x3, 0),
'NOT_ADDRESS': (0x5, 0), 'INDF': (0x0, 0), 'NOT_POR': (0x1, 0),
'TX9D': (0x0, 0), 'I2C_DATA': (0x5, 0), }
