############################################################################
# $Id$
#
# Description: Serial driver using internal USART. Pyastra project.
# Author: Stanislav Bobykin <stcor _at_ mail _dot_ ru>
#    
# Copyright (c) 2004 Stanislav Bobykin.  All rights reserved.
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

def serial_init(): #Constructor
    TRISC[7]=1
    TRISC[6]=1
    #set speed
    TXSTA[2]=1 #set high speed mode: SPBRG, 2 
    SPBRG=16 #set speed 57.6 Kbit/sec
    
    TXSTA[4]=0 #set usart mode
    RCSTA[7]=1 #swich usart on 
    TXSTA[5]=1 #allow transmit mode: 5 =1, TXIF is set to 'auto'
    RCSTA[4]=1 #allow reacive mode
    
def serial_write(serial_sym):
    TXREG=serial_sym #write data to TXREG

serial_read_byte=0

def serial_check():
    if PIR1[5]==0: #Is data in buffer?
        return 0 #No data in buffer
    else:
        return 1
        
def serial_read():
    while not serial_check():
        pass

    serial_read_byte=RCREG #read data from RCREG
    return serial_read_byte
    #CREN=0 if overloop


