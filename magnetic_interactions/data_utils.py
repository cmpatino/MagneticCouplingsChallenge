import numpy as np
import pandas as pd


def build_pair_level_df(df, structures_df,  atom_idx):
    """Extract position and type information for one atom in the coupling pair

    Arguments:
        df {pd.DataFrame} -- DataFrame containing the atom pairs
        structures_df {pd.DataFrame} -- DataFrame with information about the
                                        atoms in the molecules
        atom_idx {int} -- Index of atom in the pair (can be 0 or 1)

    Returns:
        pd.DataFrame -- DataFrame with position and type information for the
                        atom specified
    """

    pair_level_df = pd.merge(df, structures_df, how='left',
                             left_on=['molecule_name', 'atom_index_{}'
                                      .format(atom_idx)],
                             right_on=['molecule_name',  'atom_index'])

    pair_level_df = pair_level_df.drop('atom_index', axis=1)
    pair_level_df = pair_level_df.rename(columns={'atom': 'atom_type_{}'.format(atom_idx),
                                                  'x': 'x_{}'.format(atom_idx),
                                                  'y': 'y_{}'.format(atom_idx),
                                                  'z': 'z_{}'.format(atom_idx)})
    return pair_level_df


def create_structure_features(data_path, structures_data_path):
    """Create features related to molecular structure information.

    Arguments:
        data_path {str} -- path to train or test set
        structures_data_path {str} -- path to the data about XYZ and types data

    Returns:
        pd.DataFrame -- DataFrame with all features related with
                        molecular structure
    """

    df_big_memory = pd.read_csv(data_path)
    structures_big_memory = pd.read_csv(structures_data_path)

    df = reduce_mem_usage(df_big_memory)
    structures_df = reduce_mem_usage(structures_big_memory)

    del df_big_memory, structures_big_memory

    # Create Pair Level Features
    pair_level_df = build_pair_level_df(df, structures_df, 0)
    pair_level_df = build_pair_level_df(pair_level_df, structures_df, 1)
    pair_level_df = pair_level_df.rename(columns={'type': 'coupling_type'})

    # Create Molecular Level Features
    # N atoms in molecule
    atom_count = structures_df.groupby('molecule_name')\
                              .atom_index.count().reset_index(name='n_atoms')
    mol_structure_df = pd.merge(pair_level_df, atom_count,
                                on=['molecule_name'], how='left')

    # N atoms per type in molecule
    atom_types = structures_df.groupby(['molecule_name', 'atom'])\
                              .atom_index.count()
    atom_types = atom_types.unstack(fill_value=0)
    atom_types.columns = ['n_' + str(col) for col in atom_types.columns]
    mol_structure_df = pd.merge(mol_structure_df, atom_types,
                                on=['molecule_name'], how='left')

    return mol_structure_df


def data_pipeline(data_path, structures_data_path, angles_torsions_path,
                  bonds_path, distances_path, spins_path, hyb_path,
                  features_camilo_path,
                  train_data=True):

    df = create_structure_features(data_path, structures_data_path)

    df['atom_type_1'] = df['atom_type_1'].astype('category')
    one_hot_type = pd.get_dummies(df['atom_type_1'], prefix='type_1_')
    df = pd.concat([df, one_hot_type], axis=1)
    df = df.drop(['atom_type_1', 'atom_type_0'], axis=1)

    angles_torsions_df = pd.read_csv(angles_torsions_path)
    bonds_df = pd.read_csv(bonds_path)

    df = pd.merge(df, angles_torsions_df, on=['id', 'molecule_name'])
    df = pd.merge(df, bonds_df, on=['id', 'molecule_name'])
    df = reduce_mem_usage(df)

    df['karplus_1'] = np.cos(df['torsions'])
    df['karplus_2'] = (np.cos(df['torsions']))**2

    distances_df = pd.read_csv(distances_path)
    df = pd.merge(df, distances_df, on=['id', 'molecule_name'])
    df = reduce_mem_usage(df)

    spins_df = pd.read_csv(spins_path)
    df = pd.merge(df, spins_df, on=['molecule_name'], how='left')
    df = reduce_mem_usage(df)

    hyb_df = pd.read_csv(hyb_path)
    df = pd.merge(df, hyb_df, on=['id', 'molecule_name'])
    df = reduce_mem_usage(df)

    features_camilo_df = pd.read_csv(features_camilo_path)
    df = pd.merge(df, features_camilo_df, on=['id', 'molecule_name'])
    df = reduce_mem_usage(df)

    coupling_types = df.coupling_type.unique()
    coupling_dfs = {}
    coupling_targets = {}

    for coupling_type in coupling_types:

        coupling_type_df = df[df.coupling_type == coupling_type]

        if train_data:
            y_train_type = coupling_type_df['scalar_coupling_constant']
            coupling_type_df = coupling_type_df.drop('scalar_coupling_constant',
                                                     axis=1)
            coupling_targets[coupling_type] = y_train_type

        reduced_df = reduce_mem_usage(coupling_type_df)
        coupling_dfs[coupling_type] = reduced_df

    return coupling_dfs, coupling_targets


# Function taken from https://www.kaggle.com/artgor/artgor-utils
def reduce_mem_usage(df, verbose=True):
    """Function to reduce memory usage by retyping columns in a DataFrame

    Arguments:
        df {pd.DataFrame} -- DataFrame that is going to be re-typed

    Keyword Arguments:
        verbose {bool} -- Specify if function prints amount of memory
                          optimized (default: {True})

    Returns:
        pd.DataFrame -- DataFrame with optimized memory usage
    """
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage().sum() / 1024**2
    if verbose:
        print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df

