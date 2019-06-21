# Predictig Molecular Properties Challenge

This repository contains the solution for the [Predicting Molecular Properties](https://www.kaggle.com/c/champs-scalar-coupling/overview) challenge on Kaggle.

## Challenge Summary
The objective of the challenge was to predict the J-coupling between two atoms in a molecule. This J-coupling quantifies the magnetic interaction between the atoms. 

The data provided for the challenge was the structure of the molecule in which the atoms are located. I parsed this molecular structured from XYZ  files that contained the atom types and the positions in the molecule. An example of an XYZ file can be found [here](http://paulbourke.net/dataformats/xyz/).

## Approach

The approach I followed for the challenge was to create features from the molecular structures. 



## How to Run

First, make sure that you have [conda](https://docs.conda.io/en/latest/) installed and install the project.

```shell
conda create -n MagneticInteractionsChallenge
pip install -e 'git+https://github.com/cmpatino/MagneticInteractionsChallenge.git#egg=magnetic_interactions'
```

> For a private repository accessible only through an SSH authentication, substitute `git+https://github.com` with `git+ssh://git@github.com`.