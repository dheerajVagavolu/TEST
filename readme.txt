To replicate the results:

1) Copy the "Doxyfile" and the "evol_stat.py" files into the root directory of the repository.

2) Install the required python dependencies. Matplotlib, Numpy, Doxygen etc. 

3) Run the python script with an integer argument.

 - example : 'python3 evol_stat.py 0' for call graph based approach
 
  or  'python3 evol_stat.py 1' for collaborative graph based approach.

4) Output is generated in the outs_test folded generated in the root directory.

5) The plot can be found in "outs_test> component_maps > out.png" directory
