import argparse
import re
import matplotlib.pyplot as plt
from progress.spinner import Spinner

def main():
    
    # parse arguments
    parser = argparse.ArgumentParser(description='Analyze conformational compositions of protein particles in cryo-EM data.')
    parser.add_argument('-s', '--symexpand', type=str, help='star file with symmetry expanded particles', required=True)
    parser.add_argument('-c1', '--conformation1', type=str, help='star file with particles in subunit conformation 1', required=True)
    parser.add_argument('-c2', '--conformation2', type=str, help='star file with particles in subunit conformation 2', required=True)
    parser.add_argument('-n', '--numsubunits', type=int, help='number of subunits', required=True)
    args = parser.parse_args()
    
    # make list with particle oligomer name, x coordinate, y coordinate, and make list entries to store subunit counts
    num_sub = args.numsubunits
    [num_par_nx, num_par, meta_par] = get_par_meta(args.symexpand, num_sub)
    
    # make lists for subunits in c1 and c2
    [num_par_c1, meta_c1] = get_sub_meta(args.conformation1, num_sub)
    [num_par_c2, meta_c2] = get_sub_meta(args.conformation2, num_sub)
    
    # confirm that particle and subunit counts make sense
    if num_par_nx / num_par != num_sub:
        print("The number of particles in " + args.symexpand + " is not a multiple of " + str(num_sub) +". Exiting.")
        exit()
    
    if (num_par_c1 > num_par_nx or num_par_c2 > num_par_nx):
        print("The number of particles in each of the subunit conformation STAR files should be fewer than the number of particles in the symmetry expanded STAR file. Exiting.")
        exit()

    if (num_par_c1 + num_par_c2) > num_par_nx:
        print("The number of total subunit conformation particles exceeds the number of symmetry expanded particles. Exiting.")
        exit()
    
    # tabulate the conformations for each protein oligomer
    #iterate through meta_par
    #for each entry count the number of instances in meta_c1 and meta_c2
    #check that they sum to 4, if not mark the final column in meta_par
    
    # visualize output
    #make table
    #total particles and subunits
    #num in c1, c2, and other
    #num tetramers with 4, 3, 2, and 1 subunits assigned
    #for tetramers with all four subunits, plot histogram showing their distribution
    
# get relevant metadata from sym.star
def get_par_meta(starfile, nsub):
    
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
            
# get relevant metadata from sym.star
def get_sub_meta(starfile, nsub):
    
    num_par = 0 # total particle entries in star
    meta = []
    with open(starfile, "r") as file:
        
        # create progress spinner
        with Spinner('Readingmeta data from ' + starfile + ' ') as spinner:
            
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

if __name__ == "__main__":
    main()