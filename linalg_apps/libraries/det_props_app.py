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

from lib_linalg import gen_text_grid, convert_mat_to_latex, row_swap, col_swap, \
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

# Store two copies of the matrix.
B = A.copy()    # New matrix.

# Define layout for all text boxes that form the input matrix.
cell_layout = Layout(width='40px', height='35px')

# Create a description for the matrix.
mat_text = HTMLMath( 
  value=r'Enter here the values of the matrix $\bf{A}$',
  layout=Layout(width='90px') ) 

# Create a 3x3 array of the text boxes.
mat_values = gen_text_grid(A.rows, A.cols, cell_layout, '45px')

# Define the values of the text boxes.
for i in range(A.rows):
  for j in range(A.cols):
    mat_values.children[A.rows*i + j].value = str(A[i,j])
  # End for. Loop over columns
# End for. Loop over rows.

# Put together description and values of the matrix.
mat_input = HBox([mat_text, mat_values], layout=Layout(width='250px',
  height='120px')) 

# Create a text to describe the function of the start button.
start_text = HTML(
  value='Click this button to start the calculator',
  layout=Layout(width='120px') )

start_btn = Button(description='Start')          # Create a start button.

# Put together description and button.
start_input = VBox( [start_text, start_btn]) 

# Put together all inputs.
all_inputs = Box( [mat_input, start_input], 
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

add_ctrl = VBox([add_radiobtn, add_id1_drop, add_sc_tbox, add_id2_drop, add_btn])

# Controls for matrix transpose.

transp_btn = Button(description='Transpose matrix', 
  layout=Layout(width='150px'))

# Put together all row operation controls
all_ctrls = Box( [swap_ctrl, mult_ctrl, add_ctrl], 
  layout=Layout(justify_content='space-around', flex_flow='row wrap') )

# Display area

A_html = HTMLMath(
  value=r'The old matrix $\bf{A}$ will appear here.', 
  layout=Layout(justify_content='center', height='150px'))

B_html = HTMLMath(
  value=r'The current matrix $\bf{B}$ will appear here.', 
  layout=Layout(justify_content='center', height='150px'))

transp_and_AB = Box( [transp_btn, A_html, B_html], 
  layout=Layout(justify_content='space-around', flex_flow='row wrap',
  align_items='center') )


#*******************************************************************************
#                             Function definitions
#*******************************************************************************


#*******************************************************************************
def update_matrix(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Transfer the matrix contained in different input text boxes (A11_tbox,
  A12_tbox, etc) to the output HTMLMath object "A_html". This function is
  activated by the button "start_btn".

  change:   dictionary holding the information about the change of the button
            "start_btn". This argument is used to be compatible with the button
            object but not involved in the code of this function.
  '''
#*******************************************************************************

  global is_started, A
  
  is_started = True

  # Update matrix.

  for i in range(A.rows):
    for j in range(A.cols):
      A[i,j] = parse_expr(mat_values.children[A.rows*i + j].value)
    # End for. Loop over columns
  # End for. Loop over rows.

  det_A = A.det()                 # Compute determinant of A.

  A_str = convert_mat_to_latex(A, align_opt='rrr')

  # Update old matrix
  A_html.value = 'Old matrix: <br><br>'                  \
    + r'$$ {\bf{A}} = \left [' + A_str + r'\right ]$$'    \
    + r'<br> $$\det {\bf{A}} = ' + f'{det_A}' + r'$$'

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
def apply_transpose(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Performs the transpose of the matrix when the button "transp_btn" is pressed.
  Updates the output of matrix A and B

  change:   dictionary holding information about the change of the button
            "transp_btn". This argument is used to be compatible with the button
            object but not involved in the code of this function.
  '''
#*******************************************************************************

  global A, B

  if (not is_started):

    A_html.value = \
      'Error. Please enter a matrix and press the start button.'

  else:

    B = A.T                               # Set B as the transpose.

    det_B = B.det()

    B_str = convert_mat_to_latex(B, align_opt='rrr')

    # Update new matrix
    B_html.value = 'New matrix: <br><br>'                   \
      + r'$$ {\bf{B}} = \left [' + B_str + r'\right ]$$'    \
      + r'<br> $$\det {\bf{B}} = ' + f'{det_B}' + r'$$'
  
  # End if. Started app verification.

#-------------------------------------------------------------------------------


#*******************************************************************************
def apply_swap(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Performs the swapping of two rows or two columns when the button "swap_btn" is
  pressed.  Updates the Sympy matrices A and B.

  change:   dictionary holding information about the change of the button
            "swap_btn". This argument is used to be compatible with the button
            object but not involved in the code of this function.
  '''
#*******************************************************************************

  global A, B

  id1 = int(swap_id1_drop.value)          # Read row or column indices.
  id2 = int(swap_id2_drop.value)

  if (not is_started):

    A_html.value = \
      'Error. Please enter a matrix and press the start button.'

  else:

    # Verify if the two row indices the same.

    if (id1 == id2):

      # If the indices are equal, create the error message, and do not call
      # the swapping function.

      B_html.value = 'Error. No rows or columns were swapped.'
    
    else: 

      # If the indices are different, call the swapping function.

      swap_opt = swap_radiobtn.value

      if swap_opt == 'columns':

        B = col_swap(A, id1, id2)

      else:

        B = row_swap(A, id1, id2)

      # End if. Rows or columns option.

      det_B = B.det()

      B_str = convert_mat_to_latex(B, align_opt='rrr')

      # Update new matrix
      B_html.value = 'New matrix: <br><br>'                   \
        + r'$$ {\bf{B}} = \left [' + B_str + r'\right ]$$'    \
        + r'<br> $$\det {\bf{B}} = ' + f'{det_B}' + r'$$'

    # End if. Verification different row or column indices.

  # End if. Started app verification.

#-------------------------------------------------------------------------------


#*******************************************************************************
def apply_row_or_col_times_scalar(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Performs the multiplication of a row times a scalar when the button "mult_btn"
  is pressed.  Updates the Sympy matrices A and B.

  change:   dictionary holding information about the change of the button
            "mult_btn". This argument is used to be compatible with the button
            object but not involved in the code of this function.
  '''
#*******************************************************************************

  global A, B

  rcid = int(mult_id_drop.value)          # Read row or column index.
  c    = parse_expr(mult_sc_tbox.value)   # Read scalar value.

  if (not is_started):

    A_html.value = \
      'Error. Please enter a matrix and press the start button.'

  else:

    # Verify if the constant is zero.

    if (str(c) == '0'):

      # If the constant is zero, create the error message, and do not call
      # the multiplication function.

      B_html.value = 'Error. The constant must not be zero. No operation '  \
        + 'was performed.'
    
    else: 

      # If the constant is not zero, call the multiplication function.

      mult_opt = mult_radiobtn.value

      if mult_opt == 'column':

        B = col_times_scalar(A, c, rcid)

      else:

        B = row_times_scalar(A, c, rcid)

      # End if. Rows or columns option.

    # End if. Verification constant different to zero.

    det_B = B.det()

    B_str = convert_mat_to_latex(B, align_opt='rrr')

    # Update new matrix
    B_html.value = 'New matrix: <br><br>'                   \
      + r'$$ {\bf{B}} = \left [' + B_str + r'\right ]$$'    \
      + r'<br> $$\det {\bf{B}} = ' + f'{det_B}' + r'$$'

  # End if. Started app verification.

#-------------------------------------------------------------------------------


#*******************************************************************************
def apply_row_or_col_add(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Performs the addition of two rows or two columns when the button "add_btn" is
  pressed.  Updates the Sympy matrices A and B.

  change:   dictionary holding information about the change of the button
            "add_btn". This argument is used to be compatible with the button
            object but not involved in the code of this function.
  '''
#*******************************************************************************

  global A, B

  id1  = int(add_id1_drop.value)          # Read row or column indices.
  id2  = int(add_id2_drop.value)
  c1   = parse_expr(add_sc_tbox.value)    # Read scalars that multiply row 1 and
  c2   = parse_expr('1')                  # row 2 before add them.

  if (not is_started):

    A_html.value = \
      'Error. Please enter a matrix and press the start button.'

  else:

    # Verify if the two row indices the same.

    if (id1 == id2):

      # If the indices are equal, create the error message, and do not call
      # the addition function.

      B_html.value = 'Error. The selection of rows for the addition is not '  \
        'valid. No operation was performed.'
    
    else: 

      # If the indices are different, call the addition function.

      add_opt = add_radiobtn.value

      if add_opt == 'columns':

        B = col_add(A, id2, c1, id1, c2, id2)

        op_str = r'(' + '{:s}'.format(str(c1)) + r'C_{:d}'.format(id1) + ' + ' \
          + r'C_{:d}'.format(id2) + r' \to ' + r'C_{:d}'.format(id2) + r')'

      else:

        B = row_add(A, id2, c1, id1, c2, id2)

        op_str = r'(' + '{:s}'.format(str(c1)) + r'R_{:d}'.format(id1) + ' + ' \
          + r'R_{:d}'.format(id2) + r' \to ' + r'R_{:d}'.format(id2) + r')'

      # End if.

    # End if.

    det_B = B.det()

    B_str = convert_mat_to_latex(B, align_opt='rrr')

    # Update new matrix
    B_html.value = 'New matrix: <br><br>'                   \
      + r'$$ {\bf{B}} = \left [' + B_str + r'\right ]$$'    \
      + r'<br> $$\det {\bf{B}} = ' + f'{det_B}' + r'$$'

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
  transp_btn.on_click(apply_transpose) 

  # Display all objects.
  display(all_inputs)     # Inputs.
  display(all_ctrls)      # Controls.
  display(transp_and_AB)  # Transpose controls, matrices A and B.

#-------------------------------------------------------------------------------


if __name__=='__main__':

  run_app()

# End if.
