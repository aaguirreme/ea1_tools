# Name:         Cramer's rule interactive solver
# Description:  This library includes the functions required by the Cramer's
#               rule interactive solver to work.
# Author:       Andres M. Aguirre-Mesa
#               PhD student, Mechanical Engineering.
#               University of Texas at San Antonio.
# Date:         April 11, 2020.


#*******************************************************************************
#                        Import libraries and functions
#*******************************************************************************

import sympy as sym

from sympy.parsing.sympy_parser import parse_expr

from ipywidgets import Layout, Text, HTML, HTMLMath, Box, HBox, VBox, Button, \
  Dropdown

from lib_linalg import gen_text_grid

#*******************************************************************************
#           Global variables definition and notebook initialization
#*******************************************************************************

# NOTE: These commands are executed when the library is imported.

# Define initial values for the coefficient matrix A.
A = sym.Matrix([[ 1,  1, -1],
                [ 3,  1,  1],
                [ 1, -1,  4]])

# Define initial values for the constant (right hand side) matrix B.
B = sym.Matrix([ 3, 9, 8])

is_started = False

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

# Create a description for the RHS (right hand side) vector.
rhs_text = HTMLMath(
  value=r'Enter here the values of the constant matrix $\bf{B}$',
  layout=Layout(width='90px') ) 

rhs_values = gen_text_grid(len(B), 1, cell_layout, '45px')

for i in range(len(B)):
  rhs_values.children[i].value = str(B[i])
# End for.

# Put together description and values of the matrix.
rhs_input = HBox([rhs_values, rhs_text], layout=Layout(width='150px',
  height='120px'))

# Create a text to describe the function of the start button.
start_text = HTML(
  value='Click this button to start or reset the app.',
  layout=Layout(width='140px') )

start_btn = Button(description='Start')          # Create a start button.

# Put together description and button.
start_input = VBox( [start_text, start_btn]) 

# Create a HTML object to show the augmented equation in LaTeX format.
eq_latex = HTMLMath(
  value=r'The matrix $\bf{A}$ and the vector $\bf{B}$ will appear here.',
  layout=Layout(justify_content='center', height='120px', width='300px'))

# Put together all inputs.
all_inputs = Box( [mat_input, rhs_input, start_input, eq_latex], 
  layout=Layout(justify_content='space-around', flex_flow='row wrap') )

# Controls

# Create a text to describe the function of the start button.
var_text = HTML(
  value='Choose a variable to solve for.',
  layout=Layout(width='140px') )

var_drop = Dropdown( options=['x\u2081', 'x\u2082', 'x\u2083'], value='x\u2081',
  description='Variable:', layout=Layout(width='150px') )
 
var_btn = Button(description='Solve')
 
var_ctrl = VBox( [ var_text, var_drop, var_btn ] )

# Outputs

# Create a HTML object to show results in LaTeX format.
results_html = HTMLMath(value='Results will be shown here.', 
  layout=Layout(justify_content='center', height='250px', width='400px'))

# Put together all controls
other_widgets = Box( [var_ctrl, results_html], 
  layout=Layout(justify_content='space-around', flex_flow='row wrap') )


#*******************************************************************************
#                             Function definitions
#*******************************************************************************


#*******************************************************************************
def create_Ak(A,B,k):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Create the matrix A1, A2 or A3 of the Cramer's rule method.
  
  A:   Matrix of coefficients A.
  B:   Vector of independent terms B.
  k:   Column index to create A_k.
  '''
#*******************************************************************************

  if k == 1:

    Ak = B.row_join(A[:,1:])
    
  elif k == 2:
    
    Ak = A[:,0].row_join(B.row_join(A[:,2]))
    
  elif k == 3:
    
    Ak = A[:,:2].row_join(B)
    
  # End if.

  return Ak

#-------------------------------------------------------------------------------


#*******************************************************************************
def apply_cramer(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Create the matrix A1, A2 or A3 of the Cramer's rule method.
  
  A:   Matrix of coefficients A.
  B:   Vector of independent terms B.
  k:   Column index to create A_k.
  '''
#*******************************************************************************

  k_dict = {
    'x\u2081': 1,
    'x\u2082': 2,
    'x\u2083': 3
  }

  k = k_dict[var_drop.value]          # Read row index.
  
  detA = sym.det(A)
 
  if (not is_started):

    results_html.value = \
      'Error. Please enter the system of equations and press the start button.'
    
  elif detA == 0:
    
    results_html.value = \
      'Error. The system does not have a unique solution.'

  else:

    Ak = create_Ak(A,B,k)             # Build matrix A_k
    
    detA = sym.det(A)                 # Compute determinant of A.
    
    detAk = sym.det(Ak)               # Compute determinant of A_k.
    
    xk = detAk/detA                   # Find the value of the variable x_k.
  
    latex_str = \
      r'$$'   + r' \color{green}{\det A} = '  + r'\left|'                     \
      + convert_mat_to_latex(A,0)             + r'\right| = '                 \
      + f'\color{{green}}{{ {detA}}}'         + r'$$ <br>'                    \
      + r'$$' + f' \color{{red}}{{ \det A_{k} }} = ' + r'\left|'              \
      + convert_mat_to_latex(Ak,k)            + r'\right| = '                 \
      + f'\color{{red}}{{ {detAk} }}'         + r'$$ <br>'                    \
      + f'$$ x_{{ {k} }} =' + r'\frac{ \color{red}{\det A_' + f'{k}' + r'}}'  \
      + r'{\color{green}{ \det A }}'                                          \
      + r' = \frac{ \color{red}{' + f'{str(detAk)}' + r'}}'                   \
      + r'{\color{green}{'        + f'{str(detA)}'  + r'}}'                   \
      + f' = {xk}' + r'$$'
    
    results_html.value = latex_str
  
  # End if.

