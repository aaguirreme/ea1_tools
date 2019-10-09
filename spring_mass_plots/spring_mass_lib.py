# Name:         Spring Mass Library
# Description:  This library includes the functions required by the Spring Mass
#               Notebook to work.
# Author:       Andres M. Aguirre-Mesa
#               PhD student, Mechanical Engineering.
#               University of Texas at San Antonio.
# Date:         June 10, 2019.
# Update:       June 18, 2019.


#*******************************************************************************
#                        Import libraries and functions
#*******************************************************************************


import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import sympy as sym

from sympy import S


#*******************************************************************************
#                  Code to run during import of this library
#*******************************************************************************


fig, ax = plt.subplots(1);          # Initialize plot window


#*******************************************************************************
#                             Function definitions
#*******************************************************************************


#*******************************************************************************
def get_damping_case(m, c, k, tol=1e-5):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Determine the damping case of a free damped spring mass system, depending on
  the values of the mass, the damping constant, and the spring constant.
  
  m:    Mass. Real number.
  c:    Damping constant. Real number.
  k:    Spring constant.  Real number.
  tol:  Tolerance value used to evaluate the critically damped case using
        floating point numbers. Real number.

  Returns a string that describes the damping case.
  '''
#*******************************************************************************

  disc = (c/m)**2 -4*(k/m)        # Compute discriminant.

  if (c == 0):
    case ='Simple harmonic (undamped)'
  elif (disc > 0):
    case ='Overdamped'
  elif ( abs(disc) < tol ):
    case ='Critically damped'
  else:
    case ='Underdamped'
  # End if.

  return case

#-------------------------------------------------------------------------------


#*******************************************************************************
def solve_spring_mass_ode(m, c, k, x0, xp0):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Solve the initial value problem of a 2nd order ordinary differential equation
  of a free damped spring mass system, provided the initial position and the
  initial velocity, and returns the specific solution as a function f(t).

  m:    Mass. Real number.
  c:    Damping constant. Real number.
  k:    Spring constant.  Real number.
  x0:   Initial position of the mass. Real number.
  xp0:  Initial velocity of the mass. Real number.

  The returned function can be evaluated numerically. It is created using the
  lambdify function of SymPy.
  '''
#*******************************************************************************

  ms   = S(m)                     # Convert real numbers to sympy format.
  cs   = S(c)                     # This is required to be able to print
  ks   = S(k)                     # the equation using a defined number of 
  x0s  = S(x0)                    # decimal places for the numerical values.
  xp0s = S(xp0)

  t = sym.Symbol('t', real=True)  # Define t as symbol and
  x = sym.Function('x')           # x as function.

  C1, C2 = sym.symbols('C1 C2')   # Def. symbols for the integration constants.

  w = sym.sqrt(ks/ms)             # Angular frequency.
  a = -S(1)/S(2)*(cs/ms)          # Constant for cases with damping.

  disc = (c/m)**2 -4*(k/m)        # Compute discriminant.

  ## The function dsolve of SymPy can be used to solve the ODE. However, it was
  ## very slow and failed certain input parameter combinations. 
  #
  ## Define the ODE.
  #Eq1 = sym.Eq( ms*sym.diff(x(t), t, 2) + cs*sym.diff(x(t), t) + ks*x(t), 0)
  #
  ## Solve the ODE.
  #f_gen = sym.dsolve(Eq1, x(t)).rhs
 
  # Compute general solution. Initial conditions are not applied yet). This
  # solution is in terms of the constants C1 and C2. Extract the right hand side
  # only.

  # NOTE: the general solution for each case is provided here, instead of
  #       solving the ODE using the function dsolve of SymPy.

  if (c == 0):          # Undamped.

    f_gen = C1*sym.cos(w*t) + C2*sym.sin(w*t)

  elif (disc < 0):      # Underdamped.

    b = sym.sqrt(ks/ms - ( S(1)/S(2)*(cs/ms) )**S(2))

    f_gen = sym.exp(a*t)*( C1*sym.cos(b*t) + C2*sym.sin(b*t) )

  elif (disc == 0):     # Critically damped.
    
    f_gen = sym.exp(a*t)*( C1 + C2*t )

  else:                 # Overdamped.
    
    b = sym.sqrt( ( S(1)/S(2)*(cs/ms) )**S(2) - ks/ms )
    
    f_gen = sym.exp(a*t)*( C1*sym.exp(b*t) + C2*sym.exp(-b*t)  )

  # End if.

  cond0 = sym.Eq(f_gen.subs(t, S(0)), x0)              # Define initial 
  cond1 = sym.Eq(f_gen.diff(t).subs(t, S(0)), xp0)     # conditions.

  # Solve for C1, C2
  sol_C1C2 = sym.solve([cond0, cond1], (C1, C2))

  # Substitute C1 and C2 back into the general solution to compute the equation
  # of motion. This is the specific solution.
  f_esp = sym.simplify(f_gen.subs(sol_C1C2))

  return f_esp

