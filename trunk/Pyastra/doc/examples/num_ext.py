############################################################################
# $Id$
#
# Description: Numeric extensions. Pyastra project.
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
# little-endian functions
# mixed size
#

#
# Divides 16-bit number (word) by 7-bit number(byte).
# The result is stored in:
#   * div16_8_quo - the quotient (16 bits)
#   * div16_8_rem - the remainder (8 bits)
#
# NOTE: this function always work correctly only if div16_8_right < 0x80
#
def div16_8(div16_8_left_l, div16_8_left_h, div16_8_right):
    div16_8_cntr = 16
    div16_8_quo_h = div16_8_quo_l = div16_8_rem = 0
    
    asm("""
div16_8_loop3
        bcf     STATUS, C
        rlf     _div16_8_left_l, f
        rlf     _div16_8_left_h, f
        rlf     _div16_8_rem, f
        movf    _div16_8_right, w
        subwf   _div16_8_rem, w
div16_8_nochk
        btfss   STATUS, C       ;C is false when div16_8_rem<div16_8_right
        goto    div16_8_nogo
        movf    _div16_8_right, w
        subwf   _div16_8_rem, f
        bsf     STATUS, C
div16_8_nogo
        rlf     _div16_8_quo_l, f
        rlf     _div16_8_quo_h, f
        decfsz  _div16_8_cntr, f
        goto    div16_8_loop3
    """)
    
#
#saves result in add32_16_left
#
def add32_16(add32_16_left0, add32_16_left1, add32_16_left2, add32_16_left3, add32_16_right_l, add32_16_right_h):
    add32_16_right_l
    asm("""
	movf	_add32_16_right_l, w
	addwf	_add32_16_left0, f
	btfss	STATUS, C	;byte #0 overflow
	goto	add32_16_cont0
	incf	_add32_16_left1, f
	btfsc	STATUS, Z	;byte #1 overflow
	goto	add32_16_cont1
add32_16_cont0
	movf	_add32_16_right_h, w
	addwf	_add32_16_left1, f
	btfss	STATUS, C	;byte #1 overflow
	goto	add32_16_cont2
add32_16_cont1
	incf	_add32_16_left2, f
	btfsc	STATUS, Z	;byte #2 overflow
	incf	_add32_16_left3, f	;byte #3 overflow is thought unreachable
add32_16_cont2
""")
    
def div24_8(div24_8_left0, div24_8_left1, div24_8_left2, div24_8_right):
    div24_8_cntr = 24
    div24_8_quo0 = div24_8_quo1 = div24_8_quo2 = div24_8_rem = 0
    
    asm("""
div24_8_loop3
        bcf     STATUS, C
        rlf     _div24_8_left0, f
        rlf     _div24_8_left1, f
        rlf     _div24_8_left2, f
        rlf     _div24_8_rem, f
        movf    _div24_8_right, w
        subwf   _div24_8_rem, w
div24_8_nochk
        btfss   STATUS, C       ;C is false when div24_8_rem<div24_8_right
        goto    div24_8_nogo
        movf    _div24_8_right, w
        subwf   _div24_8_rem, f
        bsf     STATUS, C
div24_8_nogo
        rlf     _div24_8_quo0, f
        rlf     _div24_8_quo1, f
        rlf     _div24_8_quo2, f
        decfsz  _div24_8_cntr, f
        goto    div24_8_loop3
    """)

#
# bin-endian functions
#
# +----+--------+--------+--------+
# |    | 16-bit | 24-bit | 32-bit |
# +----+--------+--------+--------+
# |  + |    y   |        |    y   |
# |  - |    y   |        |    y   |
# |  * |    y!  |        |        |
# |  / |    y   |        |    y   |
# | >> |    y   |        |        |
# | << |    y   |        |        |
# +----+--------+--------+--------+
#

#
# 16-bit functions
#
    
