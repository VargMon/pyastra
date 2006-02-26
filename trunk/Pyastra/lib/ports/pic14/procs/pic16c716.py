############################################################################
# $Id$
#
# Description: PIC 16C716 definition. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################

"""
Pic 16C716 definition. U{Pyastra project <http://pyastra.sourceforge.net>}.

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

hdikt={'NOT_T1SYNC': 0x2, 'T2CON': 0x12, 'T1CON': 0x10,
       'T0SE': 0x4, 'NOT_POR': 0x1, 'PCFG2': 0x2,
       'PCFG1': 0x1, 'PCFG0': 0x0, 'PIE1': 0x8c,
       'TMR1ON': 0x0, 'NOT_RBPU': 0x7, 'PORTB': 0x6,
       'PORTA': 0x5, 'GIE': 0x7, 'PR2': 0x92,
       'GO': 0x2, 'INTEDG': 0x6, 'DCCP': 0x2,
       'T0CS': 0x5, 'GO_DONE': 0x2, 'DT1CK': 0x0,
       'STATUS': 0x3, 'PEIE': 0x6, 'T1SYNC': 0x2,
       'T2CKPS0': 0x0, 'T2CKPS1': 0x1, 'INTCON': 0xb,
       'PCL': 0x2, 'PS2': 0x2, 'ADON': 0x0,
       'PS0': 0x0, 'TMR1H': 0xf, 'TMR1L': 0xe,
       'CCP1M2': 0x2, 'CCP1M3': 0x3, 'CCP1M0': 0x0,
       'CCP1M1': 0x1, 'TT1CK': 0x0, 'TMR1CS': 0x1,
       'T1CKPS0': 0x4, 'DATACCP': 0x7, 'DC1B1': 0x5,
       'DC1B0': 0x4, 'C': 0x0, 'CHS0': 0x3,
       'CHS1': 0x4, 'CHS2': 0x5, 'TRISB': 0x86,
       'TRISA': 0x85, 'ADCON1': 0x9f, 'ADCON0': 0x1f,
       'OPTION_REG': 0x81, 'PIR1': 0xc, 'INTE': 0x4,
       'PSA': 0x3, 'TRISCCP': 0x87, 'RBIF': 0x0,
       'RBIE': 0x3, 'T1OSCEN': 0x3, 'PCLATH': 0xa,
       'PCON': 0x8e, 'TOUTPS2': 0x5, 'TOUTPS3': 0x6,
       'TOUTPS0': 0x3, 'TOUTPS1': 0x4, 'FSR': 0x4,
       'T0IF': 0x2, 'CCP1CON': 0x17, 'ADCS0': 0x6,
       'ADRES': 0x1e, 'NOT_BOD': 0x0, 'TMR2IE': 0x1,
       'TMR2IF': 0x1, 'NOT_BO': 0x0, 'ADIE': 0x6,
       'ADIF': 0x6, 'Z': 0x2, 'NOT_DONE': 0x2,
       'NOT_TO': 0x4, 'TMR2': 0x11, 'TMR0': 0x1,
       'CCPR1L': 0x15, 'CCPR1H': 0x16, 'T0IE': 0x5,
       'ADCS1': 0x7, 'NOT_PD': 0x3, 'DC': 0x1,
       'PS1': 0x1, 'RP1': 0x6, 'RP0': 0x5,
       'T1CKPS1': 0x5, 'INTF': 0x1, 'IRP': 0x7,
       'CCP1IE': 0x2, 'CCP1IF': 0x2, 'TMR2ON': 0x2,
       'TMR1IF': 0x0, 'TMR1IE': 0x0, 'TCCP': 0x2,
       'INDF': 0x0, }

pages=((0x5, 0x7FF), )

banks=((0x20, 0x7F), (0xA0, 0xBF), )

shareb=(
)

vectors=(0x0, 0x4)
maxram = 0xbf