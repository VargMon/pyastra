############################################################################
# $Id$
#
# Description: PIC 16C765 definition. Pyastra project.
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
       'CRC5': 0x1, 'BD0IAL': 0x1a6, 'T2CON': 0x12,
       'T1CON': 0x10, 'PSPMODE': 0x4, 'UIE': 0x191,
       'SPBRG': 0x99, 'RESUME': 0x2, 'RX9': 0x6,
       'UIR': 0x190, 'ACTIVITY': 0x2, 'PCFG2': 0x2,
       'PCFG1': 0x1, 'PCFG0': 0x0, 'PIE2': 0x8d,
       'PIE1': 0x8c, 'CCPR2H': 0x1c, 'CCP2CON': 0x1d,
       'CCPR2L': 0x1b, 'BD1IAL': 0x1ae, 'TOUTPS2': 0x5,
       'PORTD': 0x8, 'PORTE': 0x9, 'PORTB': 0x6,
       'PORTC': 0x7, 'PORTA': 0x5, 'GIE': 0x7,
       'TOUTPS0': 0x3, 'PR2': 0x92, 'GO': 0x2,
       'INTEDG': 0x6, 'TOUTPS1': 0x4, 'FERR': 0x2,
       'T0CS': 0x5, 'WRT_ERR': 0x5, 'TXIF': 0x4,
       'TXIE': 0x4, 'SPEN': 0x7, 'PID_ERR': 0x0,
       'PID1': 0x3, 'PID0': 0x2, 'PID3': 0x5,
       'PID2': 0x4, 'TXSTA': 0x98, 'INTE': 0x4,
       'PEIE': 0x6, 'TRISE1': 0x1, 'SREN': 0x5,
       'BD1IBC': 0x1ad, 'SYNC': 0x4, 'T2CKPS0': 0x0,
       'T2CKPS1': 0x1, 'INTCON': 0xb, 'BD1OST': 0x1a8,
       'PCL': 0x2, 'BD1IST': 0x1ac, 'PS2': 0x2,
       'ADON': 0x0, 'PS0': 0x0, 'TMR1H': 0xf,
       'TMR1L': 0xe, 'CCP1M2': 0x2, 'CCP1M3': 0x3,
       'BD2OAL': 0x1b2, 'CCP1M1': 0x1, 'BD0IST': 0x1a4,
       'NOT_DONE': 0x2, 'TMR1CS': 0x1, 'UADDR': 0x196,
       'BD0OST': 0x1a0, 'CCP1IF': 0x2, 'DC1B1': 0x5,
       'DC1B0': 0x4, 'OWN_ERR': 0x6, 'C': 0x0,
       'PKT_DIS': 0x4, 'CHS0': 0x3, 'CHS1': 0x4,
       'CHS2': 0x5, 'TRISC': 0x87, 'TRISB': 0x86,
       'TRISA': 0x85, 'ADCON1': 0x9f, 'ADCON0': 0x1f,
       'TRISE': 0x89, 'TRISD': 0x88, 'SUSPND': 0x1,
       'OPTION_REG': 0x81, 'T0SE': 0x4, 'PIR2': 0xd,
       'PIR1': 0xc, 'UCTRL': 0x195, 'UERR': 0x1,
       'PSPIF': 0x7, 'PSPIE': 0x7, 'OERR': 0x1,
       'RP1': 0x6, 'PSA': 0x3, 'BD1OBC': 0x1a9,
       'CREN': 0x4, 'CCP2M1': 0x1, 'CCP2M0': 0x0,
       'CCP2M3': 0x3, 'CCP2M2': 0x2, 'RBIF': 0x0,
       'RBIE': 0x3, 'TXREG': 0x19, 'T1OSCEN': 0x3,
       'PCLATH': 0xa, 'PCON': 0x8e, 'UEP2': 0x19a,
       'TOUTPS3': 0x6, 'UEP0': 0x198, 'UEP1': 0x199,
       'FSR': 0x4, 'STALL': 0x5, 'TRISE2': 0x2,
       'BD2IST': 0x1b4, 'TRISE0': 0x0, 'BD0OAL': 0x1a2,
       'RX9D': 0x0, 'TOK_DNE': 0x3, 'DEV_ATT': 0x3,
       'T0IF': 0x2, 'CCP1CON': 0x17, 'RCREG': 0x1a,
       'ADCS0': 0x6, 'ADRES': 0x1e, 'USWSTAT': 0x197,
       'EP_IN_EN': 0x1, 'TMR1IE': 0x0, 'BD1OAL': 0x1aa,
       'EP_OUT_EN': 0x2, 'OWN': 0x7, 'DATA01': 0x6,
       'USTAT': 0x194, 'SE0': 0x5, 'OBF': 0x6,
       'BD0OBC': 0x1a1, 'USB_RST': 0x0, 'BD0IBC': 0x1a5,
       'TMR2IE': 0x1, 'TMR2IF': 0x1, 'NOT_BO': 0x0,
       'ADIE': 0x6, 'ADIF': 0x6, 'Z': 0x2,
       'ENDP0': 0x3, 'EP_STALL': 0x0, 'UEIR': 0x192,
       'UIDLE': 0x4, 'BD2OST': 0x1b0, 'T1CKPS0': 0x4,
       'UOWN': 0x7, 'TXEN': 0x5, 'NOT_TO': 0x4,
       'UEIE': 0x193, 'TMR2': 0x11, 'TMR0': 0x1,
       'BRGH': 0x2, 'CCP2IE': 0x0, 'CCPR1L': 0x15,
       'CCP2IF': 0x0, 'CCPR1H': 0x16, 'T0IE': 0x5,
       'ADCS1': 0x7, 'NOT_PD': 0x3, 'DC': 0x1,
       'IBF': 0x7, 'NOT_BOR': 0x0, 'USBIE': 0x3,
       'USBIF': 0x3, 'TMR1ON': 0x0, 'RCSTA': 0x18,
       'NOT_RBPU': 0x7, 'DTS': 0x3, 'BTO_ERR': 0x4,
       'TRMT': 0x1, 'PS1': 0x1, 'DC2B0': 0x4,
       'DC2B1': 0x5, 'GO_DONE': 0x2, 'BSTALL': 0x2,
       'BD2IAL': 0x1b6, 'NOT_POR': 0x1, 'STATUS': 0x3,
       'RP0': 0x5, 'T1CKPS1': 0x5, 'INTF': 0x1,
       'IRP': 0x7, 'CCP1IE': 0x2, 'DFN8': 0x3,
       'CCP1M0': 0x0, 'EP_CTL_DIS': 0x3, 'ENDP1': 0x4,
       'BTS_ERR': 0x7, 'CSRC': 0x7, 'TX9': 0x6,
       'IN': 0x2, 'TMR2ON': 0x2, 'TMR1IF': 0x0,
       'IBOV': 0x5, 'CRC16': 0x2, 'BD2IBC': 0x1b5,
       'INDF': 0x0, 'BD2OBC': 0x1b1, 'TX9D': 0x0,
       }

pages=((0x5, 0x7FF), (0x800, 0xFFF), (0x1000, 0x17FF), (0x1800, 0x1FFF), )

banks=((0x20, 0x6F), (0x70, 0x7F), (0xA0, 0xEF), (0x120, 0x16F), )

shareb=(
        ((0x70, 0x7F), (0xF0, 0xFF), (0x170, 0x17F), (0x1F0, 0x1FF), ),
)
maxram = 0x1fff