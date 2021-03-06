############################################################################
# $Id$
#
# Description: PIC 16F916I definition. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################

"""
Pic 16F916I definition. U{Pyastra project <http://pyastra.sourceforge.net>}.

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

hdikt={'CKE': 0x6, 'ADIF': 0x6, 'C1INV': 0x4,
       'S14C0': 0x6, 'S14C1': 0x6, 'S14C2': 0x6,
       'S14C3': 0x6, 'IOCB': 0x96, 'S10C0': 0x2,
       'S10C1': 0x2, 'S10C2': 0x2, 'S10C3': 0x2,
       'IOC5': 0x5, 'IOC4': 0x4, 'IOC7': 0x7,
       'IOC6': 0x6, 'P': 0x4, 'GIE': 0x7,
       'EECON1': 0x18c, 'EECON2': 0x18d, 'LVDIE': 0x2,
       'LVDCON': 0x109, 'WR': 0x1, 'PEIE': 0x6,
       'SREN': 0x5, 'WREN': 0x2, 'T2CKPS0': 0x0,
       'T2CKPS1': 0x1, 'NOT_TO': 0x4, 'PCL': 0x2,
       'LCDCON': 0x107, 'S9C1': 0x1, 'S9C0': 0x1,
       'S9C3': 0x1, 'S9C2': 0x1, 'ADON': 0x0,
       'ADCON0': 0x1f, 'OPTION_REG': 0x81, 'CMCON0': 0x9c,
       'SWDTEN': 0x0, 'I2C_READ': 0x2, 'ADFM': 0x7,
       'CM2': 0x2, 'CM1': 0x1, 'CM0': 0x0,
       'PCLATH': 0xa, 'SMP': 0x7, 'GO_DONE': 0x1,
       'SE5': 0x5, 'I2C_STOP': 0x4, 'CCP1CON': 0x17,
       'DATA_ADDRESS': 0x5, 'IRCF0': 0x4, 'LTS': 0x1,
       'EEADRL': 0x10d, 'SEG9COM1': 0x1, 'SEG9COM0': 0x1,
       'SEG9COM3': 0x1, 'S3C2': 0x3, 'S4C0': 0x4,
       'S4C1': 0x4, 'S4C2': 0x4, 'S4C3': 0x4,
       'SSPCON': 0x14, 'TMR2': 0x11, 'TMR0': 0x1,
       'READ_WRITE': 0x2, 'SEGEN12': 0x4, 'SEGEN13': 0x5,
       'SEGEN10': 0x2, 'SEGEN11': 0x3, 'IRVST': 0x5,
       'SEGEN14': 0x6, 'SEGEN15': 0x7, 'NOT_BOR': 0x0,
       'FERR': 0x2, 'C2SYNC': 0x0, 'LCDDATA3': 0x113,
       'LCDDATA1': 0x111, 'LCDDATA0': 0x110, 'LCDDATA7': 0x117,
       'LCDDATA6': 0x116, 'SSPEN': 0x5, 'LCDDATA4': 0x114,
       'TUN3': 0x3, 'TUN2': 0x2, 'LCDDATA9': 0x119,
       'TUN0': 0x0, 'TUN4': 0x4, 'TMR0IF': 0x2,
       'TMR0IE': 0x5, 'T1CKPS1': 0x5, 'T1CKPS0': 0x4,
       'LCDEN': 0x7, 'CCP1X': 0x5, 'CCP1Y': 0x4,
       'S11C1': 0x3, 'S11C0': 0x3, 'S11C3': 0x3,
       'WDTCON': 0x105, 'NOT_ADDRESS': 0x5, 'SEG5COM1': 0x5,
       'SEG5COM0': 0x5, 'SEG5COM3': 0x5, 'SEG5COM2': 0x5,
       'LCDSE1': 0x11d, 'LCDSE0': 0x11c, 'TX9D': 0x0,
       'TUN1': 0x1, 'RCIF': 0x5, 'RCIE': 0x5,
       'VLCDEN': 0x4, 'T0SE': 0x4, 'SPBRG': 0x99,
       'LP3': 0x3, 'LP2': 0x2, 'LP1': 0x1,
       'LP0': 0x0, 'RD': 0x0, 'PIE2': 0x8d,
       'PIE1': 0x8c, 'S12C2': 0x4, 'S12C3': 0x4,
       'S12C0': 0x4, 'S12C1': 0x4, 'PR2': 0x92,
       'OSCTUNE': 0x90, 'WRERR': 0x3, 'TXIF': 0x4,
       'TXIE': 0x4, 'WDTPS2': 0x3, 'WDTPS3': 0x4,
       'WDTPS0': 0x1, 'WDTPS1': 0x2, 'TXSTA': 0x98,
       'T1SYNC': 0x2, 'INTCON': 0xb, 'WFT': 0x7,
       'I2C_DATA': 0x5, 'SWDTE': 0x0, 'CS1': 0x3,
       'CS0': 0x2, 'LVDIF': 0x2, 'S5C1': 0x5,
       'S5C0': 0x5, 'S5C3': 0x5, 'S5C2': 0x5,
       'CHS0': 0x2, 'CHS1': 0x3, 'CHS2': 0x4,
       'ADCON1': 0x9f, 'LCDIF': 0x4, 'LCDIE': 0x4,
       'CMCON1': 0x97, 'PIR2': 0xd, 'PIR1': 0xc,
       'C2IE': 0x6, 'C2IF': 0x6, 'R_W': 0x2,
       'CREN': 0x4, 'RBIF': 0x0, 'RBIE': 0x3,
       'LMUX1': 0x1, 'LMUX0': 0x0, 'PCON': 0x8e,
       'TOUTPS2': 0x5, 'TOUTPS3': 0x6, 'TOUTPS0': 0x3,
       'TOUTPS1': 0x4, 'SSPOV': 0x6, 'EEDATL': 0x10c,
       'EEDATH': 0x10e, 'WPU': 0x95, 'C1OUT': 0x6,
       'SEG8COM0': 0x0, 'SEG8COM1': 0x0, 'SEG8COM2': 0x0,
       'S11C2': 0x3, 'SBOREN': 0x4, 'SE7': 0x7,
       'SE6': 0x6, 'ANSEL': 0x91, 'SE4': 0x4,
       'SE3': 0x3, 'SE2': 0x2, 'SE1': 0x1,
       'LCDDATA10': 0x11a, 'TMR2IE': 0x1, 'TMR2IF': 0x1,
       'SE8': 0x0, 'R': 0x2, 'C2OUT': 0x7,
       'NOT_WRITE': 0x2, 'SEG8COM3': 0x0, 'TXEN': 0x5,
       'S0C0': 0x0, 'S0C1': 0x0, 'S0C2': 0x0,
       'S0C3': 0x0, 'CCPR1L': 0x15, 'T0IF': 0x2,
       'T0IE': 0x5, 'DC': 0x1, 'C1IF': 0x5,
       'C1IE': 0x5, 'TMR1H': 0xf, 'SE0': 0x0,
       'INTE': 0x4, 'RP0': 0x5, 'INTF': 0x1,
       'CCP1IF': 0x2, 'CCP1IE': 0x2, 'SE9': 0x1,
       'OSTS': 0x3, 'NOT_POR': 0x1, 'S2C3': 0x2,
       'SEGEN8': 0x0, 'SEGEN9': 0x1, 'OSFIF': 0x7,
       'OSFIE': 0x7, 'SEGEN0': 0x0, 'SEGEN1': 0x1,
       'SEGEN2': 0x2, 'SEGEN3': 0x3, 'SEGEN4': 0x4,
       'SEGEN5': 0x5, 'SEGEN6': 0x6, 'SEGEN7': 0x7,
       'NOT_T1SYNC': 0x2, 'WA': 0x4, 'WPUB3': 0x3,
       'CKP': 0x4, 'SEG7COM3': 0x7, 'SEG7COM2': 0x7,
       'SEG7COM1': 0x7, 'SEG7COM0': 0x7, 'S8C1': 0x0,
       'TRMT': 0x1, 'SSPBUF': 0x13, 'SPEN': 0x7,
       'SEG15COM2': 0x7, 'SYNC': 0x4, 'AN4': 0x4,
       'AN0': 0x0, 'AN1': 0x1, 'AN2': 0x2,
       'AN3': 0x3, 'PS2': 0x2, 'PS0': 0x0,
       'PS1': 0x1, 'TMR1L': 0xe, 'CCP1M2': 0x2,
       'CCP1M3': 0x3, 'CCP1M0': 0x0, 'CCP1M1': 0x1,
       'TMR1CS': 0x1, 'S13C3': 0x5, 'S13C2': 0x5,
       'S13C1': 0x5, 'S13C0': 0x5, 'C': 0x0,
       'TRISC': 0x87, 'TRISB': 0x86, 'TRISA': 0x85,
       'S7C3': 0x7, 'S7C2': 0x7, 'S7C1': 0x7,
       'S7C0': 0x7, 'S': 0x3, 'TRISE': 0x89,
       'SEG1COM1': 0x1, 'SEG1COM0': 0x1, 'SEG1COM3': 0x1,
       'SEG1COM2': 0x1, 'S1C1': 0x1, 'S1C0': 0x1,
       'S1C3': 0x1, 'S1C2': 0x1, 'PSA': 0x3,
       'BRGH': 0x2, 'SEG2COM2': 0x2, 'SEG2COM3': 0x2,
       'SEG2COM0': 0x2, 'SEG2COM1': 0x2, 'T1OSCEN': 0x3,
       'FSR': 0x4, 'RX9D': 0x0, 'SEG6COM2': 0x6,
       'SEG6COM3': 0x6, 'SEG6COM0': 0x6, 'SEG6COM1': 0x6,
       'WERR': 0x5, 'VRR': 0x5, 'RCREG': 0x1a,
       'SE13': 0x5, 'SE12': 0x4, 'SE11': 0x3,
       'D_A': 0x5, 'SEG10COM0': 0x2, 'SEG10COM1': 0x2,
       'SEG10COM2': 0x2, 'SEG10COM3': 0x2, 'VR3': 0x3,
       'VR2': 0x2, 'VR1': 0x1, 'VR0': 0x0,
       'SEG14COM0': 0x6, 'SEG14COM1': 0x6, 'SEG14COM2': 0x6,
       'SEG14COM3': 0x6, 'ADIE': 0x6, 'LCDA': 0x5,
       'SEG13COM3': 0x5, 'SEG13COM2': 0x5, 'SEG13COM1': 0x5,
       'SEG13COM0': 0x5, 'SSPADD': 0x93, 'ADCS2': 0x6,
       'ADCS0': 0x4, 'ADCS1': 0x5, 'SEG0COM0': 0x0,
       'SEG0COM1': 0x0, 'SEG0COM2': 0x0, 'SEG0COM3': 0x0,
       'SEG3COM3': 0x3, 'SEG3COM2': 0x3, 'SEG3COM1': 0x3,
       'SEG3COM0': 0x3, 'SEG4COM0': 0x4, 'SEG4COM1': 0x4,
       'SEG4COM2': 0x4, 'SEG4COM3': 0x4, 'CCPR1H': 0x16,
       'S6C2': 0x6, 'S6C3': 0x6, 'S6C0': 0x6,
       'S6C1': 0x6, 'IRP': 0x7, 'IOCB4': 0x4,
       'IOCB5': 0x5, 'BIASMD': 0x6, 'IOCB7': 0x7,
       'I2C_START': 0x3, 'SEG11COM1': 0x3, 'SEG11COM0': 0x3,
       'SEG11COM3': 0x3, 'SEG11COM2': 0x3, 'SEG12COM2': 0x4,
       'SEG12COM3': 0x4, 'SEG12COM0': 0x4, 'SEG12COM1': 0x4,
       'WPUB1': 0x1, 'WPUB0': 0x0, 'BF': 0x0,
       'WPUB2': 0x2, 'WPUB5': 0x5, 'WPUB4': 0x4,
       'WPUB7': 0x7, 'WPUB6': 0x6, 'SEG15COM1': 0x7,
       'SEG15COM0': 0x7, 'SEG15COM3': 0x7, 'T2CON': 0x12,
       'T1CON': 0x10, 'OSCCON': 0x8f, 'RX9': 0x6,
       'IOC': 0x96, 'TMR1ON': 0x0, 'D': 0x5,
       'PORTE': 0x9, 'PORTB': 0x6, 'PORTC': 0x7,
       'IOCB6': 0x6, 'PORTA': 0x5, 'INTEDG': 0x6,
       'T1GINV': 0x7, 'C2INV': 0x5, 'T0CS': 0x5,
       'ADRESL': 0x9e, 'ADRESH': 0x1e, 'VCFG1': 0x6,
       'VCFG0': 0x5, 'RP1': 0x6, 'SSPIE': 0x3,
       'SSPIF': 0x3, 'VREN': 0x7, 'WCOL': 0x7,
       'ADDEN': 0x3, 'SLPEN': 0x6, 'NOT_RBPU': 0x7,
       'S15C1': 0x7, 'S15C0': 0x7, 'S15C3': 0x7,
       'S15C2': 0x7, 'SCS': 0x0, 'WPU5': 0x5,
       'IRCF2': 0x6, 'IRCF1': 0x5, 'LCDPS': 0x108,
       'S3C3': 0x3, 'T1GE': 0x6, 'S3C1': 0x3,
       'S3C0': 0x3, 'EERD': 0x0, 'OERR': 0x1,
       'HTS': 0x2, 'UA': 0x1, 'TXREG': 0x19,
       'SSPSTAT': 0x94, 'NOT_A': 0x5, 'NOT_W': 0x2,
       'TMR1IF': 0x0, 'S8C0': 0x0, 'TMR1IE': 0x0,
       'S8C2': 0x0, 'S8C3': 0x0, 'S2C2': 0x2,
       'NOT_BO': 0x0, 'S2C0': 0x2, 'S2C1': 0x2,
       'Z': 0x2, 'SE10': 0x2, 'NOT_DONE': 0x1,
       'SE15': 0x7, 'SE14': 0x6, 'VRCON': 0x9d,
       'NOT_PD': 0x3, 'EEWR': 0x1, 'CIS': 0x3,
       'LVDEN': 0x4, 'RCSTA': 0x18, 'LVDL2': 0x2,
       'LVDL1': 0x1, 'LVDL0': 0x0, 'EEADRH': 0x10f,
       'SEG9COM2': 0x1, 'WPUB': 0x95, 'STATUS': 0x3,
       'EEIE': 0x7, 'EEPGD': 0x7, 'EEIF': 0x7,
       'WPU2': 0x2, 'WPU3': 0x3, 'WPU0': 0x0,
       'WPU1': 0x1, 'WPU6': 0x6, 'WPU7': 0x7,
       'WPU4': 0x4, 'T1GSS': 0x1, 'CSRC': 0x7,
       'TX9': 0x6, 'TMR2ON': 0x2, 'SSPM0': 0x0,
       'SSPM1': 0x1, 'SSPM2': 0x2, 'SSPM3': 0x3,
       'INDF': 0x0, }

pages=((0x5, 0x7FF), (0x800, 0xEFF), )

banks=((0x20, 0x6F), (0x71, 0x7F), (0xA0, 0xEF), (0x120, 0x164), (0x190, 0x1EF), )

shareb=(
        ((0x71, 0x7F), (0xF1, 0xFF), (0x171, 0x17F), (0x1F1, 0x1FF), ),
)

vectors=(0x0, 0x4)
maxram = 0x1ff