############################################################################
# $Id$
#
# Description: PIC 16C54 definition. Pyastra project.
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

hdikt={'NOT_PD': 0x3, 'DC': 0x1, 'FSR': 0x4,
       'NOT_TO': 0x4, 'PCL': 0x2, 'PS2': 0x2,
       'PS0': 0x0, 'PS1': 0x1, 'T0SE': 0x4,
       'PORTC': 0x7, 'STATUS': 0x3, 'C': 0x0,
       'PORTB': 0x6, 'T0CS': 0x5, 'PORTA': 0x5,
       'Z': 0x2, 'PA0': 0x5, 'PA1': 0x6,
       'PA2': 0x7, 'PSA': 0x3, 'INDF': 0x0,
       'TMR0': 0x1, }

pages=((0x0, 0x1FF), )

banks=((0x7, 0x1F), )

shareb=(
)
maxram = 0x1ff