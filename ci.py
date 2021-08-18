import argparse
import re
import matplotlib.pyplot as plt

# local imports
import get_meta

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
    [num_par_nx, num_par, meta_par] = get_meta.par_meta(args.symexpand, num_sub)
    
    # make lists for subunits in c1 and c2
    [num_par_c1, meta_c1] = get_meta.sub_meta(args.conformation1, num_sub)
    [num_par_c2, meta_c2] = get_meta.sub_meta(args.conformation2, num_sub)
    
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

if __name__ == "__main__":
    main()