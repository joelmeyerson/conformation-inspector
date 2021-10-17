## Conformation Inspector
The purpose of the script is to generate statistics on the conformational composition of protein homo-oligomers in cryo-EM data. Particles must be processed by symmetry expansion to generate masked images of each protein subunit from every particle in the dataset. The subunit images must then be subjected to 3D conformational classification to identify the conformation of each subunit image. The script uses the resulting conformational assignments for the protein subunits to determine the conformational composition of each protein homo-oligomer. It will work for any homo-oligomer (subunits N > 1). The script was tested using results generated with Relion.

### File inputs
The script assumes there are two interpretable subunit conformations (C1 and C2). These two subsets need not sum to the total number of subunits in the dataset. This allows for a third subset of subunits that may represent an uninterpretable conformation or conformations. The script will automatically handle any subunits which are not accounted for in C1 and C2.

`sym.star` STAR file with symmetry expanded particles.

`c1.star` STAR file with particles for conformation 1.

`c2.star` STAR file with particles for conformation 2.

Optionally, the parent oligomer star file can be provided and it will be used to generate new star files for the subset of oligomers that have "pure" C1 and C2 conformations. For example, if the oligomer is a trimer this option will return all trimers that have three C1 subunits (`pure_c1.star`), and all trimers that have three C2 subunits (`pure_c2.star`).

`oligomer.star` STAR file with oligomer particles (typically the input used during symmetry expansion).

### Conda environment
Quick setup for a conda environment to run the script.

`conda create -n ci` # create environment

`conda install -n ci numpy progress` # install packages

`conda activate ci` # activate environment

### Running the script
Command to run the script with file inputs and the number of subunits per protein specified. In this example the number of subunits is four. The results are printed to the console.

`python ci.py -n 4 -i sym.star -c1 c1.star -c2 c2.star`

If running with the option to generate "pure" STAR files.

`python ci.py -n 4 -i sym.star -c1 c1.star -c2 c2.star -o oligomer.star`