#-------------------------------------------------------------------------------


#*******************************************************************************
def update_plot(m=1, c=2, k=4, x0=1, xp0=1, tmax=5, xmin=-2, xmax=2):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Solve the ODE of a free damped spring mass system, and show a plot of the
  equation of motion.

  m:    Mass. Real number.
  c:    Damping constant. Real number.
  k:    Spring constant.  Real number.
  x0:   Initial position of the mass. Real number.
  xp0:  Initial velocity of the mass. Real number.
  tmax: Maximum time of the plot. Real number.
  xmin: Minimum range value for displacement. Real number.
  xmax: Maximum range value for displacement. Real number.
  '''
#*******************************************************************************

  ax.clear()                            # Remove previous plot. 

  # Solve the ODE using the updated parameters.
  f_sym = solve_spring_mass_ode(m, c, k, x0, xp0)  

  # Convert symbolic equation to numerical function f(t).
  f = sym.lambdify(sym.Symbol('t'), f_sym)
  
  t_array = np.linspace(0., tmax)       # Create an array of time values.
  x_array = f(t_array)                  # Compute disp. values using f(t).

  damping = get_damping_case(m, c, k)   # Determine damping case.

  ax.plot(t_array, x_array)             # Update plot.
  ax.set_xlabel('Time $t$')
  ax.set_ylabel('Displacement $x$')
  ax.set_ylim([xmin,xmax])
  ax.text(0.9, 0.9, damping, horizontalalignment='right', transform=ax.transAxes)
  ax.grid(True)
  plt.show()

#-------------------------------------------------------------------------------


#*******************************************************************************
def run_app():
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  '''
  Main function that contains the script to be executed in a Jupyter notebook.
  '''
#*******************************************************************************

  slider = widgets.FloatSlider    # Define a local alias for the slider obj.

  # Create widgets.

  # Mass.
  m_slider    = slider(value=1, min=0.1, max=10, step=0.1,
                       description='$m$:', readout_format=' .2f')
  c_slider    = slider(value=2, min=0,   max=10, step=0.1,
                       description='$c$:', readout_format=' .2f')
  k_slider    = slider(value=4, min=0,   max=10, step=0.1,
                       description='$k$:', readout_format=' .2f')
  x0_slider   = slider(value=1, min=0,   max=10, step=0.1,
                       description='$x(0)$:', readout_format=' .2f')
  xp0_slider  = slider(value=1, min=0,   max=10, step=0.1,
                      description='$x\'(0)$:', readout_format=' .2f')
  tmax_slider = slider(value=5, min=4,   max=10, step=0.1,
                       description='$t_\\mathrm{max}$:', readout_format=' .2f')
  xmin_slider = slider(value=-2, min=-5,   max=0, step=0.1,
                       description='$x_\\mathrm{min}$:', readout_format=' .2f')
  xmax_slider = slider(value=2, min=0,   max=5, step=0.1,
                       description='$x_\\mathrm{max}$:', readout_format=' .2f')

  # Make the function update_plot interactive, and assign its input values
  # using the sliders.
  w = widgets.interactive(update_plot, m=m_slider, c=c_slider, 
      k=k_slider, x0=x0_slider, xp0=xp0_slider, tmax=tmax_slider,
      xmin=xmin_slider, xmax=xmax_slider)

  # Group the sliders in a single controls object.
  controls = \
    widgets.HBox([ \
      widgets.VBox([m_slider, c_slider, k_slider, x0_slider, xp0_slider]),
      widgets.VBox([tmax_slider, xmin_slider, xmax_slider]) ])
  
  update_plot()           # Run the function update_plot once.
  
  display(controls)       # Show controls.

#-------------------------------------------------------------------------------

