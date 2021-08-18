import re
import matplotlib.pyplot as plt
from progress.spinner import Spinner

# get relevant metadata from sym.star
def par_meta(starfile, nsub):
    
    num_par_nx = 0 # total particle entries in sym.star
    num_par = 0 # total non-redundant particle entries in sym.star
    meta = []
    with open(starfile, "r") as file:
        
        # create progress spinner
        with Spinner('Reading metadata from ' + starfile + ' ') as spinner:
        
            for line in file:
                # check if line has particle and that column indexes have been found
                if (re.search(r'@', line) and img_col and x_col and y_col):            
                    if ((num_par_nx + nsub) % nsub == 0): # skip redundant lines in sym.star
                        parname = line.split()[img_col-1]
                        x = line.split()[x_col-1]
                        y = line.split()[y_col-1]
                        meta.append([parname, x, y, 0, 0, 0]) # final three list entries will be used to store subunit counts
                        if (num_par % 10000 == 0): # slow spinner
                            spinner.next()
                        num_par += 1
                    num_par_nx += 1
    
                # find header entry with column number for particle name
                elif re.search(r'_rlnImageName', line):
                    img_col = int(str(line.split()[1]).strip("#"))
        
                # find header entry with column number for particle name
                elif re.search(r'_rlnCoordinateX', line):
                    x_col = int(str(line.split()[1]).strip("#"))
        
                # find header entry with column number for particle name
                elif re.search(r'_rlnCoordinateY', line):
                    y_col = int(str(line.split()[1]).strip("#"))
        
    if len(meta) == 0:
        print("STAR file " + starfile + " is missing essential metadata or has no particles. Exiting.")
        exit()
    else:
        return [num_par_nx, num_par, meta]
		
# get relevant metadata from conformation star files
def sub_meta(starfile, nsub):
    
    num_par = 0 # total particle entries in star
    meta = []
    with open(starfile, "r") as file:
        
        # create progress spinner
        with Spinner('Reading metadata from ' + starfile + ' ') as spinner:
            
            for line in file:  
                # check if line has particle and that img column index has been found
                if (re.search(r'@', line) and img_col):
                    parname = line.split()[img_col-1]
                    meta.append(parname)
                    if (num_par % (nsub*10000) == 0): # slow spinner
                        spinner.next()
                    num_par += 1
                        
                # find header entry with column number for particle name
                elif re.search(r'_rlnImageName', line):
                    img_col = int(str(line.split()[1]).strip("#"))
        
    if len(meta) == 0:
        print("STAR file " + starfile + " is missing essential metadata or has no particles. Exiting.")
        exit()
    else:
        return [num_par, meta]