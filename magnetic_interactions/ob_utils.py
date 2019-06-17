import openbabel as ob
import numpy as np


def atom_n_bonds(mol, atom_idx_0, bond_order=1):
    """Get number of bonds for each atom in the coupled pair

    Arguments:
        mol {ob.OBMol} -- Molecule in OpenBabel's format
        atom_idx {int} -- atom index

    Keyword Arguments:
        bond_order {int} -- bond order of counted bonds (default: {1})

    Returns:
        int -- number of bonds for atom
    """

    atom = mol.GetAtom(atom_idx_0)

    n_bonds = atom.CountBondsOfOrder(bond_order)

    return n_bonds


def total_n_bonds(mol):
    """Get total number of bonds in molecule

    Arguments:
        mol {ob.OBMol} -- Molecule in OpenBabel's format

    Returns:
        int -- number of bonds in the molecule
    """

    n_bonds = mol.NumBonds()

    return n_bonds


def get_angle(mol, ob_atom_idx_0, ob_atom_idx_1):
    """Get the angle between two atoms. The function is relevant for atoms in
    a 2J coupling

    Arguments:
        mol {OBMol} -- OpenBabel molecule object
        ob_atom_idx_0 {int} -- index of atom 0 in OpenBabel
        ob_atom_idx_1 {int} -- index of atom 1 in OpenBabel

    Returns:
        float -- value of angle between coupled atoms
    """

    atom_0 = mol.GetAtom(ob_atom_idx_0)
    atom_1 = mol.GetAtom(ob_atom_idx_1)

    for bond in ob.OBAtomBondIter(atom_0):

        end_atom_idx = bond.GetEndAtomIdx()

        if end_atom_idx == atom_0.GetIdx():
            pivot_atom = bond.GetBeginAtom()
        else:
            pivot_atom = bond.GetEndAtom()

        missing_bond = atom_1.GetBond(pivot_atom)

        if missing_bond:
            return mol.GetAngle(atom_0, pivot_atom, atom_1)

    return 0


def get_torsion_pivot(mol, ob_atom_idx_0, ob_atom_idx_1):
    """Find pivot atom of a torsion

    Arguments:
        mol {OBMol} -- OpenBabel molecule object
        ob_atom_idx_0 {int} -- index of atom 0 in OpenBabel
        ob_atom_idx_1 {int} -- index of atom 1 in OpenBabel

    Returns:
        OBAtom -- torsion pivot atom
    """

    atom_0 = mol.GetAtom(ob_atom_idx_0)
    atom_1 = mol.GetAtom(ob_atom_idx_1)

    for bond in ob.OBAtomBondIter(atom_0):

        end_atom_idx = bond.GetEndAtomIdx()

        if end_atom_idx == atom_0.GetIdx():
            pivot_atom = bond.GetBeginAtom()
        else:
            pivot_atom = bond.GetEndAtom()

        missing_bond = atom_1.GetBond(pivot_atom)

        if missing_bond:
            return pivot_atom

    return None


def get_torsion(mol, ob_atom_idx_0, ob_atom_idx_1):
    """Get torsion between the two coupled atoms. The function is relevant for
    atoms in a 3J coupling

    Arguments:
        mol {OBMol} -- OpenBabel molecule object
        ob_atom_idx_0 {int} -- index of atom 0 in OpenBabel
        ob_atom_idx_1 {int} -- index of atom 1 in OpenBabel

    Returns:
        float -- torsion value for the coupled pair
    """

    atom_0 = mol.GetAtom(ob_atom_idx_0)
    atom_1 = mol.GetAtom(ob_atom_idx_1)

    for bond in ob.OBAtomBondIter(atom_0):

        end_atom_idx = bond.GetEndAtomIdx()

        if end_atom_idx == atom_0.GetIdx():
            pivot_1 = bond.GetBeginAtom()
        else:
            pivot_1 = bond.GetEndAtom()

        pivot_2 = get_torsion_pivot(mol, atom_1.GetIdx(), pivot_1.GetIdx())

        if pivot_2:
            return mol.GetTorsion(atom_0, pivot_1, pivot_2, atom_1)

    return 0


