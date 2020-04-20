# Name:         Determinant by reduction calculator
# Description:  This library includes the functions required by the determinants
#               calculator to work.
# Author:       Andres M. Aguirre-Mesa
#               PhD student, Mechanical Engineering.
#               University of Texas at San Antonio.
# Date:         April 18, 2020.

#*******************************************************************************
#                        Import libraries and functions
#*******************************************************************************

import sympy as sym

from sympy.parsing.sympy_parser import parse_expr

from ipywidgets import Layout, Text, HTML, HTMLMath, Box, HBox, VBox, Button, \
  Dropdown, RadioButtons

from lib_gauss import convert_mat_to_latex, row_swap, col_swap, \
  row_times_scalar, col_times_scalar, row_add, col_add


#*******************************************************************************
#           Global variables definition and notebook initialization
#*******************************************************************************

# NOTE: These commands are executed when the library is imported.


# Define initial values for the coefficient matrix A.
A = sym.Matrix([[4,  1, -2],
                [3, -1,  1],
                [1, -1,  1]])

is_started = False

# Create the matrix.
M = A.copy()

# Store two copies of the matrix.
M_0    = M.copy()   # Initial matrix.
M_old  = M.copy()   # Old matrix.

# Define layout for all text boxes that form the input matrix.
cell_layout = Layout(width='40px', height='35px')

# Create text boxes to enter the values of the matrix.
A11_tbox = Text(value=str(A[0,0]), layout=cell_layout)
A12_tbox = Text(value=str(A[0,1]), layout=cell_layout)
A13_tbox = Text(value=str(A[0,2]), layout=cell_layout)
A21_tbox = Text(value=str(A[1,0]), layout=cell_layout)
A22_tbox = Text(value=str(A[1,1]), layout=cell_layout)
A23_tbox = Text(value=str(A[1,2]), layout=cell_layout)
A31_tbox = Text(value=str(A[2,0]), layout=cell_layout)
A32_tbox = Text(value=str(A[2,1]), layout=cell_layout)
A33_tbox = Text(value=str(A[2,2]), layout=cell_layout)

# Create a description for the matrix.
mat_text = HTMLMath( 
  value=r'Enter here the values of matrix $\bf{A}$',
  layout=Layout(width='90px') ) 

# Group the text boxes in the shape of a 3x3 matrix.
mat_values = VBox([HBox([A11_tbox, A12_tbox, A13_tbox]),
                   HBox([A21_tbox, A22_tbox, A23_tbox]),
                   HBox([A31_tbox, A32_tbox, A33_tbox])])

# Put together description and values of the matrix.
mat_input = HBox([mat_text, mat_values]) 

# Create a text to describe the function of the start button.
start_text = HTML(
  value='Click this button to start the calculator',
  layout=Layout(width='120px') )

start_btn = Button(description='Start')          # Create a start button.

# Put together description and button.
start_input = VBox( [start_text, start_btn]) 

# Create a HTML object to show the equation in LaTeX format.
amat_latex = HTMLMath(
  value=r'Matrix $\bf{A}$ will appear here.', 
  layout=Layout(justify_content='center'))

# Put together all inputs.
all_inputs = Box( [mat_input, start_input, amat_latex], 
  layout=Layout(justify_content='space-around', flex_flow='row wrap') )

# Controls

# Controls for row or column swapping.

swap_radiobtn = RadioButtons(options=['rows', 'columns'],
  description='Swap by:')

swap_id1_drop = Dropdown( options=['1', '2', '3'], value='1',
  description='Swap row', layout=Layout(width='150px') )

swap_id2_drop = Dropdown( options=['1', '2', '3'], value='2',
  description='and row', layout=Layout(width='150px') )

swap_btn = Button(description='Swap rows')

swap_ctrl = VBox( [ swap_radiobtn, swap_id1_drop, swap_id2_drop, swap_btn ] )

# Controls for multiplication of a row or a column times a scalar.

mult_radiobtn = RadioButtons(options=['row', 'column'],
  description='Multiply:')

mult_id_drop = Dropdown( options=['1', '2', '3'], value='1',
  description='Row', layout=Layout(width='150px') )

mult_sc_tbox = Text(value='1', description='times',
  layout=Layout(width='150px')) 

mult_btn = Button(description='Multiply row')

mult_ctrl = VBox( [ mult_radiobtn, mult_id_drop, mult_sc_tbox, mult_btn ] )

# Controls for addition of two rows or two columns.

