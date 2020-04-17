# Changelog

## 2020-04-17

### Modified to Cramer's solver

- Added evaluated values of det(A_k) and det(A) to the output of solution.
- Minor changes to output HTMLMath objects to have fixed height and width
  defined in pixels.

## 2020-04-16

### Modified in Gauss tutorials

- Fixed a little mistake in the infinite solutions document. On the 3rd slide,
  the first paragraph should say "For convenience, divide the second row by
  -10".
- Added a new document for the "no solutions" case.
- Modified the notation used for the elementary row operations of the infinite
  solutions and unique solution documents to state clearly the row that is being
  modified. The green color is used to highlight such row.

### Modified to the Gauss calculator

- The row operations now state clearly the row that is being modified.

## 2020-04-15

### Added to the repository

- Gauss elimination tutorials. The folder contains LyX documents (and their LaTeX
  versions) of the step-by-step process of Gauss elimination of problems with
  unique solution and infinite number of solutions.

## 2020-04-14

### Modified to the Gauss calculator

- The default problem was modified with one that it's easier to solver using
  only integer operations.
- The app now includes a full operation history, instead of just showing the
  last operation. The HTMLMath object has now a fixed height of 300px, so a
  scroll bar appears after the content is too big to show inside the object.

## 2020-04-11

### Modified to the Gauss calculator

- The determinant of the coefficient matrix turns red if its value is equal to
  zero, which means that the system of equations does not have an unique
  solution.

### Added to the repository

- Cramer's rule interactive solver. A python notebook that computes the solution
  of a system of 3 equations with 3 unknowns using Cramer's rule.

## 2020-04-10

### Modified to the separation of variables notebook

- Minimum changes. Increased the width of the popupmenu to improve the
  visibility of the formulas. Also changed some mathematical equations to
  standard mode to improve their readability.

### Added to the repository

- Mathematica notebook on translation on the s-axis. Contains an interactive app
  that shows the original and shifted version of a Laplace transform. Includes a
  sliding bar to control the shifting constant.

## 2020-04-09

### Modified to the convolution notebook

- Minimum changes. Swapped the order of the Convolution and Partial Fraction
  options to make PF the 1st option and the default one. Also, most of the
  mathematical expressions are shown in standard mode (math-like) rather than in
  input mode (code).

## 2020-04-08

### Added to the repository

- First version of the Mathematica notebook on Convolution vs Partial Fractions.
  The notebook contains an interactive applications that shows the step by step
  process of computing the inverse Laplace transform of different functions
  using either convolution or partial fraction decomposition.

### Modified to the convolution notebook

- Modified the Convolution notebook to have a "radio button bar" instead of a
  checkbox field.

## 2020-04-02

### Modified to the README file

- Removed the initial webpage of the project from the README file. Added the
  link to the current Wix website.

### Modified to the Gauss Elimination Calculator

- The function update_aug_matrix now cleans the output of the elementary row
  operations. The function is activated by the start button.

## 2020-03-19

### Added to the repository

- Printable flashcards on translation on the s-axis. This flashcard set includes
  a color code that highlights on the basic laplace transforms due to s-shift.
  Under the same project, two LaTeX files generate the left and right-hand sides
  of the flashcards in PNG image format, to facilitate the creation of
  flashcards on online services.

## 2020-03-09

### Added to the repository

- Separation of variables step-by-step notebook. This project shows the
  step-by-step process of the separation of variables method using an
  interactive Wolfram Mathematica notebook.

### Modified to Separation of Variables Notebook.

- Removed integration calculations, and replaced with additional hard-coded
  expressions for the last step of the separation process. Also, the built-in
  exponential symbol was removed and replaced by the symbol "e".

## 2020-03-06

### Added to Laplace flashcards

- Version 6 of the TeX file, that changes the symbol of the unit-step function
  from the lowercase u letter to the uppercase cursive U letter.

### Added to the Unit Step Flashcards

- Version 5 of the Mathematica notebook. The new version provides option of
  exporting the plots as either PDF or PNG formats. Furthermore, the symbol of
  the unit-step function was changed from the lowercase u letter to the
  uppercase cursive U letter.

### Modified to Unit Step Flashcards

- The PDF document is now generated with the landscape orientation.

## 2020-02-24

### Added to the repository

- New project of unit-step function flashcards. The project combines Wolfram
  Mathematica, Python and LaTeX. The plots and the mathematical functions are
  generated in a Wolfram Mathematica notebook. Then, a Python script puts
  together a LaTeX file using the flashcards document class.

## 2020-02-20

### Modified to Laplace flashcards v4

- Uncommented flashcard of the Laplace transform of the unit step u(t - a).

## 2020-02-14

### Added to laplace_latex folder

- New version of the Laplace flashcards (v4). The new version has the size of
  Poker playing cards, and it is available in portrait and landscape
  orientations.

## 2020-02-07

### Added to the README file

- Link to a Desmos.com graph of the solution of a typical Newton's law of
  cooling IVP.

## 2020-02-05

### Added to the README file

- Link to a Desmos.com graph of the solution of a typical growth or decay IVP.

### Changed to the README file

- The Binder badge of the spring mass notebook was changed to a screenshot.
- The text hyperlink to compile the Laplace Transforms LaTeX document was
  replaced with a hyperlink that includes a screenshot.
- The Binder badge of the Gauss elimination notebook was changed to a
  screenshot.

## 2020-01-20

### Added to the repository

- First, second and third versions of Laplace transforms flashcards in LaTeX
  format.

### Added to the README file

- Links to compile the last version of the LaTeX Laplace transforms flashcards,
  and link to the source files.
- Binder badge of the spring-mass systems plots notebook.
- Hyperlink to the files of the spring-mass systems plots notebook.

## 2020-01-19

### Added to gauss_calc

- Section headers and minimal instructions for the notebook.
- Missing comments and docstrings to the library file "lib_gauss.py".

### Changed to gauss_calc

- Saved the status of the widgets in the notebook.

### Changed to the repository

- Moved the configuration file "requirements.txt" to a subfolder called "binder"
  for compatibility with mybinder.org.

### Added to the README file

- Binder badge of the Gauss elimination calculator notebook.
- Hyperlink to the files of the Gauss elimination calculator.
