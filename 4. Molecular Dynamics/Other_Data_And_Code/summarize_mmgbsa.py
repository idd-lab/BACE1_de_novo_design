import pandas as pd
import numpy as np
import os
import re

# --- CONFIGURATION ---
# Define the paths to your 15 FINAL_RESULTS_MMPBSA.dat files
LIGAND_FILES = {
    '14XS': [
        "/mnt/d/4. Molecular Dynamics/14XS/rep_1/FINAL_RESULTS_MMPBSA.dat",
        "/mnt/d/4. Molecular Dynamics/14XS/rep_2/FINAL_RESULTS_MMPBSA.dat",
        "/mnt/d/4. Molecular Dynamics/14XS/rep_3/FINAL_RESULTS_MMPBSA.dat",
    ],
    '32': [
        "/mnt/d/4. Molecular Dynamics/32/rep_1/FINAL_RESULTS_MMPBSA.dat",
        "/mnt/d/4. Molecular Dynamics/32/rep_2/FINAL_RESULTS_MMPBSA.dat",
        "/mnt/d/4. Molecular Dynamics/32/rep_3/FINAL_RESULTS_MMPBSA.dat",
    ],
    '41': [
        "/mnt/d/4. Molecular Dynamics/41/rep_1/FINAL_RESULTS_MMPBSA.dat",
        "/mnt/d/4. Molecular Dynamics/41/rep_2/FINAL_RESULTS_MMPBSA.dat",
        "/mnt/d/4. Molecular Dynamics/41/rep_3/FINAL_RESULTS_MMPBSA.dat",
    ],
    '73': [
        "/mnt/d/4. Molecular Dynamics/73/rep_1/FINAL_RESULTS_MMPBSA.dat",
        "/mnt/d/4. Molecular Dynamics/73/rep_2/FINAL_RESULTS_MMPBSA.dat",
        "/mnt/d/4. Molecular Dynamics/73/rep_3/FINAL_RESULTS_MMPBSA.dat",
    ],
    '96': [
        "/mnt/d/4. Molecular Dynamics/96/rep_1/FINAL_RESULTS_MMPBSA.dat",
        "/mnt/d/4. Molecular Dynamics/96/rep_2/FINAL_RESULTS_MMPBSA.dat",
        "/mnt/d/4. Molecular Dynamics/96/rep_3/FINAL_RESULTS_MMPBSA.dat",
    ]
}

OUTPUT_FILE = "Table_S3_MMGBSA_Summary.csv"

# --- PARSING FUNCTION ---
def parse_mmgbsa_results(filepath):
    """
    Parses a FINAL_RESULTS_MMPBSA.dat file to extract energy components.
    Returns a dictionary of values.
    """
    data = {}
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None

    # Flags to locate the correct section
    in_delta_section = False
    
    for line in lines:
        if "Delta (Complex - Receptor - Ligand):" in line:
            in_delta_section = True
            continue
        
        if in_delta_section:
            # Stop if we hit a separator line or empty line after reading data
            if line.strip().startswith("---") or line.strip() == "":
                continue
                
            parts = line.split()
            if len(parts) >= 2:
                component = parts[0]
                try:
                    # The value is the second column (Average)
                    value = float(parts[1])
                    
                    # Map the component names to your desired table headers
                    if component == "ΔTOTAL": data['Total_Binding_Energy'] = value
                    elif component == "ΔVDWAALS": data['VDW'] = value
                    elif component == "ΔEEL": data['Electrostatic'] = value
                    elif component == "ΔEGB": data['Polar_Solvation'] = value
                    elif component == "ΔESURF": data['Nonpolar_Solvation'] = value
                    
                except ValueError:
                    continue
    
    return data

# --- MAIN LOGIC ---
all_results = []

print("Processing MM/GBSA results...")

for ligand, files in LIGAND_FILES.items():
    ligand_data = {
        'Total_Binding_Energy': [],
        'VDW': [],
        'Electrostatic': [],
        'Polar_Solvation': [],
        'Nonpolar_Solvation': []
    }
    
    valid_reps = 0
    for f in files:
        result = parse_mmgbsa_results(f)
        if result:
            valid_reps += 1
            for key in ligand_data:
                if key in result:
                    ligand_data[key].append(result[key])
    
    if valid_reps == 0:
        print(f"Warning: No valid data found for Ligand {ligand}")
        continue

    # Calculate Mean and Sample SD for this ligand
    summary_row = {'Ligand': ligand}
    for key, values in ligand_data.items():
        mean_val = np.mean(values)
        
        # ddof=1 is used to calculate the Sample Standard Deviation, 
        # which is statistically correct for 3 replicates.
        sd_val = np.std(values, ddof=1) if len(values) > 1 else 0.0 
        
        # Format as "Mean ± SD" string
        summary_row[f"{key} (Mean ± SD)"] = f"{mean_val:.2f} ± {sd_val:.2f}"
        
        # Also keep raw mean/sd for sorting or other use if needed
        summary_row[f"{key}_Mean"] = mean_val
        summary_row[f"{key}_SD"] = sd_val

    all_results.append(summary_row)

# --- SAVE OUTPUT ---
df = pd.DataFrame(all_results)

# Reorder columns for the final table
cols_ordered = ['Ligand', 
                'Total_Binding_Energy (Mean ± SD)', 
                'VDW (Mean ± SD)', 
                'Electrostatic (Mean ± SD)', 
                'Polar_Solvation (Mean ± SD)', 
                'Nonpolar_Solvation (Mean ± SD)']

df_final = df[cols_ordered]

print("\n--- Calculated Table S3 Data ---")
print(df_final.to_string(index=False))

df_final.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved summary table to {OUTPUT_FILE}")