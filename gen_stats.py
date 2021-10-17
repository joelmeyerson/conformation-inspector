import numpy as np

def stats(data, num_sub):
   
    num_par = data.shape[0] # number of protein oligomers
    num_c1 = sum(data[:,0]) # number of subunits in conformation 1
    num_c2 = sum(data[:,1]) # number of subunits in conformation 2
    num_o = sum(data[:,2]) # number of subunits in undefined 'other' conformation
    
    # each element in array stores a possible protein conformational composition
    # (e.g. for a tetramer: element 0 will map to 0:4 c1:c2, element 1 will map to 1:3 c1:c2, etc)
    stats = np.zeros([num_sub + 1], dtype=int)
    c1_tot = 0
    c2_tot = 0
    for row in data:
        
        if row[2] > 0: # skip protein if one or more subunits are undefined
            pass
        else:
            c1_cnt = row[0] # number of c1 conformations used to define an array index
            stats[c1_cnt] = stats[c1_cnt] + 1
            c1_tot += row[0]
            c2_tot += row[1]
            
    # print results
    print('')
    print('Results:')
    print('Subunits in analysis (#): ' + f"{(num_par * num_sub):,}")
    print('Subunits identified as C1 (#): ' + f"{(num_c1):,}")
    print('Subunits identified as C2 (#): ' + f"{(num_c2):,}")
    print('Subunits not assigned an identity (#): ' + f"{((num_par * num_sub) - num_c1 - num_c2):,}")
    print('')
    print('Protein oligomeric state (#): ' + str(num_sub))
    print('Protein oligomers (#): ' + f"{(num_par):,}")
    print('Protein oligomers with one or more unclassified subunit(s) (#): ' + f"{(num_par - sum(stats)):,}" + ' [excluded from analysis]')
    
    oligo = f"{(sum(stats)):,}"
    sub  = f"{(sum(stats) * num_sub):,}"
    c1 = f"{(c1_tot):,}"
    c1_frac = f"{round( ((c1_tot/(sum(stats) * num_sub))*100), 2):,}"
    c2 = f"{(c2_tot):,}"
    c2_frac = f"{round( ((c2_tot/(sum(stats) * num_sub))*100), 2):,}"
    
    print('Protein oligomers with all subunits classified (#): ' + oligo + ' [total subunits included: ' + sub + '; C1 subunits: ' + c1 + ' (' + c1_frac +'%); C2 subunits: ' + c2 + ' (' + c2_frac +'%)]')
    print('')
    print('C1:C2 ratios:')
    
    for i in range(len(stats)):
        ratio = str(i) + ':' + str(num_sub-i)
        percent = (stats[i] / sum(stats))*100
        percent = str(round(percent, 2))
        result = ratio + ' => ' + f"{(stats[i]):,}" + ' oligomers (' + percent + '%)'
        print(result)