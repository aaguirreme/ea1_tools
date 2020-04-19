# Name:         Gauss interactive calculator
# Description:  This library includes the functions required by the Gauss
#               interactive calculator to work.
# Author:       Andres M. Aguirre-Mesa
#               PhD student, Mechanical Engineering.
#               University of Texas at San Antonio.
# Date:         June 10, 2019.
# Update:       April 18, 2020.

#*******************************************************************************
#                        Import libraries and functions
#*******************************************************************************

import sympy as sym

from sympy.parsing.sympy_parser import parse_expr

from ipywidgets import Layout, Text, HTML, HTMLMath, Box, HBox, VBox, Button, \
  Dropdown

from lib_gauss import convert_mat_to_latex, row_swap, row_times_scalar, row_add 


#*******************************************************************************
#           Global variables definition and notebook initialization
#*******************************************************************************

# NOTE: These commands are executed when the library is imported.

# Define initial values for the coefficient matrix A.
A = sym.Matrix([[4,  1, -2],
                [3, -1,  1],
                [1, -1,  1]])

# Define initial values for the constant (right hand side) matrix B.
B = sym.Matrix([ 3, 2, 0])

is_started = False

# Create the augmented matrix.
M = A.row_join(B)

# Store two copies of the augmented matrix.
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

# Create text boxes to enter the values of the right hand side vector.
B1_tbox  = Text(value=str(B[0]), layout=cell_layout)
B2_tbox  = Text(value=str(B[1]), layout=cell_layout)
B3_tbox  = Text(value=str(B[2]), layout=cell_layout)

# Create a description for the matrix.
mat_text = HTMLMath( 
  value=r'Enter here the values of the coefficient matrix $\bf{A}$',
  layout=Layout(width='90px') ) 

# Group the text boxes in the shape of a 3x3 matrix.
mat_values = VBox([HBox([A11_tbox, A12_tbox, A13_tbox]),
                   HBox([A21_tbox, A22_tbox, A23_tbox]),
                   HBox([A31_tbox, A32_tbox, A33_tbox])])

# Put together description and values of the matrix.
mat_input = HBox([mat_text, mat_values]) 

# Create a description for the RHS (right hand side) vector.
rhs_text = HTMLMath(
  value=r'Enter here the values of the constant matrix $\bf{B}$',
  layout=Layout(width='90px') ) 

# Group the text boxes in the shape of a 3x1 vector.
rhs_values = VBox( [B1_tbox, B2_tbox, B3_tbox], layout=Layout(width='50px') )

# Put together description and values of the matrix.
rhs_input = HBox([rhs_values, rhs_text]) 

# Create a text to describe the function of the start button.
start_text = HTML(
  value='Click this button to start the calculator',
  layout=Layout(width='120px') )

start_btn = Button(description='Start')          # Create a start button.

# Put together description and button.
start_input = VBox( [start_text, start_btn]) 

# Create a HTML object to show the augmented equation in LaTeX format.
amat_latex = HTMLMath(
  value=r'The augmented matrix $(\bf{A}|\bf{B})$ will appear here.',
  layout=Layout(justify_content='center'))

# Put together all inputs.
all_inputs = Box( [mat_input, rhs_input, start_input, amat_latex], 
  layout=Layout(justify_content='space-around', flex_flow='row wrap') )

# Controls

# Controls for row swapping.

swap_rid1_drop = Dropdown( options=['1', '2', '3'], value='1',
  description='Swap row', layout=Layout(width='150px') )

swap_rid2_drop = Dropdown( options=['1', '2', '3'], value='2',
  description='and row', layout=Layout(width='150px') )

swap_btn = Button(description='Swap rows')

swap_ctrl = VBox( [ swap_rid1_drop, swap_rid2_drop, swap_btn ] )

# Controls for multiplication of a row times a scalar.

mult_rid_drop = Dropdown( options=['1', '2', '3'], value='1',
  description='Row', layout=Layout(width='150px') )

mult_sc_tbox = Text(value='1', description='times',
  layout=Layout(width='150px')) 

mult_btn = Button(description='Multiply row')

mult_ctrl = VBox( [ mult_rid_drop, mult_sc_tbox, mult_btn ] )

# Controls for addition of two rows.

add_rid1_drop = Dropdown( options=['1', '2', '3'], value='1',
  description='Add row', layout=Layout(width='150px') )

add_sc_tbox = Text(value='1', description='times',
  layout=Layout(width='150px')) 

add_rid2_drop = Dropdown( options=['1', '2', '3'], value='2',
  description='to row', layout=Layout(width='150px') )

add_btn = Button(description='Add rows')

