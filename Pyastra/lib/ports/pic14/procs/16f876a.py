############################################################################
# $Id$
#
# Description: PIC 16F876A definition. Pyastra project.
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
       'RCIE': 0x5, 'ACKSTAT': 0x6, 'CM0': 0x0,
       'CVR1': 0x1, 'C1INV': 0x4, 'CKP': 0x4,
       'T2CON': 0x12, 'RCEN': 0x3, 'T1CON': 0x10,
       'CVR2': 0x2, 'T0SE': 0x4, 'SPBRG': 0x99,
       'RX9': 0x6, 'CVREN': 0x7, 'PCFG3': 0x3,
       'PCFG2': 0x2, 'PCFG1': 0x1, 'CVRR': 0x5,
       'PIE2': 0x8d, 'PIE1': 0x8c, 'CCPR2H': 0x1c,
       'CCP2CON': 0x1d, 'CCPR2L': 0x1b, 'D': 0x5,
       'CVRCON': 0x9d, 'PORTB': 0x6, 'PORTC': 0x7,
       'PORTA': 0x5, 'P': 0x4, 'GIE': 0x7,
       'NOT_A': 0x5, 'PR2': 0x92, 'GO': 0x2,
       'INTEDG': 0x6, 'CVR3': 0x3, 'SMP': 0x7,
       'GCEN': 0x7, 'C2INV': 0x5, 'T0CS': 0x5,
       'ADRESL': 0x9e, 'EECON1': 0x18c, 'EECON2': 0x18d,
       'SSPBUF': 0x13, 'ADRESH': 0x1e, 'TXIF': 0x4,
       'TXIE': 0x4, 'SPEN': 0x7, 'ACKDT': 0x5,
       'TXSTA': 0x98, 'INTE': 0x4, 'PEIE': 0x6,
       'T1SYNC': 0x2, 'SSPIE': 0x3, 'SSPIF': 0x3,
       'CVR0': 0x0, 'CMIF': 0x6, 'T2CKPS0': 0x0,
       'T2CKPS1': 0x1, 'INTCON': 0xb, 'CCP2Y': 0x4,
       'CCP2X': 0x5, 'PCL': 0x2, 'PS2': 0x2,
       'ADON': 0x0, 'PS0': 0x0, 'TMR1H': 0xf,
       'TMR1L': 0xe, 'CCP1M2': 0x2, 'CCP1M3': 0x3,
       'CCP1M0': 0x0, 'CCP1M1': 0x1, 'NOT_DONE': 0x2,
       'CVROE': 0x6, 'ADDEN': 0x3, 'TMR1CS': 0x1,
       'CCP1IF': 0x2, 'NOT_RBPU': 0x7, 'I2C_STOP': 0x4,
       'BCLIE': 0x3, 'C': 0x0, 'BCLIF': 0x3,
       'CHS0': 0x3, 'CHS1': 0x4, 'CHS2': 0x5,
       'TRISC': 0x87, 'TRISB': 0x86, 'TRISA': 0x85,
       'ADCON1': 0x9f, 'ADCON0': 0x1f, 'OPTION_REG': 0x81,
       'WR': 0x1, 'PIR2': 0xd, 'PIR1': 0xc,
       'SSPCON2': 0x91, 'OERR': 0x1, 'RP1': 0x6,
       'PSA': 0x3, 'S': 0x3, 'I2C_READ': 0x2,
       'ADFM': 0x7, 'CREN': 0x4, 'CCP2M1': 0x1,
       'CCP2M0': 0x0, 'CCP2M3': 0x3, 'CCP2M2': 0x2,
       'UA': 0x1, 'RBIF': 0x0, 'RBIE': 0x3,
       'TXREG': 0x19, 'T1OSCEN': 0x3, 'PCLATH': 0xa,
       'SSPSTAT': 0x94, 'PCON': 0x8e, 'TOUTPS2': 0x5,
       'TOUTPS3': 0x6, 'TOUTPS0': 0x3, 'TOUTPS1': 0x4,
       'FSR': 0x4, 'NOT_W': 0x2, 'RX9D': 0x0,
       'SSPOV': 0x6, 'ADCS0': 0x6, 'T0IF': 0x2,
       'RD': 0x0, 'CCP1CON': 0x17, 'RCREG': 0x1a,
       'EEDATH': 0x10e, 'CKE': 0x6, 'EEDATA': 0x10c,
       'DATA_ADDRESS': 0x5, 'C1OUT': 0x6, 'D_A': 0x5,
       'WREN': 0x2, 'EEADRH': 0x10f, 'FERR': 0x2,
       'TMR2IE': 0x1, 'TMR2IF': 0x1, 'SYNC': 0x4,
       'NOT_BO': 0x0, 'R': 0x2, 'ADIE': 0x6,
       'ADIF': 0x6, 'Z': 0x2, 'C2OUT': 0x7,
       'NOT_WRITE': 0x2, 'CIS': 0x3, 'PCFG0': 0x0,
       'SSPADD': 0x93, 'T1CKPS0': 0x4, 'TXEN': 0x5,
       'NOT_TO': 0x4, 'SSPCON': 0x14, 'TMR2': 0x11,
       'TMR0': 0x1, 'BRGH': 0x2, 'CCP2IE': 0x0,
       'CCPR1L': 0x15, 'READ_WRITE': 0x2, 'CCP2IF': 0x0,
       'CCPR1H': 0x16, 'T0IE': 0x5, 'ADCS1': 0x7,
       'PEN': 0x2, 'NOT_PD': 0x3, 'DC': 0x1,
       'NOT_BOR': 0x0, 'TMR1ON': 0x0, 'RCSTA': 0x18,
       'R_W': 0x2, 'EEADR': 0x10d, 'TRMT': 0x1,
       'PS1': 0x1, 'SSPEN': 0x5, 'ACKEN': 0x4,
       'GO_DONE': 0x2, 'CMCON': 0x9c, 'WCOL': 0x7,
       'STATUS': 0x3, 'RP0': 0x5, 'T1CKPS1': 0x5,
       'INTF': 0x1, 'EEIE': 0x4, 'EEPGD': 0x7,
       'EEIF': 0x4, 'IRP': 0x7, 'CCP1IE': 0x2,
       'CCP1X': 0x5, 'CCP1Y': 0x4, 'CMIE': 0x6,
       'SREN': 0x5, 'CSRC': 0x7, 'TX9': 0x6,
       'TMR2ON': 0x2, 'TMR1IF': 0x0, 'TMR1IE': 0x0,
       'SSPM0': 0x0, 'SSPM1': 0x1, 'SSPM2': 0x2,
       'SSPM3': 0x3, 'I2C_START': 0x3, 'NOT_ADDRESS': 0x5,
       'CM2': 0x2, 'INDF': 0x0, 'NOT_POR': 0x1,
       'CM1': 0x1, 'WRERR': 0x3, 'TX9D': 0x0,
       'I2C_DATA': 0x5, }

pages=((0x5, 0x7FF), (0x800, 0xFFF), (0x1000, 0x17FF), (0x1800, 0x1FFF), )

banks=((0x20, 0x6F), (0x70, 0x7F), (0xA0, 0xEF), (0x110, 0x16F), (0x190, 0x1EF), )

shareb=(
        ((0x70, 0x7F), (0xF0, 0xFF), (0x170, 0x17F), (0x1F0, 0x1FF), ),
)

vectors=(0x0, 0x4)
maxram = 0x1ff