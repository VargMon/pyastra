############################################################################
# $Id$
#
# Description: PIC 16F785 definition. Pyastra project.
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
       'PWMPH2': 0x114, 'WR': 0x1, 'PWMPH1': 0x113,
       'PH3': 0x3, 'PH2': 0x2, 'PWMCON1': 0x110,
       'PWMCON0': 0x111, 'PER1': 0x1, 'PH4': 0x4,
       'C2R': 0x2, 'VCFG': 0x6, 'NOT_POR': 0x1,
       'PH2EN': 0x1, 'OSCCON': 0x8f, 'RD': 0x0,
       'CVREN': 0x7, 'IOCA': 0x96, 'IOC': 0x96,
       'PIE1': 0x8c, 'TMR1ON': 0x0, 'PASEN': 0x6,
       'IOC1': 0x1, 'IOC0': 0x0, 'IOC3': 0x3,
       'IOC2': 0x2, 'PORTB': 0x6, 'PORTC': 0x7,
       'PORTA': 0x5, 'CM2CON1': 0x11b, 'CM2CON0': 0x11a,
       'GIE': 0x7, 'PER0': 0x0, 'PR2': 0x92,
       'GO': 0x1, 'INTEDG': 0x6, 'TOUTPS1': 0x4,
       'OSCTUNE': 0x90, 'WRERR': 0x3, 'T0CS': 0x5,
       'EECON1': 0x9c, 'EECON2': 0x9d, 'GO_DONE': 0x1,
       'WDTPS2': 0x3, 'WDTPS3': 0x4, 'WDTPS0': 0x1,
       'WDTPS1': 0x2, 'MC1OUT': 0x7, 'PWMP1': 0x6,
       'OVRLP': 0x7, 'PWMASE': 0x7, 'STATUS': 0x3,
       'PEIE': 0x6, 'PER3': 0x3, 'WREN': 0x2,
       'T2CON': 0x12, 'T2CKPS0': 0x0, 'T2CKPS1': 0x1,
       'ULPWUE': 0x5, 'INTCON': 0xb, 'NOT_DONE': 0x1,
       'PCL': 0x2, 'PS2': 0x2, 'ADON': 0x0,
       'PS0': 0x0, 'PS1': 0x1, 'PH1': 0x1,
       'CCP1M2': 0x2, 'CCP1M3': 0x3, 'CCP1M0': 0x0,
       'CCP1M1': 0x1, 'BLANK1': 0x4, 'TMR1CS': 0x1,
       'C1CH0': 0x0, 'C1CH1': 0x1, 'VR3': 0x3,
       'CCP1IF': 0x5, 'C2SP': 0x3, 'DC1B1': 0x5,
       'DC1B0': 0x4, 'WPUA2': 0x2, 'SCS': 0x0,
       'C': 0x0, 'CHS0': 0x2, 'CHS1': 0x3,
       'CHS2': 0x4, 'CHS3': 0x5, 'TRISC': 0x87,
       'TRISB': 0x86, 'TRISA': 0x85, 'ADCON1': 0x9f,
       'WPUA5': 0x5, 'PH0': 0x0, 'OPTION_REG': 0x81,
       'T0SE': 0x4, 'T1GSS': 0x1, 'IRCF2': 0x6,
       'PIR1': 0xc, 'IRCF0': 0x4, 'T1GE': 0x6,
       'C2OE': 0x5, 'INTE': 0x4, 'C1SP': 0x3,
       'T2IE': 0x1, 'C2IE': 0x4, 'OPA1CON': 0x11d,
       'T2IF': 0x1, 'VR1': 0x1, 'ADFM': 0x7,
       'HTS': 0x2, 'SBODEN': 0x4, 'REFCON': 0x98,
       'C1POL': 0x4, 'T1OSCEN': 0x3, 'PCLATH': 0xa,
       'PRSEN': 0x7, 'C1EN': 0x5, 'IOCA0': 0x0,
       'PCON': 0x8e, 'OPA2CON': 0x11e, 'TOUTPS2': 0x5,
       'TOUTPS3': 0x6, 'TOUTPS0': 0x3, 'T1GINV': 0x7,
       'FSR': 0x4, 'IOCA2': 0x2, 'ADCS2': 0x6,
       'WPUA0': 0x0, 'PWMP0': 0x5, 'T0IF': 0x2,
       'COMOD0': 0x5, 'VRR': 0x5, 'CCP1CON': 0x15,
       'NOT_BOD': 0x0, 'WPU': 0x95, 'OSTS': 0x3,
       'C1OUT': 0x6, 'ANS10': 0x2, 'ANS11': 0x3,
       'C1OE': 0x5, 'IRCF1': 0x5, 'WPUA1': 0x1,
       'VROE': 0x2, 'C1ON': 0x7, 'LTS': 0x1,
       'VR2': 0x2, 'ANSEL': 0x91, 'VR0': 0x0,
       'OPAON': 0x7, 'TMR2IE': 0x1, 'TMR2IF': 0x1,
       'C2POL': 0x4, 'PH1EN': 0x0, 'ADIE': 0x6,
       'ADIF': 0x6, 'SYNC1': 0x3, 'PER4': 0x4,
       'Z': 0x2, 'C2OUT': 0x6, 'C2CH0': 0x0,
       'COMOD1': 0x6, 'C2ON': 0x7, 'T1CKPS0': 0x4,
       'NOT_TO': 0x4, 'TMR2': 0x11, 'TMR0': 0x1,
       'C2IF': 0x4, 'VREN': 0x3, 'IOCA1': 0x1,
       'CCPR1L': 0x13, 'IOCA3': 0x3, 'PSA': 0x3,
       'IOCA5': 0x5, 'CCPR1H': 0x14, 'T0IE': 0x5,
       'ADCS1': 0x5, 'VRCON': 0x99, 'NOT_PD': 0x3,
       'DC': 0x1, 'WPUA4': 0x4, 'SYNC0': 0x2,
       'CMDLY1': 0x1, 'CMDLY0': 0x0, 'CMDLY3': 0x3,
       'CMDLY2': 0x2, 'C2SYNC': 0x0, 'CMDLY4': 0x4,
       'C1IF': 0x3, 'ANSEL1': 0x93, 'ANSEL0': 0x91,
       'ADCS0': 0x4, 'TUN3': 0x3, 'TUN2': 0x2,
       'PWMCLK': 0x112, 'TUN0': 0x0, 'MC2OUT': 0x6,
       'C2CH1': 0x1, 'TUN4': 0x4, 'TMR1GE': 0x6,
       'POL': 0x7, 'SWDTEN': 0x0, 'WPUA': 0x95,
       'NOT_RAPU': 0x7, 'RP1': 0x6, 'RP0': 0x5,
       'T1CKPS1': 0x5, 'INTF': 0x1, 'EEIE': 0x7,
       'RAIE': 0x3, 'RAIF': 0x0, 'EEIF': 0x7,
       'IRP': 0x7, 'IOC5': 0x5, 'CCP1IE': 0x5,
       'C1IE': 0x3, 'IOC4': 0x4, 'CM1CON0': 0x119,
       'C2EN': 0x6, 'IOCA4': 0x4, 'TMR2ON': 0x2,
       'TMR1IF': 0x0, 'TMR1IE': 0x0, 'WDTCON': 0x18,
       'ANS8': 0x0, 'ANS9': 0x1, 'PER2': 0x2,
       'ANS0': 0x0, 'ANS1': 0x1, 'ANS2': 0x2,
       'ANS3': 0x3, 'ANS4': 0x4, 'ANS5': 0x5,
       'ANS6': 0x6, 'ANS7': 0x7, 'BLANK2': 0x5,
       'INDF': 0x0, 'OSFIF': 0x2, 'OSFIE': 0x2,
       'C1R': 0x2, 'TUN1': 0x1, }

pages=((0x5, 0x7FF), )

banks=((0x20, 0x3F), (0x40, 0x6F), (0x70, 0x7F), )

shareb=(
        ((0x70, 0x7F), (0xF0, 0xFF), (0x170, 0x17F), (0x1F0, 0x1FF), ),
        ((0x20, 0x3F), (0xA0, 0xBF), ),
)
maxram = 0x1ff