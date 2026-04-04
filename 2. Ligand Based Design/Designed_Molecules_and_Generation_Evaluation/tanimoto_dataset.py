import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs

# Define WSL/Ubuntu Paths
candidates_path = "/mnt/c/Users/THANG/Desktop/qsar/cleaned/Designed_Molecules_cleaned/candidates_zoned_full_CNS.csv"
inhibitors_path = "/mnt/c/Users/THANG/Desktop/qsar/cleaned/Designed_Molecules_cleaned/inhibitors_pKi_M_cleaned.txt"
output_path = "/mnt/c/Users/THANG/Desktop/qsar/cleaned/Designed_Molecules_cleaned/candidates_with_max_tanimoto_LBDD.csv"

def generate_morgan_fp(smiles):
    """
    Generates an RDKit molecular object and computes the extended-connectivity 
    fingerprint (ECFP4-like, Morgan radius = 2, nBits = 2048).
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            return AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
    except Exception:
        pass
    return None

print("Loading dataset files...")
# Load the designed molecules and reference inhibitors
df_candidates = pd.read_csv(candidates_path)
df_inhibitors = pd.read_csv(inhibitors_path, sep='\t') 

print(f"Generating Morgan fingerprints for {len(df_inhibitors)} reference inhibitors...")
# Generate molecular objects and fingerprints for the reference inhibitors
reference_fps = []
for smiles in df_inhibitors['SMILES']:
    fp = generate_morgan_fp(smiles)
    if fp is not None:
        reference_fps.append(fp)

print(f"Computing pairwise Tanimoto similarity for {len(df_candidates)} designed molecules...")
max_tanimoto_scores = []

# Compute pairwise Tanimoto similarity coefficients against reference inhibitors
for smiles in df_candidates['SMILES']:
    designed_fp = generate_morgan_fp(smiles)
    
    if designed_fp is not None and reference_fps:
        # Utilizing BulkTanimotoSimilarity to compute coefficients against all references
        similarity_coefficients = DataStructs.BulkTanimotoSimilarity(designed_fp, reference_fps)
        max_score = max(similarity_coefficients)
        max_tanimoto_scores.append(max_score)
    else:
        max_tanimoto_scores.append(None)

# Append the maximum similarity coefficient as a new column
df_candidates['SBDD_Tanimoto_max'] = max_tanimoto_scores

# Export the updated dataframe
df_candidates.to_csv(output_path, index=False)
print(f"Processing complete. Data successfully saved to:\n{output_path}")