# Name:         Gauss interactive calculator
# Description:  This library includes the functions required by the Gauss
#               interactive calculator to work.
# Author:       Andres M. Aguirre-Mesa
#               PhD student, Mechanical Engineering.
#               University of Texas at San Antonio.
# Date:         June 10, 2019.
# Update:       January 19, 2019.


#*******************************************************************************
#                        Import libraries and functions
#*******************************************************************************

import sympy as sym

from sympy.parsing.sympy_parser import parse_expr

from ipywidgets import Layout, Text, HTML, HTMLMath, Box, HBox, VBox, Button, \
  Dropdown

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
def row_swap(M, rid1, rid2):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Swap two rows of a SymPy matrix.

  M:    SymPy matrix to be modified.
  rid1: integer identificator of a row. One based (1, 2, ...).
  rid2: identificator of another row. One based (1, 2, ...).

  Returns a new matrix with swapped rows.
  '''
#*******************************************************************************
 
  nrows = M.rows            # Get the number of rows.

  if (rid1 == rid2):        # Verify if the swap is not valid
  
    print('Error. No rows were swapped.')

    new_M = M.copy()

  elif (rid1 > nrows) or (rid2 > nrows):

    print(f'Error. Please use row indices from 1 through {nrows}.')

    new_M = M.copy()

  elif (rid1 == 0) or (rid2 == 0):
  
    print(f'Error. Please use row indices from 1 through {nrows}.')

    new_M = M.copy()

  else:

    # Create a list of indices.
    id_lst = [k for k in range(nrows)]    # Create a list of indices.

    id_lst[rid1 - 1] = rid2 - 1           # Swap indices in the list.
    id_lst[rid2 - 1] = rid1 - 1

    new_M = M[id_lst,:]                   # Reorganize matrix.

  # End if. 

  return new_M
 
#-------------------------------------------------------------------------------


#*******************************************************************************
def row_add(M, new_rid, c1, rid1, c2, rid2):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Set new values for a row that are the linear combination of two existing rows.

  M:        SymPy matrix to be modified.
  new_rid:  integer identificator of the row to be modified. One based (1, 2,
            ...).
  c1:       real, scalar value to multiply row 1.
  rid1:     integer identificator of row 1. One based (1, 2, ...).
  c2:       real, scalar value to multiply row 2.
  rid2:     integer identificator of row 2. One based (1, 2, ...).
  '''
#*******************************************************************************

  new_M = M.copy()

  if (new_rid != rid1) and (new_rid != rid2):

    print(f'Error. The index of the new row is {new_rid}.')
    print(f'It must be either {rid1} or {rid2}.')

  else:
 
    new_M[new_rid - 1, :] = c1*M[rid1 - 1, :] + c2*M[rid2 - 1, :]

  # End if.

  return new_M

#-------------------------------------------------------------------------------


#*******************************************************************************
def row_times_scalar(M, c, rid):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Multiplies the row of a Sympy matrix times a scalar value.

  M:        SymPy matrix to be modified.
  c:        real, scalar value to multiply the row.
  rid:      integer identificator of the row. One based (1, 2, ...).
  '''
#*******************************************************************************

  new_M = M.copy()

  new_M[rid - 1, :] = c*M[rid - 1, :]

  return new_M

#-------------------------------------------------------------------------------


#*******************************************************************************
def convert_mat_to_latex(M):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Convert a Sympy matrix to a LaTeX. It generates the code to print the
  augmented matrix used for the Gauss elimination process.

  M:        SymPy matrix to be modified.
  '''
#*******************************************************************************

  latex_str = r''' 
    \left[ \begin{{array}}{{rrr|r}}
        {:s} & {:s} & {:s} & {:s}\\
        {:s} & {:s} & {:s} & {:s}\\
        {:s} & {:s} & {:s} & {:s}
    \end{{array}} \right]
    '''

  latex_str = latex_str.format(
    str(M[0,0]), str(M[0,1]), str(M[0,2]), str(M[0,3]),
    str(M[1,0]), str(M[1,1]), str(M[1,2]), str(M[1,3]),
    str(M[2,0]), str(M[2,1]), str(M[2,2]), str(M[2,3]))

  return latex_str

#-------------------------------------------------------------------------------


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
  
  # Create the string with the initial augmented matrix in LaTeX format.
  latex_str = r'The augmented matrix $(\bf{A}|\bf{B})$ is:' + '\n $$' \
    + convert_mat_to_latex(M) + r'$$ with ' + detA_str + '.'
 
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

  rid1 = int(swap_rid1_drop.value)    # Read row indices.
  rid2 = int(swap_rid2_drop.value)

  if (not is_started):

    results_html.value = \
      'Error. Please enter the system of equations and press the start button.'

  else:

    M_old = M.copy()                  # Store the old augmented matrix.

    # Verify if the two row indices the same.

    if (rid1 == rid2):

      # If the indices are equal, create the error message, and do not call
      # the swapping function.

      err_str    = 'Error. No rows were swapped.\n'
      row_op_str = r'\Rightarrow'
    
    else: 

      # If the indices are different, call the swapping function.

      M = row_swap(M_old, rid1, rid2)
      
      err_str = ''

      row_op_str = \
        r'\stackrel{{ R_{:d} \leftrightarrow R_{:d} }}{{\Rightarrow}}'.format(
        rid1, rid2)

    # End if.

    # Update sympy matrices.
    M_old_str = convert_mat_to_latex(M_old)    
    M_str     = convert_mat_to_latex(M)

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

  if (not is_started):

    results_html.value = \
      'Error. Please enter the system of equations and press the start button.'

  else:

    M_old = M.copy()    # Store the old augmented matrix.

    # Verify if the constant is zero.

    if (str(c) == '0'):

      # If the constant is zero, create the error message, and do not call
      # the multiplication function.

      err_str    = 'Error. The constant must not be zero. ' +\
        'No operation was performed.\n'
      row_op_str = r'\Rightarrow'
    
    else: 

      # If the constant is not zero, call the multiplication function.

      M = row_times_scalar(M, c, rid)
      
      err_str = ''

      row_op_str = \
        r'\stackrel{{ {:s} \, R_{:d} }}{{\Rightarrow}}'.format(str(c), rid)

    # End if.

    # Update sympy matrices.
    M_old_str = convert_mat_to_latex(M_old)    
    M_str     = convert_mat_to_latex(M)

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

  if (not is_started):

    results_html.value = \
      'Error. Please enter the system of equations and press the start button.'

  else:

    M_old = M.copy()    # Store the old augmented matrix.

    # Verify if the two row indices the same.

    if (rid1 == rid2):

      # If the indices are equal, create the error message, and do not call
      # the addition function.

      err_str    = 'Error. The selection of rows for the addition ' + \
        'is not valid. No operation was performed.'
      row_op_str = r'\Rightarrow'
    
    else: 

      # If the indices are different, call the addition function.

      M = row_add(M_old, rid2, c1, rid1, c2, rid2)
      
      err_str = ''

      row_op_str = \
        r'\stackrel{{ {:s} \, R_{:d} + R_{:d} }}{{\Rightarrow}}'.format(
        str(c1), rid1, rid2)

    # End if.

    # Update sympy matrices.
    M_old_str = convert_mat_to_latex(M_old)    
    M_str     = convert_mat_to_latex(M)

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
