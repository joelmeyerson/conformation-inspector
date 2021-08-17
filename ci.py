import os
import shutil
import argparse
import sys
import re
import matplotlib.pyplot as plt
from progress.bar import Bar

def main():
    
    # parse arguments
    parser = argparse.ArgumentParser(description='Analyze conformational compositions of protein particles in cryo-EM data.')
    parser.add_argument('-i', '--input', type=str, help='star file with symmetry expanded particles', required=True)
    #parser.add_argument('-c1', '--conformation1', type=str, help='star file with particles in subunit conformation 1', required=True)
    #parser.add_argument('-c2', '--conformation2', type=str, help='star file with particles in subunit conformation 2', required=True)
    #parser.add_argument('-c3', '--conformation3', type=str, help='star file with particles in undefined conformation(s)', required=True)
    #parser.add_argument('-s', '--symmetry', type=str, help='number of subunits', required=True)
    args = parser.parse_args()
    
    cnt = countpar(args.input)
    print(cnt)
    
# count number of particles in a star file
def countpar(starfile):
    
    count = 0
    with open(starfile, "r") as file:
        for line in file:
            if re.search(r'@', line): # this is a data entry which needs to be converted from array to tab-delimited string
                count += 1

    return count

if __name__ == "__main__":
    main()