# MagneticInteractionsChallenge

This repository contains the solution for the [Predicting Molecular Properties](https://www.kaggle.com/c/champs-scalar-coupling/overview) challenge on Kaggle.

## Challenge Summary
The objective of the challenge was to predict the J-coupling between two atoms in a molecule. This J-coupling quantifies the magnetic interaction between the atoms. 

There were eight types of J-couplings for the challenge:
+ 1JHC
+ 1JHN
+ 2JHH
+ 2JHC
+ 2JHN
+ 3JHH
+ 3JHC
+ 3JHN

The nomenclature followed for the coupling types indicates the coupling order and the atom types of the coupled pair. 

The data provided for the challenge was the structure of the molecule in which the atoms are located. I parsed this molecular structured from XYZ  files that contained the atom types and the positions in the molecule. An example of an XYZ file can be found [here](http://paulbourke.net/dataformats/xyz/).

## Approach

The approach I followed for the challenge was to focus on feature engineering. 

### OpenBabel
The features I extracted using OpenBabel were the angles for the 2J couplings and the torsions for the 3J couplings. I also included the hybridization of the atoms coupled to the hydrogen atom.

As an extra feature engineering step, I included $\cos(\phi)$ and $\cos^{2}(\phi)$ following the Karplus equation.

### Additional Features
There were additional features calculated by other members of Lacuna. These additional features include information about distances between atoms in the molecule and information about neighbor atoms of the coupled pair.

## Results
The model and the features for the challenge achieved a score of -0.848 on Kaggle. This score was one of the top-100 scores in the initial week of the competition.

## How to Run

First, make sure that you have [conda](https://docs.conda.io/en/latest/) installed and install the project.

```shell
conda create -n MagneticInteractionsChallenge
pip install -e 'git+https://github.com/cmpatino/MagneticInteractionsChallenge.git#egg=magnetic_interactions'
```

The file `data_utils.py` has all the functions necessary to merge all the features and generate the datasets to fit the 8 models.

The file `ob_utils.py` has all the functions used to generate features using the `open_babel` library.

The process of creating the dataset is and fitting the models is condensed in the `Final Model.ipynb` Jupyter Notebook. 

## How to Run

First, make sure that you have [conda](https://docs.conda.io/en/latest/) installed and install the project.

```shell
conda create -n MagneticInteractionsChallenge
pip install -e 'git+https://github.com/cmpatino/MagneticInteractionsChallenge.git#egg=magnetic_interactions'
```

> For a private repository accessible only through an SSH authentication, substitute `git+https://github.com` with `git+ssh://git@github.com`.