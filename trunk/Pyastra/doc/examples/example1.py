############################################################################
# $Id$
#
# Description: This example gets data from ADC and writes it to serial
#              port. Pyastra project.
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

# Import ADC and serial port modules 
from pic_adc import *
from serial import *

#
# Inits ADC module with following parameters:
# * internal oscillator F_osc/8
# * output data would be right justified (6 Most Significant
#   bits of ADRESH are read as '0'
# * Use pin 0 of PIC's port A as input analogue channel
# * A/D Port Configuration Control bits are set so that only pin 0
#   of port A is used as analogue input
#
PIC_ADC_init(CLOCK_OSC8, JUSTIFY_RIGHT, 0, fbin('0000 1110'))

# Inits module serial
serial_init()

# Does an infinite loop
while 1:
    # Reads data from ADC
    PIC_ADC_get()
    
    # Writes data given by ADC to serial port
    serial_write(PIC_ADC_resl)
    serial_write(PIC_ADC_resh)
    
    # Wait a bit between reading next value
    for i in xrange(0,255):
        pass
