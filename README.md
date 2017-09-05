# ABM_media
Agent-Based-Modelling approach on the influence of the Internet and Social Media on opinion formation and vocalization.

The work consists of 4 python-files and 2 R-files:

Python:
- abm.py
- plotting_1000agents.py
- plotting_500agents.py
- exportToCSV.py

R:
- datapreparation.R
- analyses.R

Usage: 
- abm.py is used to define classes, run the model and save the information throughout to runs in .pkl files. 
- The two plotting files then load this information and procude meaningful plots.
- exportToCSV.py then exports the stored .pkl files to .csv files to be used in R.
- the R-Files then load the csv. files produced by exportToCSV.py and conduct descriptive analysies and linear models.
