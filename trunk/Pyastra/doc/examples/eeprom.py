############################################################################
# $Id$
#
# Description: Internal EEPROM driver. Pyastra project.
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

def EEPROM_write(EEPROM_write_addr, EEPROM_write_data):
    EEDATA = EEPROM_write_data
    EEADR = EEPROM_write_addr
    EECON1[EEPGD] = 0
    EECON1[WREN] = 1
    INTCON[GIE] = 0
    #
    # FIXME: this asm-code can't be converted to python while
    # because of missing optimizations in Pyastra that generates
    # extra code that prevents enabling write mode
    #
    asm("""
        bsf     STATUS,      RP0
        bsf     STATUS,      RP1
        movlw   0x55
        movwf   EECON2
        movlw   0xaa
        movwf   EECON2
        bsf     EECON1, WR
    """, 5)
    INTCON[GIE] = 1
    EECON1[WR] = 0

def EEPROM_read(EEPROM_read_addr):
    EEADR = EEPROM_read_addr
    EECON1[EEPGD] = 0
    EECON1[RD] = 1
    return EEDATA

