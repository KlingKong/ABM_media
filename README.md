# ABM_media
Agent-Based-Modelling approach on the influence of the Internet and Social Media on opinion formation and vocalization.

The work consists of 4 python-files and one R-file:

Python:
- abm.py
- plotting_1000agents.py
- exportToCSV.py
- extremists.py

R:
- analyses.R

Usage: 
- abm.py is used to define classes, run the model and save the information throughout the runs in .pkl files. 
- The plotting file then load this information and procude meaningful plots.
- exportToCSV.py then exports the stored .pkl files to .csv files to be used in R.
- extremists.py extracts information about extreme opinion holders and exports them to a .csv file to load in R.
- the R-File then load the .csv files produced by exportToCSV.py and conduct descriptive analysies and linear models.
