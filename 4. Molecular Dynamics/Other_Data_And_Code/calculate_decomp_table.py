import pandas as pd
import numpy as np
import os

# --- CONFIGURATION (Paths and Residues) ---

# Adjusted to your WSL paths and updated Ligand list
LIGAND_FILES = {
    '14XS': [
        "/mnt/d/4. Molecular Dynamics/14XS/rep_1/CLEAN_FINAL_DECOMP_MMPBSA.csv",
        "/mnt/d/4. Molecular Dynamics/14XS/rep_2/CLEAN_FINAL_DECOMP_MMPBSA.csv",
        "/mnt/d/4. Molecular Dynamics/14XS/rep_3/CLEAN_FINAL_DECOMP_MMPBSA.csv",
    ],
    '32': [
        "/mnt/d/4. Molecular Dynamics/32/rep_1/CLEAN_FINAL_DECOMP_MMPBSA.csv",
        "/mnt/d/4. Molecular Dynamics/32/rep_2/CLEAN_FINAL_DECOMP_MMPBSA.csv",
        "/mnt/d/4. Molecular Dynamics/32/rep_3/CLEAN_FINAL_DECOMP_MMPBSA.csv",
    ],
    '41': [
        "/mnt/d/4. Molecular Dynamics/41/rep_1/CLEAN_FINAL_DECOMP_MMPBSA.csv",
        "/mnt/d/4. Molecular Dynamics/41/rep_2/CLEAN_FINAL_DECOMP_MMPBSA.csv",
        "/mnt/d/4. Molecular Dynamics/41/rep_3/CLEAN_FINAL_DECOMP_MMPBSA.csv",
    ],
    '73': [
        "/mnt/d/4. Molecular Dynamics/73/rep_1/CLEAN_FINAL_DECOMP_MMPBSA.csv",
        "/mnt/d/4. Molecular Dynamics/73/rep_2/CLEAN_FINAL_DECOMP_MMPBSA.csv",
        "/mnt/d/4. Molecular Dynamics/73/rep_3/CLEAN_FINAL_DECOMP_MMPBSA.csv",
    ],
    '96': [
        "/mnt/d/4. Molecular Dynamics/96/rep_1/CLEAN_FINAL_DECOMP_MMPBSA.csv",
        "/mnt/d/4. Molecular Dynamics/96/rep_2/CLEAN_FINAL_DECOMP_MMPBSA.csv",
        "/mnt/d/4. Molecular Dynamics/96/rep_3/CLEAN_FINAL_DECOMP_MMPBSA.csv",
    ]
}

# The specific residues identified in your analysis
RESIDUES_OF_INTEREST = [
    'R:A:LEU:35', 'R:A:ASH:37', 'R:A:SER:40', 'R:A:VAL:74', 'R:A:TYR:76', 
    'R:A:ILE:123', 'R:A:ARG:133', 'R:A:ASP:224', 'R:A:THR:227'
]

OUTPUT_TABLE_PATH = "/mnt/d/4. Molecular Dynamics/Table_S3_Decomp_Averaged.csv"

# --- CORE LOGIC ---

def process_all_ligands(ligand_files, residues):
    all_results = []

    for ligand_name, rep_files in ligand_files.items():
        replicate_contributions = {res: [] for res in residues}

        for f in rep_files:
            if not os.path.exists(f):
                print(f"ERROR: File not found: {f}. Check paths. Skipping replicate.")
                continue
                
            df = pd.read_csv(f).set_index('Residue')
            
            for res in residues:
                if res in df.index:
                    contribution = df.loc[res, 'Total_Avg']
                    replicate_contributions[res].append(contribution)
                else:
                    replicate_contributions[res].append(0.0) 

        # Calculate Mean and Sample SD across the 3 replicates for each residue
        for res, contributions in replicate_contributions.items():
            if len(contributions) > 0:
                mean_val = np.mean(contributions)
                # CORRECTED: ddof=1 for Sample Standard Deviation across the 3 independent seeds
                std_dev_val = np.std(contributions, ddof=1) if len(contributions) > 1 else 0.0
                
                all_results.append({
                    'Ligand': ligand_name,
                    'Residue': res,
                    'Mean_Total_Avg': mean_val,
                    'SD_Rep_Avg': std_dev_val
                })
                
    return pd.DataFrame(all_results)

def format_residue_name_simple(res_str):
    """Cleans R:A:GLY:2 -> Gly-2"""
    try:
        parts = res_str.split(':')
        return f"{parts[2].title()}-{parts[3]}"
    except:
        return res_str

if __name__ == "__main__":
    
    print("Processing Decomposition Data...")
    final_df = process_all_ligands(LIGAND_FILES, RESIDUES_OF_INTEREST)
    
    if final_df.empty:
        print("Error: No data processed. Check file paths.")
    else:
        final_df['Residue_Label'] = final_df['Residue'].apply(format_residue_name_simple)
        
        final_df['Report_Value'] = final_df.apply(
            lambda row: f"{row['Mean_Total_Avg']:.2f} \u00B1 {row['SD_Rep_Avg']:.2f}", axis=1
        )
        
        pivot_table = final_df.pivot(index='Ligand', columns='Residue_Label', values='Report_Value')
        
        print("\n--- DECOMPOSITION DATA (MEAN ± SD, kcal/mol) ---")
        print(pivot_table)
        
        final_df.to_csv(OUTPUT_TABLE_PATH, index=False)
        # Also save the pivot table as it's the actual publication format
        pivot_table.to_csv(OUTPUT_TABLE_PATH.replace('.csv', '_Pivot.csv'))
        print(f"\nSaved detailed analysis to {OUTPUT_TABLE_PATH}")
        print(f"Saved publication-ready table to {OUTPUT_TABLE_PATH.replace('.csv', '_Pivot.csv')}")