==============
Pyastra README
==============

To start use a command:

python pyastra.py infile [outfile]

Where infile is the python file you would like to compile. Outfile is
the assembler output file. If no outfile is given, then the name would
be selected automatically (e.g. test.py -> test.asm)

Current versions are very unstable. Some code may be generated
incorrectly. So you shouldn't use it in critical tasks! If you'll find a
bug please submit it on

https://sourceforge.net/tracker/?atid=643744&group_id=106265&func=browse


Syntax notes
------------

Syntax is planned as 100% standard python compatible (see
doc/STATUS.html <doc/README.html> to get more information about maturity).

No standard modules and libraries ported.

Built-ins are changed too. All pic's SFRs and bits names are defined in
CAPS (e.g. PORTA, STATUS, RP0). The following built-in functions are
supported:

asm(code, instr_count [, (local_var1, local_var2, ...)])
    include verbatim assembler code, that has instr_count
    instructions and uses local variables local_varN
    
halt()
    halt the system (iterates an infinite loop)
    
fbin('0101 0101')
    converts binary number to decimal one. Separators (spaces) are
    enabled for user's convenience.


Thanks for interesting in our project!

$Id$