def get_n_hyb_3(mol):
    """Get number of atoms in the molecule that have sp3 hybridization

    Arguments:
        mol {OBMol} -- OpenBabel molecule object

    Returns:
        int -- number of atoms with sp3 hybridization in molecule
    """

    n_atoms = mol.NumAtoms()
    count = 0

    for i in range(1, n_atoms + 1):

        atom = mol.GetAtom(i)
        atom_hyb = atom.GetHyb()
        if atom_hyb == 3:
            count += 1

    return count


def get_hybrid_coupled_atom(mol, ob_atom_idx_1):
    """Get hybridazation of atom coupled to hydrogen atom

    Arguments:
        mol {OBMol} -- OpenBabel molecule object
        ob_atom_idx_1 {int} -- index of atom coupled to hydrogen

    Returns:
        int -- hybridazation of atom
    """

    atom = mol.GetAtom(ob_atom_idx_1)
    hybridization = atom.GetHyb()

    return hybridization


def get_spin_multiplicity(mol):
    """Get spin multiplicity of molecule

    Arguments:
        mol {ob.OBMol} -- OpenBabel molecule object

    Returns:
        float -- spin multiplicity of molecule
    """

    spin_multiplicity = mol.GetTotalSpinMultiplicity()

    return spin_multiplicity


def create_ob_features(data_df):
    """Extract features from molecular structure using OpenBabel

    Arguments:
        data_df {pd.DataFrame} -- DataFrame with train or test data

    Returns:
        pd.DataFrame -- Train or test DataFrame with features
                        extracted from OpenBabel
    """

    structures_dir = "./data/champs-scalar-coupling/structures/"

    n_bonds_total = np.zeros((len(data_df), 1))
    n_bonds_0 = np.zeros((len(data_df), 1))
    n_bonds_1 = np.zeros((len(data_df), 1))
    angles = np.zeros((len(data_df), 1))
    torsions = np.zeros((len(data_df), 1))
    spin_multiplicities = np.zeros((len(data_df), 1))
    coupled_atom_hybs = np.zeros((len(data_df), 1))
    n_hyb_3 = np.zeros((len(data_df), 1))

    for i, row in enumerate(data_df.itertuples()):

        mol_name = row.molecule_name
        ob_atom_idx_0 = row.atom_index_0 + 1
        ob_atom_idx_1 = row.atom_index_1 + 1

        obConversion = ob.OBConversion()
        obConversion.SetInFormat("xyz")
        mol = ob.OBMol()
        obConversion.ReadFile(mol, structures_dir + f"{mol_name}.xyz")

        n_bonds_total[i] = total_n_bonds(mol)
        n_bonds_0[i] = atom_n_bonds(mol, ob_atom_idx_0)
        n_bonds_1[i] = atom_n_bonds(mol, ob_atom_idx_1)
        angles[i] = get_angle(mol, ob_atom_idx_0, ob_atom_idx_1)
        torsions[i] = get_torsion(mol, ob_atom_idx_0, ob_atom_idx_1)
        spin_multiplicities[i] = get_spin_multiplicity(mol)
        coupled_atom_hybs = get_hybrid_coupled_atom(mol, ob_atom_idx_1)
        n_hyb_3 = get_n_hyb_3(mol)

    data_df['n_bonds_mol'] = n_bonds_total
    data_df['n_bonds_0'] = n_bonds_0
    data_df['n_bonds_1'] = n_bonds_1
    data_df['angles'] = angles
    data_df['torsions'] = torsions
    data_df['spin'] = spin_multiplicities
    data_df['hyb_coupled_atom'] = coupled_atom_hybs
    data_df['n_hyb_3'] = n_hyb_3
    data_df['1/hyb'] = 1/(1 + data_df['hyb_coupled_atom'])

    return data_df