def add16(add16_left1, add16_left0, add16_right1, add16_right0):
    add16_res1 = 0
    
    asm("""
        movf    _add16_left0,  w
        addwf   _add16_right0, w
        movwf   _add16_res0
        btfsc   STATUS, C
        incf    _add16_res1, f
        
        movf    _add16_left1,  w
        addwf   _add16_right1, w
        addwf   _add16_res1, f
""")
    
def sub16(sub16_left1, sub16_left0, sub16_right1, sub16_right0):
    sub16_res1 = 0
    
    asm("""
        movf    _sub16_right0,  w
        subwf   _sub16_left0, w
        movwf   _sub16_res0
        btfss   STATUS, C
        decf    _sub16_res1, f
        
        movf    _sub16_right1,  w
        subwf   _sub16_left1, w
        addwf   _sub16_res1, f
""")

def mul16(mul16_left1, mul16_left0, mul16_right1, mul16_right0):
    mul16_res0 = mul16_res1 = mul16_res2 = mul16_res3 = 0
    mul16_temp=16

    asm("""
    
mul16_loop
        bcf STATUS, C
        rlf _mul16_res0, f
        rlf _mul16_res1, f
        rlf _mul16_res2, f
        rlf _mul16_res3, f

        rlf _mul16_left0,    f
        rlf _mul16_left1,    f

        btfss   STATUS, C
        goto    mul16_no_add
        
        movf    _mul16_right0,  w
        addwf   _mul16_res0,    f
        btfss   STATUS, C
        goto    mul16_no_ovf0
        incf    _mul16_res1,    f
        btfss   STATUS, Z
        goto    mul16_no_ovf0
        incf    _mul16_res2,    f
        btfsc   STATUS, Z
        incf    _mul16_res3,    f
mul16_no_ovf0
        
        movf    _mul16_right1,  w
        addwf   _mul16_res1,    f
        btfss   STATUS, C
        goto    mul16_no_ovf1
        incf    _mul16_res2,    f
        btfsc   STATUS, Z
        incf    _mul16_res3,    f
mul16_no_ovf1

mul16_no_add
        decfsz  _mul16_temp, f
        goto    mul16_loop
        """)

def div16(div16_left1, div16_left0, div16_right1, div16_right0):
    div16_cntr = 16
    div16_quo0=div16_quo1=0
    div16_rem0=div16_rem1=0
    
    asm("""
div16_loop
	bcf	STATUS, C
	rlf	_div16_left0, f
	rlf	_div16_left1, f
	rlf	_div16_rem0, f
	rlf	_div16_rem1, f
        movf	_div16_right1, w
        subwf   _div16_rem1, w
        btfss   STATUS, Z
        goto    div16_nochk
        movf	_div16_right0, w
        subwf   _div16_rem0, w
div16_nochk
	btfss	STATUS, C	;C is false when _ACC_c<msc
	goto	div16_nogo
        
 	movf	_div16_right0, w
	subwf	_div16_rem0, f
	btfss	STATUS, C
        decf    _div16_rem1, f

 	movf	_div16_right1, w
	subwf	_div16_rem1, f
	bsf	STATUS, C
div16_nogo
	rlf	_div16_quo0, f
	rlf	_div16_quo1, f
	decfsz	_div16_cntr, f
	goto	div16_loop
""")

def rrf16(rrf16_arg1, rrf16_arg0):
    asm("""
        bcf     STATUS, C
        rrf     _rrf16_arg1, w
        movwf   _rrf16_res1
        rrf     _rrf16_arg0, w
        movwf   _rrf16_res0
    """)

def rlf16(rlf16_arg1, rlf16_arg0):
    asm("""
        bcf     STATUS, C
        rlf     _rlf16_arg0, w
        movwf   _rlf16_res0
        rlf     _rlf16_arg1, w
        movwf   _rlf16_res1
    """)
    
#
# 32-bit functions
#

