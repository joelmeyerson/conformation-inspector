import re
from progress.spinner import Spinner

# build star file with conformational "pure" oligomers
def gen(dict_cx, oligostar, outstar):
    
    star_header = [] # store header
    star_lines = [] # star lines with particles
    in_header = True
    img_col = 0
    
    with open(oligostar, "r") as file:
        
        # extract header
        for line in file:
        
            # monitor for when exit header block
            if re.search(r'@', line) and in_header == True:
                in_header = False
                    
            if in_header == True:
                star_header.append(line)

                # find header entry with column number for particle name
                if re.search(r'_rlnImageName', line):
                    img_col = int(str(line.split()[1]).strip("#"))
                    
            # if line has particle, and not in header, and that particle image index has been found
            elif re.search(r'@', line) and in_header == False and img_col:
                star_lines.append(line)
        
        # get list of oligomer images with "pure" composition
        pure = []
        for key, value in dict_cx.items():
            if value == 4:
               pure.append(key) 
        
        # find entries in oligomer star that match entries in the conformation star
        matches = []
        with Spinner('Generating ' + outstar + ' ') as spinner:
            for i in range(len(star_lines)):
            
                par_img = star_lines[i].split()[img_col - 1]
                if par_img in pure:
                    matches.append(star_lines[i])
                
                if (i % 10000 == 0): # slow spinner
                    spinner.next()
            
        # write star file output
        with open(outstar, "w") as starfile:
            starfile.writelines("%s" % l for l in star_header)
            starfile.writelines("%s" % l for l in matches)
            