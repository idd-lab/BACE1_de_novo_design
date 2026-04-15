from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import DataStructs
from rdkit.SimDivFilters import MaxMinPicker

# Function to read SMILES from the input file
def read_smiles(file_path):
    with open(file_path, 'r') as f:
        smiles_list = [line.strip().split()[0] for line in f]  # Assumes SMILES is the first column
    return smiles_list

# Function to generate Morgan fingerprints
def generate_fingerprints(smiles_list):
    mols = [Chem.MolFromSmiles(smi) for smi in smiles_list if Chem.MolFromSmiles(smi) is not None]
    fps = [AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024) for mol in mols]
    return mols, fps

# Function to select diverse inhibitors using MaxMinPicker
def select_diverse_inhibitors(fps, num_to_pick):
    picker = MaxMinPicker()
    # Define a distance function (1 - Tanimoto similarity)
    def dist_func(i, j):
        return 1 - DataStructs.TanimotoSimilarity(fps[i], fps[j])
    # Pick indices of diverse inhibitors
    selected_indices = picker.LazyPick(dist_func, len(fps), num_to_pick)
    return list(selected_indices)

# Function to write selected inhibitors to a new file
def write_selected_smiles(mols, selected_indices, output_file):
    with open(output_file, 'w') as f:
        for idx in selected_indices:
            smi = Chem.MolToSmiles(mols[idx])
            f.write(f"{smi}\n")

# Main function to run the process
def main(input_file, output_file, num_to_pick=2400):
    # Read SMILES
    smiles_list = read_smiles(input_file)
    print(f"Loaded {len(smiles_list)} inhibitors from {input_file}")
    
    # Generate fingerprints
    mols, fps = generate_fingerprints(smiles_list)
    print(f"Generated fingerprints for {len(mols)} valid molecules")
    
    # Select diverse inhibitors
    selected_indices = select_diverse_inhibitors(fps, num_to_pick)
    print(f"Selected {len(selected_indices)} diverse inhibitors")
    
    # Write to output file
    write_selected_smiles(mols, selected_indices, output_file)
    print(f"Saved selected inhibitors to {output_file}")

# Run the script with your file paths
if __name__ == "__main__":
    input_file = AutoGrow_default_ZINC_lib_100_150.smi
    output_file = selected_default_200.smi
    main(input_file, output_file, num_to_pick=200)    #Modify to your need (to 2000 for LBDD)
