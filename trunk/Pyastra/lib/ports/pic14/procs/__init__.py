############################################################################
# $Id$
#
# Description: pic14 processor definitions. Pyastra project.
# Author: Alex Ziranov <estyler _at_ users _dot_ sourceforge _dot_ net>
#    
# Copyright (c) 2004 Alex Ziranov.  All rights reserved.
#
############################################################################
"""
Pic14 processor definitions. U{Pyastra project <http://pyastra.sourceforge.net>}.

All the processors must be listed in the C{__all__} dictionary to be
enabled. Files whose name end with "i" are definitions for processors with
ICD mode enabled.

Pyastra is shipped with C{inc2py.py} script that converts C{*.lkr} and
C{*.inc} files from the U{gputils <http://gputils.sourceforge.net>}
project into Pyastra processor definitions.

Every definition consists of:
    - B{hdikt:} Dictionary of registers. Keys are register names in
      uppercase and values are its 9-bit addresses.
    - B{pages:} Tuples with starts and ends of program memory pages.
    - B{banks:} Contains general-purpose register memory start and end
      addresses.
    - B{shareb:} Register memory addresses that are mirrored between each
      other. The tuples have the following format::
        shareb=(
            ((area11_start, area11_end), (area12_start, area12_end), ...),
            ((area21_start, area21_end), (area22_start, area22_end), ...),
            ...
        )
      Here area1 is from address C{area11_start} to C{area11_end} and its
      mirror is from address C{area12_start} to C{area12_end}.
    - B{vectors:} Tuple of interrupt vectors supported by the processor.
      Values are addresses.
    - B{maxram:} Maximal register address supported by the processor.

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

__all__ = [
    'pic12c508a',
    'pic12c508',
    'pic12c509a',
    'pic12c509',
    'pic12c671',
    'pic12c672',
    'pic12ce518',
    'pic12ce519',
    'pic12ce673',
    'pic12ce674',
    'pic12cr509a',
    'pic12f508',
    'pic12f509',
    'pic12f510',
    'pic12f629i',
    'pic12f629',
    'pic12f635i',
    'pic12f635',
    'pic12f675i',
    'pic12f675',
    'pic12f683i',
    'pic12f683',
    'pic14000',
    'pic16c432',
    'pic16c433',
    'pic16c505',
    'pic16c52',
    'pic16c54a',
    'pic16c54b',
    'pic16c54c',
    'pic16c54',
    'pic16c554',
    'pic16c557',
    'pic16c558',
    'pic16c55a',
    'pic16c55',
    'pic16c56a',
    'pic16c56',
    'pic16c57c',
    'pic16c57',
    'pic16c58a',
    'pic16c58b',
    'pic16c61',
    'pic16c620a',
    'pic16c620',
    'pic16c621a',
    'pic16c621',
    'pic16c622a',
    'pic16c622',
    'pic16c62a',
    'pic16c62b',
    'pic16c62',
    'pic16c63a',
    'pic16c63',
    'pic16c642',
    'pic16c64a',
    'pic16c64',
    'pic16c65a',
    'pic16c65b',
    'pic16c65',
    'pic16c662',
    'pic16c66',
    'pic16c67',
    'pic16c710',
    'pic16c711',
    'pic16c712',
    'pic16c715',
    'pic16c716',
    'pic16c717',
    'pic16c71',
    'pic16c72a',
    'pic16c72',
    'pic16c73a',
    'pic16c73b',
    'pic16c73',
    'pic16c745',
    'pic16c74a',
    'pic16c74b',
    'pic16c74',
    'pic16c765',
    'pic16c76',
    'pic16c770',
    'pic16c771',
    'pic16c773',
    'pic16c774',
    'pic16c77',
    'pic16c781',
    'pic16c782',
    'pic16c84',
    'pic16c923',
    'pic16c924',
    'pic16c925',
    'pic16c926',
    'pic16ce623',
    'pic16ce624',
    'pic16ce625',
    'pic16cr54a',
    'pic16cr54b',
    'pic16cr54c',
    'pic16cr54',
    'pic16cr56a',
    'pic16cr57a',
    'pic16cr57b',
    'pic16cr57c',
    'pic16cr58a',
    'pic16cr58b',
    'pic16cr620a',
    'pic16cr62',
    'pic16cr63',
    'pic16cr64',
    'pic16cr65',
    'pic16cr72',
    'pic16cr83',
    'pic16cr84',
    'pic16f505',
    'pic16f506',
    'pic16f54',
    'pic16f57',
    'pic16f59',
    'pic16f627ai',
    'pic16f627a',
    'pic16f627',
    'pic16f628ai',
    'pic16f628a',
    'pic16f628',
    'pic16f630i',
    'pic16f630',
    'pic16f636i',
    'pic16f636',
    'pic16f639i',
    'pic16f639',
    'pic16f648ai',
    'pic16f648a',
    'pic16f676i',
    'pic16f676',
    'pic16f684i',
    'pic16f684',
    'pic16f685',
    'pic16f687',
    'pic16f688i',
    'pic16f688',
    'pic16f689',
    'pic16f690',
    'pic16f716i',
    'pic16f716',
    'pic16f72',
    'pic16f737i',
    'pic16f737',
    'pic16f73',
    'pic16f747i',
    'pic16f747',
    'pic16f74',
    'pic16f767i',
    'pic16f767',
    'pic16f76',
    'pic16f777i',
    'pic16f777',
    'pic16f77',
    'pic16f785',
    'pic16f818i',
    'pic16f818',
    'pic16f819i',
    'pic16f819',
    'pic16f83',
    'pic16f84a',
    'pic16f84',
    'pic16f870i',
    'pic16f870',
    'pic16f871i',
    'pic16f871',
    'pic16f872i',
    'pic16f872',
    'pic16f873ai',
    'pic16f873a',
    'pic16f873i',
    'pic16f873',
    'pic16f874ai',
    'pic16f874a',
    'pic16f874i',
    'pic16f874',
    'pic16f876ai',
    'pic16f876a',
    'pic16f876i',
    'pic16f876',
    'pic16f877ai',
    'pic16f877a',
    'pic16f877i',
    'pic16f877',
    'pic16f87i',
    'pic16f87',
    'pic16f88i',
    'pic16f88',
    'pic16f913i',
    'pic16f913',
    'pic16f914i',
    'pic16f914',
    'pic16f916i',
    'pic16f916',
    'pic16f917i',
    'pic16f917',
    'pic16hv540',
]
