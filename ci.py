# main

import argparse
import re
import numpy as np
from collections import Counter
from progress.bar import Bar

# local imports
import get_meta
import gen_stats
import gen_pure_star

def main():
    
    # parse arguments
    parser = argparse.ArgumentParser(description='Analyze conformational compositions of protein particles in cryo-EM data.')
    parser.add_argument('-s', '--symexpand', type=str, help='star file with symmetry expanded particles', required=True)
    parser.add_argument('-c1', '--conformation1', type=str, help='star file with particles in subunit conformation 1', required=True)
    parser.add_argument('-c2', '--conformation2', type=str, help='star file with particles in subunit conformation 2', required=True)
    parser.add_argument('-n', '--numsubunits', type=int, help='number of subunits', required=True)
    parser.add_argument('-o', '--oligostar', type=str, help='star file with oligomers, used to to generate star files containing conformationally homogeneous ("pure") oligomers', required=False)
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
    data = np.empty([num_par, 3], dtype=int)
    dict_c1 = Counter(meta_c1)
    dict_c2 = Counter(meta_c2)

    # create progress bar
    with Bar('Tabulating subunit conformations for each oligomer', fill='-', suffix='%(percent)d%%', max=num_par) as bar:

        for i in range(num_par):
            parname = meta_par[i][0]
            cnt_c1 = dict_c1[parname]
            cnt_c2 = dict_c2[parname]
            cnt_other = num_sub - cnt_c1 - cnt_c2 # accounts for unclassified subunits in an oligomer

            if (cnt_c1 + cnt_c2 + cnt_other) != num_sub:
                print("Something went wrong in tabulating the conformations for " + parname + ". Exiting")
                exit()

            # update meta_par to hold the conformation counts
            data[i, 0] = cnt_c1
            data[i, 1] = cnt_c2
            data[i, 2] = cnt_other
            bar.next()

    # visualize output
    gen_stats.stats(data, num_sub)
    print("")

    # generate star files containing oligomers with pure C1 and C2
    # requires that user provide optional oligomer star file with -o option
    if args.oligostar:
        print("Writing star files with pure C1 and C2 oligomers.")
        print("")
        gen_pure_star.gen(dict_c1, args.oligostar, "pure_c1.star")
        print("File written for pure C1 oligomers (pure_c1.star)")
        print("")
        gen_pure_star.gen(dict_c2, args.oligostar, "pure_c2.star")
        print("File written for pure C2 oligomers (pure_c2.star)")
        print("")
    
    print("Finished.")

if __name__ == "__main__":
    main()