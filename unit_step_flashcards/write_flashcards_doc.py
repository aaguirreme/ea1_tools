
# User parameters
# ===============

# Number of plots.
N = 11

filename = 'flashcards_unit_step.tex'

preamble = r'''\documentclass[grid, poker_landscape]{flashcards}

\usepackage{graphicx}
\usepackage{mathrsfs}
\usepackage{breqn}

\cardfrontstyle[\Huge]{plain}
\cardbackstyle[\Huge]{plain}
'''

# Main script

# Write the preamble and open the document environment.
with open(filename, 'w') as fid:
    fid.write(preamble + '\n')
    fid.write(r'\begin{document}' + '\n\n')
# Close file.

# Write flashcards.
for k in range(1,N+1):

    with open(filename, 'a') as fid:
        fid.write(\
fr'''    %{k}
    \begin{{flashcard}}{{ \begin{{dmath*}} \input{{ example{k}.txt }} \end{{dmath*}} }}
        \includegraphics[width=8cm]{{example{k}unitstep.pdf}}
    \end{{flashcard}}
''')
        fid.write('\n')
    # Close file. 

# End for. Write flashcards.

# Write the statement to close the document environment.
with open(filename, 'a') as fid:
    fid.write(r'\end{document}')
# Close file.
