############################################################################
# $Id$
#
# Description: PIC 12F635 definition. Pyastra project.
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

hdikt={'NOT_T1SYNC': 0x2, 'C1INV': 0x4, 'WR': 0x1,
       'T0SE': 0x4, 'NOT_POR': 0x1, 'OSCCON': 0x8f,
       'RD': 0x0, 'WPDA': 0x97, 'IOCA': 0x96,
       'PIE1': 0x8c, 'TMR1ON': 0x0, 'WRERR': 0x3,
       'PLVDIF': 0x6, 'PLVDIE': 0x6, 'PORTA': 0x5,
       'NOT_RAPUD': 0x7, 'GIE': 0x7, 'GO': 0x7,
       'INTEDG': 0x6, 'OSCTUNE': 0x90, 'C2INV': 0x5,
       'T0CS': 0x5, 'T1GEQ': 0x6, 'EECON1': 0x9c,
       'EECON2': 0x9d, 'KLQDAT0': 0x111, 'WDTPS3': 0x4,
       'WDTPS0': 0x1, 'KLQDAT3': 0x114, 'KLQREG1': 0x1,
       'KLQREG0': 0x0, 'STATUS': 0x3, 'PEIE': 0x6,
       'PLVDL0': 0x0, 'PLVDL1': 0x1, 'WREN': 0x2,
       'ULPWUE': 0x5, 'INTCON': 0xb, 'VREN': 0x7,
       'PCL': 0x2, 'PS2': 0x2, 'PS0': 0x0,
       'PS1': 0x1, 'WDTPS2': 0x3, 'KLQDAT1': 0x112,
       'TMR1CS': 0x1, 'KLQDAT2': 0x113, 'VR3': 0x3,
       'WDTPS1': 0x2, 'SCS': 0x0, 'C': 0x0,
       'NOT_WUR': 0x3, 'TRISA': 0x85, 'OPTION_REG': 0x81,
       'PIR1': 0xc, 'KLQIE': 0x5, 'KLQIF': 0x5,
       'INTE': 0x4, 'C2IE': 0x4, 'C2IF': 0x4,
       'PSA': 0x3, 'ENC_DEC': 0x6, 'IOSCF2': 0x6,
       'IOSCF0': 0x4, 'IOSCF1': 0x5, 'HTS': 0x2,
       'SBODEN': 0x4, 'CM2': 0x2, 'CM1': 0x1,
       'CM0': 0x0, 'T1OSCEN': 0x3, 'PCLATH': 0xa,
       'PCON': 0x8e, 'T1GINV': 0x7, 'FSR': 0x4,
       'IOCA4': 0x4, 'VRR': 0x5, 'NOT_BOD': 0x0,
       'PLVDCON': 0x94, 'OSTS': 0x3, 'C1OUT': 0x6,
       'PLVDL2': 0x2, 'LTS': 0x1, 'VR2': 0x2,
       'VR1': 0x1, 'VR0': 0x0, 'IRVST': 0x6,
       'Z': 0x2, 'C2OUT': 0x7, 'PLVDEN': 0x5,
       'T1CKPS0': 0x4, 'NOT_TO': 0x4, 'TMR0': 0x1,
       'IOCA1': 0x1, 'IOCA0': 0x0, 'IOCA3': 0x3,
       'IOCA2': 0x2, 'IOCA5': 0x5, 'T0IF': 0x2,
       'T0IE': 0x5, 'VRCON': 0x99, 'NOT_PD': 0x3,
       'DC': 0x1, 'CIS': 0x3, 'C1IF': 0x3,
       'C1IE': 0x3, 'TUN3': 0x3, 'TUN2': 0x2,
       'TUN1': 0x1, 'TUN0': 0x0, 'KLQCON': 0x110,
       'TUN4': 0x4, 'SWDTEN': 0x0, 'WPUA': 0x95,
       'RP1': 0x6, 'RP0': 0x5, 'T1CKPS1': 0x5,
       'INTF': 0x1, 'EEIE': 0x7, 'RAIE': 0x3,
       'RAIF': 0x0, 'EEIF': 0x7, 'IRP': 0x7,
       'T1GSS': 0x1, 'TMR1IF': 0x0, 'TMR1IE': 0x0,
       'WDTCON': 0x18, 'INDF': 0x0, 'OSFIF': 0x2,
       'OSFIE': 0x2, }

pages=((0x5, 0x3FF), )

banks=((0x40, 0x6F), (0x70, 0x7F), )

shareb=(
        ((0x70, 0x7F), (0xF0, 0xFF), (0x170, 0x17F), (0x1F0, 0x1FF), ),
)
maxram = 0x3ff