############################################################################
# $Id$
#
# Description: PIC 12F683I definition. Pyastra project.
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
       'GPIF': 0x0, 'GPIE': 0x3, 'WR': 0x1,
       'T2CON': 0x12, 'GPIO': 0x5, 'T0SE': 0x4,
       'NOT_POR': 0x1, 'OSCCON': 0x8f, 'RD': 0x0,
       'IOCA': 0x96, 'IOC': 0x96, 'PIE1': 0x8c,
       'TMR1ON': 0x0, 'IOC1': 0x1, 'IOC0': 0x0,
       'IOC3': 0x3, 'IOC2': 0x2, 'IOC5': 0x5,
       'IOC4': 0x4, 'GIE': 0x7, 'PR2': 0x92,
       'GO': 0x1, 'INTEDG': 0x6, 'TOUTPS1': 0x4,
       'TRISIO': 0x85, 'OSCTUNE': 0x90, 'WRERR': 0x3,
       'T0CS': 0x5, 'EECON1': 0x9c, 'EECON2': 0x9d,
       'GO_DONE': 0x1, 'WDTPS2': 0x3, 'WDTPS3': 0x4,
       'WDTPS0': 0x1, 'WDTPS1': 0x2, 'CINV': 0x4,
       'STATUS': 0x3, 'PEIE': 0x6, 'COUT': 0x6,
       'WREN': 0x2, 'CMIF': 0x3, 'T2CKPS0': 0x0,
       'T2CKPS1': 0x1, 'ULPWUE': 0x5, 'INTCON': 0xb,
       'NOT_DONE': 0x1, 'PCL': 0x2, 'PS2': 0x2,
       'ADON': 0x0, 'PS0': 0x0, 'PS1': 0x1,
       'CCP1M2': 0x2, 'CCP1M3': 0x3, 'CCP1M0': 0x0,
       'CCP1M1': 0x1, 'TMR1CS': 0x1, 'VR3': 0x3,
       'IRP': 0x7, 'DC1B1': 0x5, 'DC1B0': 0x4,
       'SCS': 0x0, 'C': 0x0, 'CMSYNC': 0x0,
       'CHS0': 0x2, 'CHS1': 0x3, 'CHS2': 0x4,
       'VCFG': 0x6, 'OPTION_REG': 0x81, 'IRCF2': 0x6,
       'PIR1': 0xc, 'IRCF0': 0x4, 'T1GE': 0x6,
       'INTE': 0x4, 'T2IE': 0x1, 'T2IF': 0x1,
       'VR1': 0x1, 'ADFM': 0x7, 'HTS': 0x2,
       'SBODEN': 0x4, 'CM2': 0x2, 'CM1': 0x1,
       'CM0': 0x0, 'T1OSCEN': 0x3, 'PCLATH': 0xa,
       'IOCA0': 0x0, 'PCON': 0x8e, 'TOUTPS2': 0x5,
       'TOUTPS3': 0x6, 'TOUTPS0': 0x3, 'T1GINV': 0x7,
       'FSR': 0x4, 'IOCA2': 0x2, 'ADCS2': 0x6,
       'T0IF': 0x2, 'VRR': 0x5, 'CCP1CON': 0x15,
       'NOT_BOD': 0x0, 'WPU': 0x95, 'OSTS': 0x3,
       'IRCF1': 0x5, 'LTS': 0x1, 'VR2': 0x2,
       'ANSEL': 0x9f, 'VR0': 0x0, 'TMR2IE': 0x1,
       'TMR2IF': 0x1, 'ADIE': 0x6, 'ADIF': 0x6,
       'Z': 0x2, 'T1CKPS0': 0x4, 'NOT_TO': 0x4,
       'TMR2': 0x11, 'TMR0': 0x1, 'IOCA3': 0x3,
       'VREN': 0x7, 'IOCA1': 0x1, 'CCPR1L': 0x13,
       'NOT_GPPU': 0x7, 'PSA': 0x3, 'IOCA5': 0x5,
       'CCPR1H': 0x14, 'T0IE': 0x5, 'ADCS1': 0x5,
       'VRCON': 0x99, 'NOT_PD': 0x3, 'DC': 0x1,
       'CIS': 0x3, 'ADCS0': 0x4, 'TUN3': 0x3,
       'TUN2': 0x2, 'TUN1': 0x1, 'TUN0': 0x0,
       'TUN4': 0x4, 'SWDTEN': 0x0, 'WPUA': 0x95,
       'RP1': 0x6, 'RP0': 0x5, 'T1CKPS1': 0x5,
       'INTF': 0x1, 'EEIE': 0x7, 'EEIF': 0x7,
       'CCP1IF': 0x5, 'CCP1IE': 0x5, 'CMIE': 0x3,
       'T1GSS': 0x1, 'IOCA4': 0x4, 'TMR2ON': 0x2,
       'TMR1IF': 0x0, 'TMR1IE': 0x0, 'WDTCON': 0x18,
       'ANS0': 0x0, 'ANS1': 0x1, 'ANS2': 0x2,
       'ANS3': 0x3, 'INDF': 0x0, 'OSFIF': 0x2,
       'OSFIE': 0x2, }

pages=((0x5, 0x6FF), )

banks=((0x20, 0x64), (0x71, 0x7F), (0xA0, 0xBF), )

shareb=(
        ((0x71, 0x7F), (0xF1, 0xFF), ),
)

vectors=(0x0, 0x4)
maxram = 0xff