add_radiobtn = RadioButtons(options=['rows', 'columns'],
  description='Add:')

add_id1_drop = Dropdown( options=['1', '2', '3'], value='1',
  description='Add row', layout=Layout(width='150px') )

add_sc_tbox = Text(value='1', description='times',
  layout=Layout(width='150px')) 

add_id2_drop = Dropdown( options=['1', '2', '3'], value='2',
  description='to row', layout=Layout(width='150px') )

add_btn = Button(description='Add rows')

add_ctrl =  VBox([add_radiobtn, add_id1_drop, add_sc_tbox, add_id2_drop, add_btn])

# Put together all controls
all_ctrls = Box( [swap_ctrl, mult_ctrl, add_ctrl], 
  layout=Layout(justify_content='space-around', flex_flow='row wrap') )

# Display area

# Create a HTML object to show results in LaTeX format.
results_html = HTMLMath(value='Results will be shown here.', 
  layout=Layout(justify_content='center', height='300px'))


#*******************************************************************************
#                             Function definitions
#*******************************************************************************


#*******************************************************************************
def update_matrix(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Transfer the matrix contained in different input text boxes (A11_tbox,
  A12_tbox, etc) to the output HTMLMath object "amat_latex". This function is
  activated by the button "start_btn".

  change:   dictionary holding the information about the change of the button
            "start_btn". This argument is used to be compatible with the button
            object but not involved in the code of this function.
  '''
#*******************************************************************************

  global is_started, M, M_0, M_old, coeffs_lst, coeffs_lst_old
  
  is_started = True

  coeffs_lst = [sym.sympify(1)]
  
  coeffs_lst_old = coeffs_lst.copy()

  M[0,0] = parse_expr(A11_tbox.value)   # Get matrix for computations.
  M[0,1] = parse_expr(A12_tbox.value)
  M[0,2] = parse_expr(A13_tbox.value)
  M[1,0] = parse_expr(A21_tbox.value)
  M[1,1] = parse_expr(A22_tbox.value)
  M[1,2] = parse_expr(A23_tbox.value)
  M[2,0] = parse_expr(A31_tbox.value)
  M[2,1] = parse_expr(A32_tbox.value)
  M[2,2] = parse_expr(A33_tbox.value)

  # Store two copies of the matrix.
  M_0    = M.copy()   # Initial matrix.
  M_old  = M.copy()   # Old matrix.

  color_dict = {0: '', 1: '', 2: ''}

  # Create the string with the initial matrix in LaTeX format.
  latex_str = r'The initial matrix $\bf{A}$ is:' + '\n $$'  \
    + r'\left [' + convert_mat_to_latex(M, color_dict, 'rrr') + r'\right ] $$'
 
  # Update object "amat_latex" with the matrix in LaTeX format. 
  amat_latex.value=latex_str

  # Clear the contents of the results_html output.
  results_html.value = '' 

#-------------------------------------------------------------------------------


#*******************************************************************************
def update_swap_labels(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  val = swap_radiobtn.value

  if val == 'columns':
    swap_id1_drop.description = 'Swap col.'
    swap_id2_drop.description = 'and col.'
    swap_btn.description      = 'Swap columns'
  else:
    swap_id1_drop.description = 'Swap row'
    swap_id2_drop.description = 'and row'
    swap_btn.description      = 'Swap rows'
  # End if. 

#-------------------------------------------------------------------------------


#*******************************************************************************
def update_mult_labels(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  val = mult_radiobtn.value

  if val == 'column':
    mult_id_drop.description  = 'Column'
    mult_btn.description      = 'Multiply column'
  else:
    mult_id_drop.description  = 'Row'
    mult_btn.description      = 'Multiply row'
  # End if. 

#-------------------------------------------------------------------------------


#*******************************************************************************
def update_add_labels(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  val = add_radiobtn.value

  if val == 'columns':
    add_id1_drop.description = 'Add column'
    add_id2_drop.description = 'to column'
    add_btn.description      = 'Add columns'
  else:
    add_id1_drop.description = 'Add row'
    add_id2_drop.description = 'to row'
    add_btn.description      = 'Add rows'
  # End if. 

#-------------------------------------------------------------------------------


#*******************************************************************************
def apply_swap(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Performs the swapping of two rows or two columns when the button "swap_btn" is
  pressed.  Updates the Sympy matrices M and M_old, and the HTMLMath object
  "results_hmtl".

  change:   dictionary holding information about the change of the button
            "swap_btn". This argument is used to be compatible with the button
            object but not involved in the code of this function.
  '''
#*******************************************************************************

  global M, M_old, coeffs_lst, coeffs_lst_old

  id1 = int(swap_id1_drop.value)          # Read row or column indices.
  id2 = int(swap_id2_drop.value)

  if (not is_started):

    results_html.value = \
      'Error. Please enter a matrix and press the start button.'

  else:

    M_old = M.copy()                      # Store the old matrix.

    coeffs_lst_old = coeffs_lst.copy()    # Store the old coefficients list.

    # Verify if the two row indices the same.

    if (id1 == id2):

      # If the indices are equal, create the error message, and do not call
      # the swapping function.

      err_str    = '$$ $$' + 'Error. No rows or columns were swapped.\n'
      row_op_str = r'\text{No op.}'
    
    else: 

      # If the indices are different, call the swapping function.

      swap_opt = swap_radiobtn.value

      if swap_opt == 'columns':

        M = col_swap(M_old, id1, id2)

        op_str = r'(' + r'C_{:d}'.format(id1)  \
          + r' \leftrightarrow ' + r'C_{:d}'.format(id2) + r' )'

      else:

        M = row_swap(M_old, id1, id2)

        op_str = r'(' + r'R_{:d}'.format(id1)  \
          + r' \leftrightarrow ' + r'R_{:d}'.format(id2) + r' )'

      # End if.

      coeffs_lst.append(sym.sympify(-1))

      err_str = ''

    # End if.

    # Update sympy matrices.
    M_old_str = convert_mat_to_latex(M_old, align_opt='rrr')    
    M_str     = convert_mat_to_latex(M,     align_opt='rrr')

    prod_old = sym.S(1)
    for num in coeffs_lst_old:
      prod_old *= num
    # End for.

    if prod_old == sym.S(1):
      prod_old_str = ''
    else:
      prod_old_str = str(prod_old)
    # End if.

    prod = sym.S(1)
    for num in coeffs_lst:
      prod *= num
    # End for.

    if prod == sym.S(1):
      prod_str = ''
    else:
      prod_str = str(prod)
    # End if.

    # Update output.
    results_html.value += \
      err_str + '$$ $$' + r'$$ \overset{' + op_str + r'}{'  \
      + prod_old_str + r'\left |' + M_old_str + r'\right |'     \
      + r'\qquad = \qquad'                                      \
      + prod_str     + r'\left |' + M_str     + r'\right | }$$'

  # End if.

#-------------------------------------------------------------------------------


#*******************************************************************************
def apply_row_or_col_times_scalar(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Performs the multiplication of a row times a scalar when the button "mult_btn"
  is pressed.  Updates the Sympy matrices M and M_old, and the HTMLMath object
  "results_hmtl".

  change:   dictionary holding information about the change of the button
            "mult_btn". This argument is used to be compatible with the button
            object but not involved in the code of this function.
  '''
#*******************************************************************************

  global M, M_old, coeffs_lst, coeffs_lst_old

  rcid = int(mult_id_drop.value)          # Read row or column index.
  c    = parse_expr(mult_sc_tbox.value)   # Read scalar value.

  if (not is_started):

    results_html.value = \
      'Error. Please enter the system of equations and press the start button.'

  else:

    M_old = M.copy()                      # Store the old matrix.

    coeffs_lst_old = coeffs_lst.copy()    # Store the old coefficients list.

    # Verify if the constant is zero.

    if (str(c) == '0'):

      # If the constant is zero, create the error message, and do not call
      # the multiplication function.

      err_str    = '$$ $$' + 'Error. The constant must not be zero. ' +\
        'No operation was performed.\n'
      row_op_str = r'\Rightarrow'
    
    else: 

      # If the constant is not zero, call the multiplication function.

      mult_opt = mult_radiobtn.value

      if mult_opt == 'column':

        M = col_times_scalar(M, c, rcid)

        op_str = r'( {:s} \,'.format(str(c)) + r'C_{:d}'.format(rcid) \
          + r' \to ' + r'C_{:d}'.format(rcid) + r' )'

      else:

        M = row_times_scalar(M, c, rcid)

        op_str = r'( {:s} \,'.format(str(c)) + r'R_{:d}'.format(rcid) \
          + r' \to ' + r'R_{:d}'.format(rcid) + r' )'

      # End if.

      coeffs_lst.append(sym.S(1)/sym.sympify(c))

      err_str = ''

    # End if.

    # Update sympy matrices.
    M_old_str = convert_mat_to_latex(M_old, align_opt='rrr')    
    M_str     = convert_mat_to_latex(M,     align_opt='rrr')

    prod_old = sym.S(1)
    for num in coeffs_lst_old:
      prod_old *= num
    # End for.

    if prod_old == sym.S(1):
      prod_old_str = ''
    else:
      prod_old_str = str(prod_old)
    # End if.

    prod = sym.S(1)
    for num in coeffs_lst:
      prod *= num
    # End for.

    if prod == sym.S(1):
      prod_str = ''
    else:
      prod_str = str(prod)
    # End if.

    # Update output.
    results_html.value += \
      err_str + '$$ $$' + r'$$ \overset{' + op_str + r'}{'  \
      + prod_old_str + r'\left |' + M_old_str + r'\right |'     \
      + r'\qquad = \qquad'                                      \
      + prod_str     + r'\left |' + M_str     + r'\right | }$$'

  # End if.

#-------------------------------------------------------------------------------


#*******************************************************************************
def apply_row_or_col_add(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Performs the addition of two rows or two columns when the button "add_btn" is
  pressed.  Updates the Sympy matrices M and M_old, and the HTMLMath object
  "results_hmtl".

  change:   dictionary holding information about the change of the button
            "add_btn". This argument is used to be compatible with the button
            object but not involved in the code of this function.
  '''
#*******************************************************************************

  global M, M_old, coeffs_lst, coeffs_lst_old

  id1  = int(add_id1_drop.value)          # Read row or column indices.
  id2  = int(add_id2_drop.value)
  c1   = parse_expr(add_sc_tbox.value)    # Read scalars that multiply row 1 and
  c2   = parse_expr('1')                  # row 2 before add them.

  if (not is_started):

    results_html.value = \
      'Error. Please enter the system of equations and press the start button.'

  else:

    M_old = M.copy()    # Store the old matrix.

    # Verify if the two row indices the same.

    if (id1 == id2):

      # If the indices are equal, create the error message, and do not call
      # the addition function.

      err_str    = '$$ $$' + 'Error. The selection of rows for the addition ' +\
        'is not valid. No operation was performed.'
      row_op_str = r'\Rightarrow'
    
    else: 

      # If the indices are different, call the addition function.

      add_opt = add_radiobtn.value

      if add_opt == 'columns':

        M = col_add(M_old, id2, c1, id1, c2, id2)

        op_str = r'(' + '{:s}'.format(str(c1)) + r'C_{:d}'.format(id1) + ' + ' \
          + r'C_{:d}'.format(id2) + r' \to ' + r'C_{:d}'.format(id2) + r')'

      else:

        M = row_add(M_old, id2, c1, id1, c2, id2)

        op_str = r'(' + '{:s}'.format(str(c1)) + r'R_{:d}'.format(id1) + ' + ' \
          + r'R_{:d}'.format(id2) + r' \to ' + r'R_{:d}'.format(id2) + r')'

      # End if.
      
      err_str = ''

    # End if.

    # Update sympy matrices.
    M_old_str = convert_mat_to_latex(M_old, align_opt='rrr')    
    M_str     = convert_mat_to_latex(M,     align_opt='rrr')

    prod = sym.S(1)
    for num in coeffs_lst:
      prod *= num
    # End for.

    if prod == sym.S(1):
      prod_str = ''
    else:
      prod_str = str(prod)
    # End if.

    # Update output.
    results_html.value += \
      err_str + '$$ $$' + r'$$ \overset{' + op_str + r'}{'  \
      + prod_str + r'\left |' + M_old_str + r'\right |'     \
      + r'\qquad = \qquad'                                      \
      + prod_str  + r'\left |' + M_str     + r'\right | }$$'

  # End if.

#-------------------------------------------------------------------------------


#*******************************************************************************
def run_app():
#*******************************************************************************

  # Define the function associated with each widget.

  start_btn.on_click(update_matrix)

  swap_radiobtn.on_trait_change(update_swap_labels)
  mult_radiobtn.on_trait_change(update_mult_labels)
  add_radiobtn.on_trait_change(update_add_labels)

  swap_btn.on_click(apply_swap)
  mult_btn.on_click(apply_row_or_col_times_scalar)
  add_btn.on_click(apply_row_or_col_add)

  # Display all objects.
  display(all_inputs)     # Inputs.
  display(all_ctrls)      # Controls.
  display(results_html)   # Output.

#-------------------------------------------------------------------------------


if __name__=='__main__':

  run_app()

# End if.
