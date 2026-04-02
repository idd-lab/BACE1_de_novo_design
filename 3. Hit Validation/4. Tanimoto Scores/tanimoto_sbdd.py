import pandas as pd
import numpy as np
import os
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit import DataStructs

# --- 1. CONFIGURATION (WSL Paths) ---
SBDD_FILE = "/mnt/d/Archive/For_Writing_Paper/All_Molecules/Run_All/all_canonical_unique_SBDD.txt"
INHIBITORS_FILE = "/mnt/d/Archive/For_Writing_Paper/All_Molecules/Run_All/inhibitors_pKi_M_cleaned.txt"

def load_smiles(filepath):
    """
    Reads a text file and extracts the first column as SMILES strings.
    Handles space, tab, or comma separation.
    """
    smiles_list = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(('#', 'SMILES', 'smiles')):
                    continue
                # Take the first token as the SMILES string
                smi = line.replace(',', ' ').replace('\t', ' ').split()[0]
                smiles_list.append(smi)
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}")
        return []
    return smiles_list

def get_fingerprints(smiles_list, name_tag):
    """
    Converts a list of SMILES to RDKit Morgan fingerprints (radius=2, 2048 bits).
    Drops invalid SMILES to prevent crashes.
    """
    fps = []
    valid_count = 0
    print(f"Processing {name_tag} fingerprints...")
    
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol is not None:
            # ECFP4 equivalent
            fp = rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
            fps.append(fp)
            valid_count += 1
            
    print(f"  -> Successfully generated {valid_count} fingerprints from {len(smiles_list)} SMILES.")
    return fps

def analyze_tanimoto_max():
    # 1. Load Data
    print("Loading datasets...")
    sbdd_smiles = load_smiles(SBDD_FILE)
    inhibitor_smiles = load_smiles(INHIBITORS_FILE)
    
    if not sbdd_smiles or not inhibitor_smiles:
        print("Data loading failed. Check file paths and formats.")
        return

    # 2. Generate Fingerprints
    sbdd_fps = get_fingerprints(sbdd_smiles, "SBDD Compounds")
    inhibitor_fps = get_fingerprints(inhibitor_smiles, "Known Inhibitors")
    
    if not sbdd_fps or not inhibitor_fps:
        print("Fingerprint generation failed. Cannot proceed.")
        return

    # 3. Calculate Max Tanimoto Similarity
    print("\nCalculating Tanimoto_max for each SBDD compound against all inhibitors...")
    max_sims = []
    
    for count, fp_sbdd in enumerate(sbdd_fps, 1):
        # DataStructs.BulkTanimotoSimilarity compares one FP against a list of FPs very fast
        sims = DataStructs.BulkTanimotoSimilarity(fp_sbdd, inhibitor_fps)
        max_sims.append(max(sims))
        
        if count % 1000 == 0:
            print(f"  -> Processed {count}/{len(sbdd_fps)} SBDD compounds...")

    # 4. Statistical Analysis
    max_sims_array = np.array(max_sims)
    
    n = len(max_sims_array)
    val_min = np.min(max_sims_array)
    val_max = np.max(max_sims_array)
    val_mean = np.mean(max_sims_array)
    
    # Sample standard deviation (ddof=1)
    val_std = np.std(max_sims_array, ddof=1) if n > 1 else 0.0
    val_sem = val_std / np.sqrt(n) if n > 0 else 0.0

    print("\n--- STATISTICAL RESULTS: SBDD Tanimoto_max ---")
    print(f"Total Evaluated: {n}")
    print(f"Range:           {val_min:.4f} to {val_max:.4f}")
    print(f"Mean:            {val_mean:.4f}")
    print(f"SD:              {val_std:.4f}")
    print(f"SEM:             {val_sem:.4f}")
    
    # Optional: Save the raw array to a CSV if you need to plot a distribution graph later
    pd.DataFrame({'Tanimoto_max': max_sims_array}).to_csv('/mnt/d/Archive/For_Writing_Paper/All_Molecules/Run_All/SBDD_Tanimoto_max.csv', index=False)

if __name__ == "__main__":
    analyze_tanimoto_max()