#-------------------------------------------------------------------------------


#*******************************************************************************
def convert_mat_to_latex(M,k):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Convert a Sympy 3x3 matrix to a LaTeX. It generates the code to print the 
  matrix surrounded by braces.

  M:        SymPy matrix to be printed.
  '''
#*******************************************************************************

  if k == 1:
    
    latex_str = r''' 
      \begin{{array}}{{rrr}}
          \color{{blue}}{{ {:s} }} & {:s} & {:s}\\
          \color{{blue}}{{ {:s} }} & {:s} & {:s}\\
          \color{{blue}}{{ {:s} }} & {:s} & {:s}
      \end{{array}}
      '''
    
  elif k == 2:
    
    latex_str = r''' 
      \begin{{array}}{{rrr}}
          {:s} & \color{{blue}}{{ {:s} }} & {:s}\\
          {:s} & \color{{blue}}{{ {:s} }} & {:s}\\
          {:s} & \color{{blue}}{{ {:s} }} & {:s}
      \end{{array}}
      '''
    
  elif k == 3:
    
    latex_str = r''' 
      \begin{{array}}{{rrr}}
          {:s} & {:s} & \color{{blue}}{{ {:s} }}\\
          {:s} & {:s} & \color{{blue}}{{ {:s} }}\\
          {:s} & {:s} & \color{{blue}}{{ {:s} }}
      \end{{array}}
      '''
    
  else:
    
    latex_str = r''' 
      \begin{{array}}{{rrr}}
          {:s} & {:s} & {:s}\\
          {:s} & {:s} & {:s}\\
          {:s} & {:s} & {:s}
      \end{{array}}
      '''
    
  # End if.
    

  latex_str = latex_str.format(
    str(M[0,0]), str(M[0,1]), str(M[0,2]),
    str(M[1,0]), str(M[1,1]), str(M[1,2]),
    str(M[2,0]), str(M[2,1]), str(M[2,2]))

  return latex_str

#-------------------------------------------------------------------------------


#*******************************************************************************
def convert_vec_to_latex(V):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Convert a Sympy 3x1 vector to a LaTeX. It generates the code to print the 
  matrix surrounded by braces.

  V:        SymPy vector to be printed.
  '''
#*******************************************************************************

  latex_str = r''' 
    \begin{{array}}{{r}}
        {:s} \\
        {:s} \\
        {:s} 
    \end{{array}}
    '''

  latex_str = latex_str.format(
    str(V[0,0]),
    str(V[1,0]),
    str(V[2,0]))

  return latex_str

#-------------------------------------------------------------------------------


#*******************************************************************************
def update_system(change):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Transfer the system of equations contained in different input text boxes
  (A11_tbox, A12_tbox, ..., B1_tbox, B2_tbox, etc) to the output HTMLMath object
  "eq_latex". This function is activated by the button "start_btn".

  change:   dictionary holding the information about the change of the button
            "start_btn". This argument is used to be compatible with the button
            object but not involved in the code of this function.
  '''
#*******************************************************************************

  global is_started, M, M_0, M_old
  
  is_started = True

  for i in range(A.rows):
    for j in range(A.cols):
      A[i,j] = parse_expr(mat_values.children[A.rows*i + j].value)
    # End for. Loop over columns
  # End for. Loop over rows.

  for i in range(len(B)):
    B[i] = parse_expr(rhs_values.children[i].value)
  # End for. Loop over rows.

  detA = A.det()      # Compute determinant.

  if detA == 0:
    
    detA_str = r'$\color{red}{ \det A =' + f'{detA}' + r'}$'
  
  else:
  
    detA_str = r'$\det A =' + f'{detA}' + r'$'
    
  # End if.
    
  # Create the string with the initial augmented matrix in LaTeX format.
  latex_str = r'$$ \mathbf{A} = \left[ ' + convert_mat_to_latex(A,0) + \
    r', \right] \quad \color{blue}{\mathbf{B} = \left[' + \
    convert_vec_to_latex(B) + r'\right]}$$' + \
    '<br>with ' + detA_str + '.' 
  
  # Update object "eq_latex" with the augmented matrix in LaTeX format. 
  eq_latex.value=latex_str

  # Clear the contents of the results_html output.
  results_html.value = '' 

#-------------------------------------------------------------------------------


#*******************************************************************************
def run_app():
#*******************************************************************************

  start_btn.on_click(update_system)           # Define the function associated
  var_btn.on_click(apply_cramer)             # with each button.

  # Display all objects.
  display(all_inputs)         # Inputs.
  display(other_widgets)      # Controls and output.

#-------------------------------------------------------------------------------


if __name__=='__main__':

  run_app()

# End if.
