############################################################################
# $Id$
#
# Description: This example writes 255 bytes from serial port to eeprom.
#              Pyastra project.
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
from eeprom import *
from serial import *

# Inits module serial
serial_init()

# Does an infinite loop
for addr in xrange(0,255):
    
    # Reads data from serial port
    data=serial_read()

    # Writes data to byte addr in EEPROM
    EEPROM_write(addr, data)