def div32(div32_left3, div32_left2, div32_left1, div32_left0, div32_right3, div32_right2, div32_right1, div32_right0):
    div32_cntr = 32
    div32_quo0=div32_quo1=div32_quo2=div32_quo3=0
    div32_rem0=div32_rem1=div32_rem2=div32_rem3=0
    
    asm("""
div32_loop
	bcf	STATUS, C
	rlf	_div32_left0, f
	rlf	_div32_left1, f
	rlf	_div32_left2, f
	rlf	_div32_left3, f
	rlf	_div32_rem0, f
	rlf	_div32_rem1, f
	rlf	_div32_rem2, f
        rlf     _div32_rem3, f
	movf	_div32_right3, w
        subwf   _div32_rem3, w
        btfss   STATUS, Z
        goto    div32_nochk
	movf	_div32_right2, w
        subwf   _div32_rem2, w
        btfss   STATUS, Z
        goto    div32_nochk
        movf	_div32_right1, w
        subwf   _div32_rem1, w
        btfss   STATUS, Z
        goto    div32_nochk
        movf	_div32_right0, w
        subwf   _div32_rem0, w
div32_nochk
	btfss	STATUS, C	;C is false when _ACC_c<msc
	goto	div32_nogo
        
 	movf	_div32_right0, w
	subwf	_div32_rem0, f
	btfsc	STATUS, C
	goto	div32_no_ovf0
        movlw   1
        subwf   _div32_rem1, f
        btfsc	STATUS, C
	goto	div32_no_ovf0
	movlw	1
	subwf	_div32_rem2, f
	btfss	STATUS, C
	decf	_div32_rem3, f
div32_no_ovf0
 	movf	_div32_right1, w
	subwf	_div32_rem1, f
	btfsc	STATUS, C
	goto	div32_no_ovf1
	movlw	1
	subwf	_div32_rem2, f
	btfss	STATUS, C
	decf	_div32_rem3, f
div32_no_ovf1
	movf	_div32_right2, w
	subwf	_div32_rem2, f
	btfss	STATUS, C
	decf	_div32_rem3, f
div32_no_ovf2
	movf	_div32_right3, w
	subwf	_div32_rem3, f
	bsf	STATUS, C
div32_nogo
	rlf	_div32_quo0, f
	rlf	_div32_quo1, f
	rlf	_div32_quo2, f
	rlf	_div32_quo3, f
	decfsz	_div32_cntr, f
	goto	div32_loop
""")

def sub32(sub32_left3, sub32_left2, sub32_left1, sub32_left0, sub32_right3, sub32_right2, sub32_right1, sub32_right0):
    sub32_res0 = sub32_res1 = sub32_res2 = sub32_res3 = 0
    
    asm("""
 	movf	_sub32_right0, w
	subwf	_sub32_left0, w
        movwf   _sub32_res0
	btfss	STATUS, C
	decf	_sub32_res1, f

 	movf	_sub32_right1, w
	subwf	_sub32_left1, w
	btfss	STATUS, C
	decf	_sub32_res2, f
        addwf   _sub32_res1,    f

	movf	_sub32_right2, w
	subwf	_sub32_left2, w
	btfss	STATUS, C
	decf	_sub32_res3, f
        addwf   _sub32_res2,    f

	movf	_sub32_right3, w
	subwf	_sub32_left3, w
        addwf   _sub32_res3,    f
""")
    
def add32(add32_left3, add32_left2, add32_left1, add32_left0, add32_right3, add32_right2, add32_right1, add32_right0):
    add32_res1 = add32_res2 = add32_res3 = 0
    
    asm("""
        movf    _add32_left0,  w
        addwf   _add32_right0, w
        movwf   _add32_res0
        btfsc   STATUS, C
        incf    _add32_res1, f

        movf    _add32_left1,  w
        addwf   _add32_right1, w
        addwf   _add32_res1,   f
        btfsc   STATUS, C
        incf    _add32_res2, f

        movf    _add32_left2,  w
        addwf   _add32_right2, w
        addwf   _add32_res2,   f
        btfsc   STATUS, C
        incf    _add32_res3, f
        
        movf    _add32_left3,  w
        addwf   _add32_right3, w
        addwf   _add32_res3, f
""")
    
