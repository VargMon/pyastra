############################################################################
# $Id$
#
# Description: PIC 14000 definition. Pyastra project.
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

hdikt={'RCIF': 0x2, 'BF': 0x0, 'RCIE': 0x2,
       'CKP': 0x4, 'OVFIE': 0x0, 'ADOFF': 0x0,
       'PBIE': 0x4, 'PBIF': 0x4, 'T0SE': 0x4,
       'PCFG3': 0x3, 'PCFG2': 0x2, 'PIE1': 0x8c,
       'D': 0x5, 'PREFA': 0x9b, 'PREFB': 0x9c,
       'PORTC': 0x7, 'PORTA': 0x5, 'P': 0x4,
       'GIE': 0x7, 'NOT_A': 0x5, 'SMBUS': 0x3,
       'SMHOG': 0x7, 'OSC2': 0x1, 'OSC1': 0x0,
       'ADCIE': 0x1, 'ADCIF': 0x1, 'I2COV': 0x6,
       'TEMPOFF': 0x1, 'ADZERO': 0x0, 'CMBOUT': 0x6,
       'CMAOUT': 0x2, 'I2CBUF': 0x13, 'PEIE': 0x6,
       'HIBEN': 0x7, 'CMIF': 0x7, 'CMIE': 0x7,
       'INTCON': 0xb, 'PCL': 0x2, 'I2CSTAT': 0x94,
       'PS2': 0x2, 'PS0': 0x0, 'PS1': 0x1,
       'WCOL': 0x7, 'CHGCON': 0x9d, 'ADDAC1': 0x5,
       'SPGNDA': 0x5, 'SPGNDB': 0x6, 'I2C_STOP': 0x4,
       'C': 0x0, 'TRISC': 0x87, 'MISC': 0x9e,
       'TRISA': 0x85, 'ADCON1': 0x9f, 'ADCON0': 0x1f,
       'TRISD': 0x88, 'REFOFF': 0x5, 'OPTION_REG': 0x81,
       'I2CSEL': 0x4, 'DATA_ADDRESS': 0x5, 'PIR1': 0xc,
       'R_W': 0x2, 'I2CIF': 0x3, 'I2CCON': 0x14,
       'I2CIE': 0x3, 'ADTMRH': 0xf, 'PSA': 0x3,
       'S': 0x3, 'I2C_READ': 0x2, 'T0CS': 0x5,
       'UA': 0x1, 'I2CADD': 0x93, 'ADCAPL': 0x15,
       'PCLATH': 0xa, 'ADCAPH': 0x16, 'OVFIF': 0x0,
       'PCON': 0x8e, 'NOT_RCPU': 0x7, 'NOT_LVD': 0x0,
       'FSR': 0x4, 'ADRST': 0x1, 'NOT_W': 0x2,
       'CPOLA': 0x0, 'ADCS3': 0x7, 'ADCS0': 0x4,
       'ADCS1': 0x5, 'CMBOE': 0x5, 'CCBEN': 0x5,
       'D_A': 0x5, 'CWUOFF': 0x2, 'CCAEN': 0x1,
       'STATUS': 0x3, 'I2CEN': 0x5, 'ADTMRL': 0xe,
       'R': 0x2, 'Z': 0x2, 'NOT_WRITE': 0x2,
       'AMUXOE': 0x2, 'LDACA': 0x9b, 'LDACB': 0x9c,
       'NOT_TO': 0x4, 'TMR0': 0x1, 'READ_WRITE': 0x2,
       'LSOFF': 0x4, 'ADCS2': 0x6, 'T0IF': 0x2,
       'T0IE': 0x5, 'SLPCON': 0x8f, 'ACFG2': 0x2,
       'ACFG3': 0x3, 'ACFG0': 0x0, 'ACFG1': 0x1,
       'NOT_PD': 0x3, 'DC': 0x1, 'I2CM2': 0x2,
       'I2CM3': 0x3, 'I2CM0': 0x0, 'I2CM1': 0x1,
       'CMCON': 0x9d, 'CMOFF': 0x2, 'BIASOFF': 0x4,
       'CMAOE': 0x1, 'I2C_DATA': 0x5, 'PORTD': 0x8,
       'OSCOFF': 0x3, 'RP1': 0x6, 'RP0': 0x5,
       'IRP': 0x7, 'ADDAC0': 0x4, 'ADDAC3': 0x7,
       'ADDAC2': 0x6, 'INCLKEN': 0x2, 'NOT_POR': 0x1,
       'WUIF': 0x7, 'WUIE': 0x7, 'I2C_START': 0x3,
       'NOT_ADDRESS': 0x5, 'INDF': 0x0, 'CPOLB': 0x4,
       'CCOMPA': 0x2, 'CCOMPB': 0x6, }

pages=((0x5, 0x07FF), (0x0800, 0x0FBF), )

banks=((0x20, 0x7F), (0xA0, 0xFF), )

shareb=(
)