add_ctrl = HBox( [ VBox([add_rid1_drop, add_sc_tbox]), 
                   VBox([add_rid2_drop, add_btn    ]) ] )

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
def update_aug_matrix(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Transfer the augmented matrix contained in different input text boxes
  (A11_tbox, A12_tbox, ..., B1_tbox, B2_tbox, etc) to the output HTMLMath object
  "amat_latex". This function is activated by the button "start_btn".

  change:   dictionary holding the information about the change of the button
            "start_btn". This argument is used to be compatible with the button
            object but not involved in the code of this function.
  '''
#*******************************************************************************

  global is_started, M, M_0, M_old
  
  is_started = True

  A[0,0] = parse_expr(A11_tbox.value)   # Update augmented matrix.
  A[0,1] = parse_expr(A12_tbox.value)
  A[0,2] = parse_expr(A13_tbox.value)
  A[1,0] = parse_expr(A21_tbox.value)
  A[1,1] = parse_expr(A22_tbox.value)
  A[1,2] = parse_expr(A23_tbox.value)
  A[2,0] = parse_expr(A31_tbox.value)
  A[2,1] = parse_expr(A32_tbox.value)
  A[2,2] = parse_expr(A33_tbox.value)

  B[0] = parse_expr(B1_tbox.value)
  B[1] = parse_expr(B2_tbox.value)
  B[2] = parse_expr(B3_tbox.value)

  # Create the augmented matrix.
  M = A.row_join(B)
  
  # Store two copies of the augmented matrix.
  M_0    = M.copy()   # Initial matrix.
  M_old  = M.copy()   # Old matrix.

  detA = A.det()      # Compute determinant.

  if detA == 0:
    
    detA_str = r'$\color{red}{ \det A =' + f'{detA}' + r'}$'
  
  else:
  
    detA_str = r'$\det A =' + f'{detA}' + r'$'
    
  # End if.
 
  color_dict = {0: '', 1: '', 2: ''}

  # Create the string with the initial augmented matrix in LaTeX format.
  latex_str = r'The augmented matrix $(\bf{A}|\bf{B})$ is:' + '\n $$' \
    + convert_mat_to_latex(M, color_dict, 'rrr|r') + r'$$ with ' \
    + detA_str + '.'
 
  # Update object "amat_latex" with the augmented matrix in LaTeX format. 
  amat_latex.value=latex_str

  # Clear the contents of the results_html output.
  results_html.value = '' 

#-------------------------------------------------------------------------------


#*******************************************************************************
def apply_row_swap(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Performs the swapping of two rows when the button "swap_btn" is pressed.
  Updates the Sympy matrices M and M_old, and the HTMLMath object
  "results_hmtl".

  change:   dictionary holding information about the change of the button
            "swap_btn". This argument is used to be compatible with the button
            object but not involved in the code of this function.
  '''
#*******************************************************************************

  global M, M_old

  rid1 = int(swap_rid1_drop.value)        # Read row indices.
  rid2 = int(swap_rid2_drop.value)

  color_M_old = {0: '', 1: '', 2: ''}     # Initialize color dictionaries.
  color_M     = {0: '', 1: '', 2: ''}

  if (not is_started):

    results_html.value = \
      'Error. Please enter the system of equations and press the start button.'

  else:

    M_old = M.copy()                      # Store the old augmented matrix.

    # Verify if the two row indices the same.

    if (rid1 == rid2):

      # If the indices are equal, create the error message, and do not call
      # the swapping function.

      err_str    = '$$ $$' + 'Error. No rows were swapped.\n'
      row_op_str = r'\Rightarrow'
    
    else: 

      # If the indices are different, call the swapping function.

      M = row_swap(M_old, rid1, rid2)

      err_str = ''

      row_op_str = r'\stackrel{ ' + r'\color{blue}{' + r'R_{:d}'.format(rid1) \
        + r'} \leftrightarrow \color{red}{' + r'R_{:d}'.format(rid2)          \
        + r'}}{\Longrightarrow}'

      color_M_old[rid1 - 1] = 'blue'
      color_M_old[rid2 - 1] = 'red'

      color_M[rid2 - 1] = 'blue'
      color_M[rid1 - 1] = 'red'

    # End if.

    # Update sympy matrices.
    M_old_str = convert_mat_to_latex(M_old, color_M_old, 'rrr|r')    
    M_str     = convert_mat_to_latex(M, color_M, 'rrr|r')

    # Update output.
    results_html.value += err_str + '$$ $$' + '$$' + M_old_str + row_op_str + \
      M_str + '$$'

  # End if.

#-------------------------------------------------------------------------------


#*******************************************************************************
def apply_row_times_scalar(change):
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

  global M, M_old

  rid = int(mult_rid_drop.value)          # Read row index.
  c   = parse_expr(mult_sc_tbox.value)    # Read scalar value.

  color_M_old = {0: '', 1: '', 2: ''}     # Initialize color dictionaries.
  color_M     = {0: '', 1: '', 2: ''}

  if (not is_started):

    results_html.value = \
      'Error. Please enter the system of equations and press the start button.'

  else:

    M_old = M.copy()                      # Store the old augmented matrix.

    # Verify if the constant is zero.

    if (str(c) == '0'):

      # If the constant is zero, create the error message, and do not call
      # the multiplication function.

      err_str    = '$$ $$' + 'Error. The constant must not be zero. ' +\
        'No operation was performed.\n'
      row_op_str = r'\Rightarrow'
    
    else: 

      # If the constant is not zero, call the multiplication function.

      M = row_times_scalar(M, c, rid)
      
      err_str = ''

      row_op_str = r'\stackrel{ ' + r'{:s} \,'.format(str(c)) \
        + r'\color{red}{' + r'R_{:d}'.format(rid)             \
        + r'} \to \color{green}{' + r'R_{:d}'.format(rid)     \
        + r'}}{\Longrightarrow}'

      color_M_old[rid - 1] = 'red'
      color_M[rid - 1]     = 'green'

    # End if.

    # Update sympy matrices.
    M_old_str = convert_mat_to_latex(M_old, color_M_old, 'rrr|r')    
    M_str     = convert_mat_to_latex(M, color_M, 'rrr|r')

    # Update output.
    results_html.value += err_str + '$$ $$' + '$$' + M_old_str + row_op_str \
      + M_str + '$$'

  # End if.

#-------------------------------------------------------------------------------


#*******************************************************************************
def apply_row_add(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Performs the addition of two rows when the button "add_btn" is pressed.
  Updates the Sympy matrices M and M_old, and the HTMLMath object
  "results_hmtl".

  change:   dictionary holding information about the change of the button
            "add_btn". This argument is used to be compatible with the button
            object but not involved in the code of this function.
  '''
#*******************************************************************************

  global M, M_old

  rid1 = int(add_rid1_drop.value)         # Read row indices.
  rid2 = int(add_rid2_drop.value)
  c1   = parse_expr(add_sc_tbox.value)    # Read scalars that multiply row 1 and
  c2   = parse_expr('1')                  # row 2 before add them.

  color_M_old = {0: '', 1: '', 2: ''}     # Initialize color dictionaries.
  color_M     = {0: '', 1: '', 2: ''}

  if (not is_started):

    results_html.value = \
      'Error. Please enter the system of equations and press the start button.'

  else:

    M_old = M.copy()    # Store the old augmented matrix.

    # Verify if the two row indices the same.

    if (rid1 == rid2):

      # If the indices are equal, create the error message, and do not call
      # the addition function.

      err_str    = '$$ $$' + 'Error. The selection of rows for the addition ' +\
        'is not valid. No operation was performed.'
      row_op_str = r'\Rightarrow'
    
    else: 

      # If the indices are different, call the addition function.

      M = row_add(M_old, rid2, c1, rid1, c2, rid2)
      
      err_str = ''

      row_op_str = r'\stackrel{ ' + '{:s}'.format(str(c1))  \
        + r'\color{blue}{' + r'R_{:d}'.format(rid1) +'} + ' \
        + r'\color{red}{'  + r'R_{:d}'.format(rid2)         \
        + r'} \to \color{green}{' + r'R_{:d}'.format(rid2)  \
        + r'}}{\Longrightarrow}'

      color_M_old[rid1 - 1] = 'blue'
      color_M_old[rid2 - 1] = 'red'

      color_M[rid1 - 1] = 'blue'
      color_M[rid2 - 1] = 'green'

    # End if.

    # Update sympy matrices.
    M_old_str = convert_mat_to_latex(M_old, color_M_old, 'rrr|r')
    M_str     = convert_mat_to_latex(M, color_M, 'rrr|r')

    # Update output.
    results_html.value += err_str + '$$ $$' + '$$' + M_old_str + row_op_str \
      + M_str + '$$'

  # End if.

#-------------------------------------------------------------------------------


#*******************************************************************************
def run_app():
#*******************************************************************************

  start_btn.on_click(update_aug_matrix)       # Define the function associated
  swap_btn.on_click(apply_row_swap)           # with each button.
  mult_btn.on_click(apply_row_times_scalar)
  add_btn.on_click(apply_row_add)

  # Display all objects.
  display(all_inputs)     # Inputs.
  display(all_ctrls)      # Controls.
  display(results_html)   # Output.

#-------------------------------------------------------------------------------


if __name__=='__main__':

  run_app()

# End if.
