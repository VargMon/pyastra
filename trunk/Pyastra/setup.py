#!/usr/bin/env python
############################################################################
# $Id$
#
# Description: Setup script. Pyastra project.
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

from distutils.core import setup
VERSION='0.0.1'

setup(name='Pyastra',
      version=VERSION,
      description='PYthon to ASsembler TRAnslator',
      author='Alex Ziranov',
      author_email='estyler@users.sourceforge.net',
      url='http://pyastra.sourceforge.net/',
      package_dir = {'pyastra': '.'},
      packages=['pyastra'],
      scripts=['pyastra'],
      data_files=[('share/doc/pyastra-%s' % VERSION, ['doc/STATUS.html', 'doc/TODO.html', 'LICENSE', ]),
                  ('share/doc/pyastra-%s/scripts' % VERSION, ['scripts/inc2py.py', ]),
                  ('share/pixmaps', ['pyastra_48x48.xpm', ]),
                 ],
      license='GPL',
      long_description="""
PYthon to ASsembler TRAnslator. At this moment supports Microchip PIC16
instruction set only. Its main goals are:

* to support a wide range of microcontrollers and processors

* to generate compact and effective code.

*NOTE: this is a preview release. This is NOT intended for general use
(because it's fairly unfinished).*
""",
      classifiers = [
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console (Text Based)',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Manufacturing',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Compilers',
          'Translations :: English',
      ],
     )
