############################################################################
# $Id$
#
# Description: PIC 16C781 definition. Pyastra project.
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

hdikt={'NOT_T1SYNC': 0x2, 'PMCON1': 0x18c, 'CMPEN': 0x6,
       'CALCON': 0x110, 'C2R': 0x2, 'T1CON': 0x10,
       'T0SE': 0x4, 'OSCF': 0x3, 'DAON': 0x7,
       'RD': 0x0, 'IOCB': 0x96, 'SMCON': 0x7,
       'SMCOM': 0x2, 'PIE1': 0x8c, 'TMR1ON': 0x0,
       'PORTB': 0x6, 'GBWP': 0x0, 'PORTA': 0x5,
       'CM2CON1': 0x11b, 'CM2CON0': 0x11a, 'GIE': 0x7,
       'GO': 0x2, 'INTEDG': 0x6, 'PSMCCON1': 0x112,
       'PSMCCON0': 0x111, 'NOT_PSM': 0x1, 'DC0': 0x0,
       'DC1': 0x1, 'BGST': 0x5, 'T0CS': 0x5,
       'VCFG1': 0x5, 'GO_DONE': 0x2, 'C2ON': 0x7,
       'MINDC0': 0x4, 'LVDCON': 0x9c, 'C2OE': 0x5,
       'STATUS': 0x3, 'PEIE': 0x6, 'SCEN': 0x3,
       'VCFG0': 0x4, 'NOT_TO': 0x4, 'PCL': 0x2,
       'PS2': 0x2, 'ADON': 0x0, 'PS0': 0x0,
       'TMR1H': 0xf, 'TMR1L': 0xe, 'VREFEN': 0x3,
       'TMR1CS': 0x1, 'CALREF': 0x5, 'C1CH0': 0x0,
       'C1CH1': 0x1, 'C2SP': 0x3, 'NOT_RBPU': 0x7,
       'DAOE': 0x6, 'LVDIE': 0x7, 'LVDIF': 0x7,
       'S1BPOL': 0x5, 'C': 0x0, 'CHS0': 0x3,
       'CHS1': 0x4, 'CHS2': 0x5, 'CHS3': 0x1,
       'TRISB': 0x86, 'TRISA': 0x85, 'ADCON1': 0x9f,
       'ADCON0': 0x1f, 'OPTION_REG': 0x81, 'PIR1': 0xc,
       'INTE': 0x4, 'C1SP': 0x3, 'PSM': 0x1,
       'C2IE': 0x5, 'C2IF': 0x5, 'PSA': 0x3,
       'REFCON': 0x9b, 'C1POL': 0x4, 'RBIF': 0x0,
       'RBIE': 0x3, 'T1OSCEN': 0x3, 'PCLATH': 0xa,
       'MC1OUT': 0x7, 'PCON': 0x8e, 'DARS1': 0x1,
       'DARS0': 0x0, 'FSR': 0x4, 'WDTON': 0x4,
       'PMDATH': 0x10e, 'PMDATL': 0x10c, 'ADCS0': 0x6,
       'ADRES': 0x1e, 'C1OUT': 0x6, 'SMCCL0': 0x6,
       'SMCCL1': 0x7, 'C1OE': 0x5, 'INTF': 0x1,
       'C1ON': 0x7, 'ANSEL': 0x9d, 'DACON0': 0x11f,
       'NOT_PD': 0x3, 'C2POL': 0x4, 'NOT_BO': 0x0,
       'ADIE': 0x6, 'ADIF': 0x6, 'Z': 0x2,
       'C2OUT': 0x6, 'NOT_DONE': 0x2, 'INTCON': 0xb,
       'TMR0': 0x1, 'T0IF': 0x2, 'T0IE': 0x5,
       'ADCS1': 0x7, 'OPACON': 0x11c, 'DC': 0x1,
       'VREFOE': 0x2, 'NOT_BOR': 0x0, 'LVDEN': 0x4,
       'CAL': 0x7, 'OPAON': 0x7, 'C2SYNC': 0x0,
       'C1IF': 0x4, 'C1IE': 0x4, 'PS1': 0x1,
       'LV1': 0x1, 'LV0': 0x0, 'LV3': 0x3,
       'DAC': 0x11e, 'MC2OUT': 0x6, 'C2CH1': 0x1,
       'C2CH0': 0x0, 'TMR1GE': 0x6, 'WPUB': 0x95,
       'RP1': 0x6, 'RP0': 0x5, 'T1CKPS1': 0x5,
       'T1CKPS0': 0x4, 'IRP': 0x7, 'SMCCS': 0x0,
       'S1APOL': 0x6, 'CM1CON0': 0x119, 'TMR1IF': 0x0,
       'TMR1IE': 0x0, 'MINDC1': 0x5, 'PMADRL': 0x10d,
       'LV2': 0x2, 'PMADRH': 0x10f, 'MAXDC1': 0x3,
       'MAXDC0': 0x2, 'INDF': 0x0, 'NOT_POR': 0x1,
       'C1R': 0x2, 'PWM': 0x1, 'CALERR': 0x6,
       }

pages=((0x5, 0x3FF), )

banks=((0x20, 0x6F), (0x70, 0x7F), (0xA0, 0xBF), )

shareb=(
        ((0x70, 0x7F), (0xF0, 0xFF), (0x170, 0x17F), (0x1F0, 0x1FF), ),
)
