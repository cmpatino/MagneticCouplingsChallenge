# Data

The data provided for this challenge has several files. Below is a description of the information contained in every file. 

## train.csv
+ `molecule_name`: The name of the molecule where the coupling constant originates.
+ `atom_index_0` and `atom_index_1`: Indices of the atoms creating the magnetic coupling.
+ `scalar_coupling_constant`: Scalar coupling constant that has to be predicted.

## test.csv 

Contains the same information as train.csv without the `scalar_coupling_constant`.

## structures.zip

Folder containing the molecular structure for each molecule in the train and test files. The first line in one file has the number of atoms in the molecule. The second line is a blank line followed by lines with the information about the atom. Each line contains the atomic element and the XYZ coordinates of the atom. 

## Additional Information

There is additional information provided only for the molecules used for training.

+ **dipole_moments.csv**: contains the information about the XYZ components of the 3D dipole moment vector
+ **magnetic_shielding_tensors.csv**: contains the magnetic shielding tensors for each of the molecules. 
    + `molecule_name`: molecule name
    + `atom_index`: contains the index of the atom in the molecule
    + columns 3-11: XX, XX, YX, ZX, XY, YY, ZY, XZ, YZ and ZZ elements of the tensor/matrix.
+ **mulliken_charges.csv**: contains the mulliken charge for all the atoms in the molecule
+ **potential_energy.csv**: contains the potential energy of the entire molecule
+ **scalar_coupling_contributions.csv**: The scalar coupling is the result of the four contributions contained in this file.
    + **fc**: Fermi contact coupling
    + **sd**:spin-dipolar contribution
    + **pso**: Parametric spin-orbit contribution
    + **dso**: Diamagnetic spin-orbit contribution