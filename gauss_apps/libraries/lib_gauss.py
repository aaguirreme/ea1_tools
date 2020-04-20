# Name:         Gauss elimination library
# Description:  This library includes the functions required by different
#               applications based on the Gauss elimination method.
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
def col_swap(M, cid1, cid2):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Swap two columns of a SymPy matrix.

  M:    SymPy matrix to be modified.
  cid1: integer identificator of a column. One based (1, 2, ...).
  cid2: identificator of another column. One based (1, 2, ...).

  Returns a new matrix with swapped rows.
  '''
#*******************************************************************************
 
  ncols = M.cols            # Get the number of columns.

  if (cid1 == cid2):        # Verify if the swap is not valid
  
    print('Error. No columns were swapped.')

    new_M = M.copy()

  elif (cid1 > ncols) or (cid2 > ncols):

    print(f'Error. Please use col. indices from 1 through {nrows}.')

    new_M = M.copy()

  elif (cid1 == 0) or (cid2 == 0):
  
    print(f'Error. Please use row indices from 1 through {nrows}.')

    new_M = M.copy()

  else:

    # Create a list of indices.
    id_lst = [k for k in range(ncols)]    # Create a list of indices.

    id_lst[cid1 - 1] = cid2 - 1           # Swap indices in the list.
    id_lst[cid2 - 1] = cid1 - 1

    new_M = M[:,id_lst]                   # Reorganize matrix.

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
def col_add(M, new_cid, c1, cid1, c2, cid2):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Set new values for a column that are the linear combination of two existing
  columns.

  M:        SymPy matrix to be modified.
  new_cid:  integer identificator of the column to be modified. One based (1, 2,
            ...).
  c1:       real, scalar value to multiply column 1.
  cid1:     integer identificator of column 1. One based (1, 2, ...).
  c2:       real, scalar value to multiply column 2.
  cid2:     integer identificator of column 2. One based (1, 2, ...).
  '''
#*******************************************************************************

  new_M = M.copy()

  if (new_cid != cid1) and (new_cid != cid2):

    print(f'Error. The index of the new column is {new_cid}.')
    print(f'It must be either {cid1} or {cid2}.')

  else:
 
    new_M[:, new_cid - 1] = c1*M[:, cid1 - 1] + c2*M[:, cid2 - 1]

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
def col_times_scalar(M, c, cid):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Multiplies the column of a Sympy matrix times a scalar value.

  M:        SymPy matrix to be modified.
  c:        real, scalar value to multiply the row.
  cid:      integer identificator of the column. One based (1, 2, ...).
  '''
#*******************************************************************************

  new_M = M.copy()

  new_M[:, cid - 1] = c*M[:, cid - 1]

  return new_M

#-------------------------------------------------------------------------------


#*******************************************************************************
def generate_latex_string_per_row(row, color_str=''):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Convert the row of a matrix in Sympy format into LaTeX code. The code
  generated by this needs to be wrapped in an array LaTeX environment to work.

  row:        Sympy row of a matrix. Mutable dense matrix.
  color_str:  Optional. String containing the name of a color compatible with
              Jupyter/ipywidgets/Mathjax.
  '''
#*******************************************************************************

  ncols = len(row)

  latex_str = ''

  if color_str != '':

    for k in range(ncols):                      # Loop over row elements.

      latex_str += r'\color{{ {:s} }}{{ {:s} }}'.format(color_str, str(row[k]))

      if k < ncols - 1:                         # Add column separators.

        latex_str += ' & '

      # End if. Add column separator.

    # End for. Loop over row elements.

  else:

    for k in range(ncols):                      # Loop over row elements.

      latex_str += r'{:s}'.format(str(row[k]))

      if k < ncols - 1:                         # Add column separators 

        latex_str += ' & '

      # End if. Add column separator.

    # End for. Loop over row elements.

  # End if. Select case for the optional color argument.

  return latex_str

#-------------------------------------------------------------------------------


#*******************************************************************************
def convert_mat_to_latex(M, color_dict={0:'',1:'',2:''}, align_opt=""):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Convert a Sympy matrix to a LaTeX. It generates the code to print the
  augmented matrix used for the Gauss elimination process.

  M:              SymPy matrix to converted.
  color_dict:     A dictionary which keys are the row indices, and the values
                  are strings containing names of colors compatible with
                  Jupyter/ipywidgets/Mathjax. For example:
                  
                  color_dict = {
                    0:  'blue',
                    1:  'red',
                    2:  ''
                  }

  align_opt:      A string that tells the array LaTeX environment how to align
                  the columns of the array. For example, for a 4 column matrix,
                  
                  align_opt = 'rrr|r'

                  tells the array environment to align columns to the right, and
                  adds a vertical line between the 3rd and the 4th column.
  '''
#*******************************************************************************

  nrows = M.rows
 
  latex_str = r'\begin{array}' + r'{{ {:s} }}'.format(align_opt) + '\n'

  for k in range(nrows):

    row = M.row(k)

    row_color = color_dict[k]

    row_str = generate_latex_string_per_row(row, row_color)

    latex_str += row_str

    if k < nrows - 1:

      latex_str += r' \\'

    # End if. Add row separator.

    latex_str += '\n'

  # End for. Loop over rows of the matrix. 

  latex_str += r'\end{array}'

  return latex_str

#-------------------------------------------------------------------------------
