************ PPyyaassttrraa RREEAADDMMEE ************
To start use a command:
python pyastra.py infile [outfile]
Where infile is the python file you would like to compile. Outfile is the
assembler output file. If no outfile is given, then the name would be selected
automatically (e.g. test.py -> test.asm)

Current versions are very unstable. Some code may be generated incorrectly. So
you shouldn't use it in critical tasks! If you'll find a bug please submit it
on
_h_t_t_p_s_:_/_/_s_o_u_r_c_e_f_o_r_g_e_._n_e_t_/_t_r_a_c_k_e_r_/_?_a_t_i_d_=_6_4_3_7_4_4_&_g_r_o_u_p___i_d_=_1_0_6_2_6_5_&_f_u_n_c_=_b_r_o_w_s_e

********** SSyynnttaaxx nnootteess **********
Syntax is planned as 100% standard python compatible (see _d_o_c_/_S_T_A_T_U_S_._h_t_m_l to
get more information about maturity).

No standard modules and libraries ported.

Built-ins are changed too. All pic's SFRs and bits names are defined in CAPS
(e.g. PORTA, STATUS, RP0). The following built-in functions are supported:
  asm(code, instr_count [, (local_var1, local_var2, ...)])
      include verbatim assembler code, that has instr_count instructions and
      uses local variables local_varN
  halt()
      halt the system (iterates an infinite loop)
  fbin('0101 0101')
      converts binary number to decimal one. Separators (spaces) are enabled
      for user's convenience.

Thanks for interesting in our project!
$Id$

