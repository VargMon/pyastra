
  Pyastra README

To start use a command:

pyastra [options] infile [outfile]

Where infile is the python file you would like to compile. Outfile is
the assembler output file. If no outfile is given, then the name would
be selected automatically (e.g. test.py -> test.asm)

Options are:
-m 	
	Set the port to use (default: -mpic14)
-mlist 	
	List available ports
-p 	
	Select port specific processor
-plist 	
	List supported port specific processors

	--icd 	Enable ICD support (disabled by default)

	--op-speed 	Optimize for speed (for code size by default)
-h 	--help 	Show this usage message


Current versions are very unstable. Some code may be generated
incorrectly. So you shouldn't use it in critical tasks! If you'll find a
bug please submit it on
https://sourceforge.net/tracker/?atid=643744&group_id=106265&func=browse

If it really works, please inform me for which microcontroller did you
used Pyastra and other thigs that may be important:
estyler (at) users (dot) sourceforge (dot) net
<mailto:estyler%20%28at%29%20users%20%28dot%29%20sourceforge%20%28dot%29%20net>


    Syntax notes

Syntax is planned as 100% standard python compatible (see
doc/STATUS.html <doc/README.html> to get more information about maturity).

No standard modules and libraries ported.

Built-ins are changed too. All pic's SFRs and bits names are defined in
CAPS (e.g. PORTA, STATUS, RP0). The following built-in functions are
supported:

asm(code, instr_count [, (local_var1, local_var2, ...)])
    include verbatim assembler |code|, that has |instr_count|
    instructions and uses local variables |local_varN|
halt()
    halt the system (iterates an infinite loop)
sleep()
    switch the system in sleep (power-down) mode (equivalent
    to the assembler SLEEP command)
fbin('0101 0101')
    converts binary number to decimal one. Separators (spaces) are
    enabled for user's convenience.

All the variables are unsigned bytes at this moment.
Bits of any byte may be accessed just like an element of an array:
some_var[5]=1   ;set bit 5 of some_var
some_var[7]=0   ;clear bit 7 of some_var

Thanks for interesting in our project!
$Id$

