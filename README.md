## Conformation Inspector
The purpose of the script is to visualize statistics on the conformational composition of protein homo-oligomers in cryo-EM data. Particles must be processed by symmetry expansion to generate masked images of each protein subunit from every particle in the dataset. The subunits must then be subjected to 3D conformational classification to identify the conformation of each subunit image. The script uses the resulting conformational assignments for the protein subunits to determine the conformational composition of each protein homo-oligomer.

### File inputs
The script assumes there are two interpretable subunit conformations (C1 and C2) and a third subunit conformation that is not interpretable but must be accounted for in the analysis (C3).

`sym.star` STAR file with symmetry expanded particles
`c1.star` STAR file with particles for conformation 1.
`c2.star` STAR file with particles for conformation 2.
`c3.star` STAR file with other particles that are not assigned to conformation 1 or 2.

### Conda environment
Quick setup for a conda environment to run the script.

`conda create -n ci` # create environment
`conda install -n ci matplotlib progress` # install packages
`conda activate ci` # activate environment

### Running the script
Command to run the script with file inputs and the number of subunits specified. In this example the number of subunits is four. The output is `out.png` and is written to the user working directory.

`python ci.py -i sym.star -c1 c1.star -c2 c2.star -c3 c3.star -n 4`



