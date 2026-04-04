import pandas as pd
from rdkit import Chem
import warnings

# Suppress RDKit warnings to keep the terminal clean
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*') 

# 1. Define WSL/Ubuntu Paths
rediscovery_path = "/mnt/c/Users/THANG/Desktop/qsar/cleaned/Designed_Molecules_cleaned/re_discovery.txt"
bdb_path = "/mnt/c/Users/THANG/Desktop/qsar/Data_Curation/raw_binding_db.csv"
output_path = "/mnt/c/Users/THANG/Desktop/qsar/cleaned/Designed_Molecules_cleaned/re_discovery_BDB_matched.csv"

print("Loading raw BindingDB dataset...")
# 2. Load the BindingDB dataset
# BindingDB files are notoriously large and sometimes have mixed datatypes, low_memory=False prevents warnings
bdb_df = pd.read_csv(bdb_path, low_memory=False, on_bad_lines='skip')

print("Building canonical SMILES mapping from BindingDB (This might take a minute)...")
# 3. Create a strict Canonical SMILES dictionary mapping to BDB info
bdb_map = {}
for idx, row in bdb_df.iterrows():
    smi = row.get('Ligand SMILES')
    if pd.isna(smi):
        continue
        
    # Grab DOI (Preferring the Article DOI, falling back to BindingDB Entry DOI)
    doi = row.get('Article DOI')
    if pd.isna(doi):
        doi = row.get('BindingDB Entry DOI', 'Not Found')
        
    ki_nm = row.get('Ki (nM)', 'N/A')
    
    try:
        mol = Chem.MolFromSmiles(str(smi))
        if mol:
            canon_smi = Chem.MolToSmiles(mol, canonical=True)
            # Store the data. If duplicates exist, we keep the first one parsed.
            if canon_smi not in bdb_map:
                bdb_map[canon_smi] = {
                    'BDB_DOI': doi,
                    'Experimental_Ki_nM': ki_nm
                }
    except Exception:
        pass

print(f"Loaded {len(bdb_map)} unique valid structures from BindingDB.")

print("Processing re-discovery candidates...")
# 4. Load the re-discovery file
# Your txt file is tab-separated based on the previous structure
rediscovery_df = pd.read_csv(rediscovery_path, sep="\t")

matched_data = []

# 5. Cross-reference and generate identifiers
for idx, row in rediscovery_df.iterrows():
    orig_smi = str(row['SMILES'])
    mol = Chem.MolFromSmiles(orig_smi)
    
    if mol:
        canon_smi = Chem.MolToSmiles(mol, canonical=True)
        
        # Generate standard molecular identifiers
        inchi = Chem.MolToInchi(mol)
        inchi_key = Chem.InchiToInchiKey(inchi)
        
        # Match against the BindingDB dictionary
        match_info = bdb_map.get(canon_smi, {})
        
        matched_data.append({
            'SMILES': orig_smi,
            'InChI_ID': inchi_key,
            'BDB_DOI': match_info.get('BDB_DOI', 'Not Found in DB'),
            'Experimental_Ki_nM': match_info.get('Experimental_Ki_nM', 'N/A'),
            'Predicted_pKi': row['Predicted_pKi'],
            'Max_Sim_AD': row['Max_Sim_AD'],
            'Zone': row['Zone']
        })
    else:
        # Fallback if RDKit fails to parse the generated SMILES
        matched_data.append({
            'SMILES': orig_smi,
            'InChI_ID': 'Parsing Error',
            'BDB_DOI': 'Parsing Error',
            'Experimental_Ki_nM': 'Parsing Error',
            'Predicted_pKi': row['Predicted_pKi'],
            'Max_Sim_AD': row['Max_Sim_AD'],
            'Zone': row['Zone']
        })

# 6. Save the enriched data
results_df = pd.DataFrame(matched_data)
results_df.to_csv(output_path, index=False)

print(f"\nMatch complete! Enriched dataset successfully saved to:\n{output_path}")