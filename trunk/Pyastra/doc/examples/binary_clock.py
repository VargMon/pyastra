############################################################################
# $Id$
#
# Description: Binary LED clock. Pyastra project.
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

#
# The LED panel should be connected to PIC like on this figure:
#
# +----------+----------+----------+
# |   hours  |  minutes |  seconds |
# +----------+----------+----------+
# |          | PORTC[5] | PORTA[5] |
# | PORTD[4] | PORTC[4] | PORTA[4] |
# | PORTD[3] | PORTC[3] | PORTA[3] |
# | PORTD[2] | PORTC[2] | PORTA[2] |
# | PORTD[1] | PORTC[1] | PORTA[1] |
# | PORTD[0] | PORTC[0] | PORTA[0] |
# +----------+----------+----------+
#
# Default values are for 16 MHz chips.
# Code is written for PIC16F877 but may be used on other chips
# with similar capabilities.
#
# Values for other popular frequencies:
# 
# +-----------+------+------+
# | Freq, MHz |  n0  |  n1  |
# +-----------+------+------+
# |        40 | 0x4a | 0x4c |
# |        20 | 0x25 | 0x26 |
# |         8 | 0x42 |  0xf |
# |         4 | 0xa1 |  0x7 |
# +-----------+------+------+
#
# To setup for other frequency you should:
# 1. Calculate n = 488.25 * f
#    where f is frequency in MHz.
# 2. n0 = 0xff & n
#    n1 = (0xff00 & n) >> 8
#
n0 = 0x84
n1 = 0x1e

# Setting time to 00:00:00
secs = mins = hours = 0


n0_cp = n0
n1_cp = n1

#
# This function updates LED panel
#
def update_leds():
    PORTA=secs
    PORTC=mins
    PORTD=hours

#
# This function will be called on every interrupt
#
def on_interrupt():
    # Check that interrupt came from timer 0
    if INTCON[T0IF]:
        # n = n - 1
        asm("""
            movlw   1
            subwf   _n0, f
            btfss   STATUS, C
            decf    _n1, f
        """)
        
        # n = 0 every next second
        if not (n0 or n1):
            n0 = n0_cp
            n1 = n1_cp
            secs += 1

            if secs == 60:
                secs = 0
                mins += 1
                if mins == 60:
                    hours += 1
                    mins = 0
                    if hours == 24:
                        hours = 0
            update_leds()
                
        INTCON[T0IF]=0

#
# Initializing ports
#
TRISA = TRISC = TRISD = 0
PORTA = PORTC = PORTD = 0

#
#Starting timer 0
#
OPTION_REG[T0CS]=0      #select internal cycle clock
OPTION_REG[PSA]=0       #prescaler is assigned for TMR0
OPTION_REG[PS2]=0       #set prescaler coefficient to 2
OPTION_REG[PS1]=0
OPTION_REG[PS0]=0
TMR0=0                  #reset timer's counter
INTCON=PIE1=PIE2=0      #clear TMR0 interrupt flag and disable other interrupts
INTCON[T0IE]=1          #enable TMR0 interrupt
INTCON[GIE]=1           #enable interrupts globally


