############################################################################
# $Id$
#
# Description: PIC 16F685 definition. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################

"""
Pic 16F685 definition. U{Pyastra project <http://pyastra.sourceforge.net>}.

@author: U{Alex Ziranov <mailto:estyler_at_users_dot_sourceforge_dot_net>}
@copyright: (C) 2004-2006 Alex Ziranov.  All rights reserved.
@license: This program is free software; you can redistribute it and/or
          modify it under the terms of the GNU General Public License as
          published by the Free Software Foundation; either version 2 of
          the License, or (at your option) any later version.
          
          This program is distributed in the hope that it will be useful,
          but WITHOUT ANY WARRANTY; without even the implied warranty of
          MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
          GNU Library General Public License for more details.
          
          You should have received a copy of the GNU General Public
          License along with this program; if not, write to the Free
          Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
          MA 02111-1307, USA.
@contact: U{http://pyastra.sourceforge.net}
"""

hdikt={'NOT_T1SYNC': 0x2, 'WPUB5': 0x5, 'TRISB4': 0x4,
       'WPUB7': 0x7, 'WPUB6': 0x6, 'T1IF': 0x0,
       'ECCPASE': 0x7, 'T1IE': 0x0, 'PWM1CON': 0x1c,
       'NOT_RABPU': 0x7, 'SRCON': 0x19e, 'C2VREN': 0x6,
       'WR': 0x1, 'T2CON': 0x12, 'TRISA3': 0x3,
       'TRISA2': 0x2, 'TRISA1': 0x1, 'TRISA0': 0x0,
       'TRISA5': 0x5, 'TRISA4': 0x4, 'C2R': 0x2,
       'VCFG': 0x6, 'CCPIE': 0x2, 'OSCCON': 0x8f,
       'RD': 0x0, 'RABIE': 0x3, 'RABIF': 0x0,
       'IOCA': 0x96, 'VP6EN': 0x4, 'IOCB': 0x116,
       'PIE2': 0x8d, 'PIE1': 0x8c, 'IRCF1': 0x5,
       'TMR1ON': 0x0, 'C1SEN': 0x5, 'IOC1': 0x1,
       'IOC0': 0x0, 'IOC3': 0x3, 'IOC2': 0x2,
       'PORTB': 0x6, 'PORTC': 0x7, 'IOCB6': 0x6,
       'PORTA': 0x5, 'CM2CON1': 0x11b, 'CM2CON0': 0x11a,
       'GIE': 0x7, 'PR2': 0x92, 'GO': 0x1,
       'INTEDG': 0x6, 'TOUTPS1': 0x4, 'OSCTUNE': 0x90,
       'WRERR': 0x3, 'T0CS': 0x5, 'EECON1': 0x18c,
       'EECON2': 0x18d, 'PSTRCON': 0x19d, 'GO_DONE': 0x1,
       'WDTPS2': 0x3, 'WDTPS3': 0x4, 'WDTPS0': 0x1,
       'WDTPS1': 0x2, 'MC1OUT': 0x7, 'PSSBD0': 0x0,
       'PSSBD1': 0x1, 'C2OE': 0x5, 'ECCPAS0': 0x4,
       'ECCPAS1': 0x5, 'ECCPAS2': 0x6, 'STATUS': 0x3,
       'PEIE': 0x6, 'WREN': 0x2, 'T2CKPS0': 0x0,
       'T2CKPS1': 0x1, 'ULPWUE': 0x5, 'INTCON': 0xb,
       'NOT_DONE': 0x1, 'PCL': 0x2, 'PS2': 0x2,
       'ADON': 0x0, 'PS0': 0x0, 'PS1': 0x1,
       'PSSAC0': 0x2, 'PSSAC1': 0x3, 'CCP1M2': 0x2,
       'CCP1M3': 0x3, 'CCP1M0': 0x0, 'CCP1M1': 0x1,
       'TMR1CS': 0x1, 'ANS3': 0x3, 'C1CH0': 0x0,
       'C1CH1': 0x1, 'VR3': 0x3, 'CCP1IF': 0x2,
       'C2ON': 0x7, 'DC1B1': 0x5, 'DC1B0': 0x4,
       'WPUA2': 0x2, 'SCS': 0x0, 'C1VREN': 0x7,
       'C': 0x0, 'CHS0': 0x2, 'CHS1': 0x3,
       'CHS2': 0x4, 'CHS3': 0x5, 'TRISC': 0x87,
       'TRISB': 0x86, 'TRISA': 0x85, 'ADCON1': 0x9f,
       'WPUA5': 0x5, 'OPTION_REG': 0x81, 'T0SE': 0x4,
       'T1GSS': 0x1, 'PIR2': 0xd, 'PIR1': 0xc,
       'IRCF0': 0x4, 'ANS1': 0x1, 'WPUA4': 0x4,
       'INTE': 0x4, 'T2IE': 0x1, 'C2IE': 0x6,
       'C2IF': 0x6, 'T2IF': 0x1, 'VR1': 0x1,
       'ADFM': 0x7, 'HTS': 0x2, 'SBODEN': 0x4,
       'STRC': 0x2, 'STRB': 0x1, 'STRA': 0x0,
       'C1POL': 0x4, 'STRD': 0x3, 'T1OSCEN': 0x3,
       'PCLATH': 0xa, 'PRSEN': 0x7, 'C2REN': 0x4,
       'IOCA0': 0x0, 'PCON': 0x8e, 'OSTS': 0x3,
       'TOUTPS2': 0x5, 'TOUTPS3': 0x6, 'TOUTPS0': 0x3,
       'T1GINV': 0x7, 'FSR': 0x4, 'IOCA2': 0x2,
       'ADCS2': 0x6, 'WPUA0': 0x0, 'T0IF': 0x2,
       'VRR': 0x5, 'CCP1CON': 0x17, 'EEDATH': 0x10e,
       'WPU': 0x95, 'EEDATA': 0x10c, 'IRCF2': 0x6,
       'C1OUT': 0x6, 'SR0': 0x6, 'SR1': 0x7,
       'C1OE': 0x5, 'TMR1IE': 0x0, 'WPUA1': 0x1,
       'P1M1': 0x7, 'C1ON': 0x7, 'LTS': 0x1,
       'VR2': 0x2, 'ANSEL': 0x11e, 'VR0': 0x0,
       'EEADRH': 0x10f, 'NOT_BOD': 0x0, 'TMR2IE': 0x1,
       'TMR2IF': 0x1, 'C2POL': 0x4, 'TRISB6': 0x6,
       'TRISB7': 0x7, 'ADIF': 0x6, 'TRISB5': 0x5,
       'Z': 0x2, 'C2OUT': 0x6, 'ECCPAS': 0x1d,
       'IOCB4': 0x4, 'C2CH0': 0x0, 'IOC': 0x96,
       'T1CKPS0': 0x4, 'ANS0': 0x0, 'NOT_TO': 0x4,
       'TMR2': 0x11, 'TMR0': 0x1, 'ANS2': 0x2,
       'IOCB5': 0x5, 'IOCA1': 0x1, 'CCPR1L': 0x15,
       'IOCA3': 0x3, 'PSA': 0x3, 'IOCA5': 0x5,
       'CCPR1H': 0x16, 'T0IE': 0x5, 'ADCS1': 0x5,
       'VRCON': 0x118, 'WPUB4': 0x4, 'NOT_PD': 0x3,
       'DC': 0x1, 'ANS5': 0x5, 'TRISC1': 0x1,
       'TRISC0': 0x0, 'TRISC3': 0x3, 'TRISC2': 0x2,
       'TRISC5': 0x5, 'TRISC4': 0x4, 'TRISC7': 0x7,
       'TRISC6': 0x6, 'C2SYNC': 0x0, 'ANS7': 0x7,
       'EEADR': 0x10d, 'C1IF': 0x5, 'C1IE': 0x5,
       'ADCS0': 0x4, 'TUN3': 0x3, 'TUN2': 0x2,
       'TUN1': 0x1, 'TUN0': 0x0, 'MC2OUT': 0x6,
       'C2CH1': 0x1, 'TUN4': 0x4, 'TMR1GE': 0x6,
       'SWDTEN': 0x0, 'WPUB': 0x115, 'IOCB7': 0x7,
       'WPUA': 0x95, 'NOT_POR': 0x1, 'RP1': 0x6,
       'RP0': 0x5, 'T1CKPS1': 0x5, 'INTF': 0x1,
       'EEIE': 0x4, 'EEPGD': 0x7, 'EEIF': 0x4,
       'IRP': 0x7, 'IOC5': 0x5, 'ANS4': 0x4,
       'IOC4': 0x4, 'PULSS': 0x3, 'CM1CON0': 0x119,
       'PULSR': 0x2, 'IOCA4': 0x4, 'ANSELH': 0x11f,
       'TMR2ON': 0x2, 'TMR1IF': 0x0, 'P1M0': 0x6,
       'WDTCON': 0x97, 'STRSYNC': 0x4, 'PDC1': 0x1,
       'PDC0': 0x0, 'PDC3': 0x3, 'PDC2': 0x2,
       'PDC5': 0x5, 'PDC4': 0x4, 'ANS6': 0x6,
       'PDC6': 0x6, 'INDF': 0x0, 'OSFIF': 0x7,
       'OSFIE': 0x7, 'C1R': 0x2, 'ADIE': 0x6,
       }

pages=((0x5, 0x7FF), (0x800, 0xFFF), )

banks=((0x20, 0x6F), (0x70, 0x7F), (0xA0, 0xEF), (0x120, 0x16F), )

shareb=(
        ((0x70, 0x7F), (0xF0, 0xFF), (0x170, 0x17F), (0x1F0, 0x1FF), ),
)

vectors=(0x0, 0x4)
maxram = 0x1ff