import pandas as pd
import matplotlib
# Use Agg backend for reliable file output
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

# --- 1. CONFIGURATION (EDIT THIS SECTION) ---

# Updated to WSL paths and the correct 5 ligands in your local machine
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

# Define your catalytic dyad for BACE1
DYAD_RESIDUES = ['R:A:ASH:37', 'R:A:ASP:224'] 

TOP_N_CONTRIBUTORS = 5
FIGURE_FILE_PATH = "/mnt/d/4. Molecular Dynamics/Figure9_Decomp_Fingerprint.pdf"
# --- END CONFIGURATION ---

def format_residue_name(res_str):
    """Cleans R:A:GLY:2 -> GLY-2"""
    try:
        parts = res_str.split(':')
        return f"{parts[2].title()}-{parts[3]}"
    except:
        return res_str

def get_mean_std_all_ligands(ligand_files):
    """Averages replicates and returns a dict of DataFrames."""
    
    all_ligand_avg_data = {}
    
    for ligand_name, rep_files in ligand_files.items():
        all_dfs = []
        for f in rep_files:
            if not os.path.exists(f):
                print(f"ERROR: File not found: {f}. Skipping.")
                continue
            # Read only the 'Total_Avg' column, indexed by 'Residue'
            all_dfs.append(pd.read_csv(f).set_index('Residue')['Total_Avg'])
        
        if not all_dfs:
            print(f"No data for ligand {ligand_name}. Skipping.")
            continue
            
        # Concat all reps for this ligand (Residues x Reps)
        concatenated_df = pd.concat(all_dfs, axis=1)
        
        # Calculate Mean and Std Dev across replicates (axis=1)
        avg_decomp = pd.DataFrame()
        avg_decomp['Mean'] = concatenated_df.mean(axis=1)
        
        # Explicitly setting ddof=1 for rigorous Sample SD documentation
        avg_decomp['Std_Dev'] = concatenated_df.std(axis=1, ddof=1) 
        all_ligand_avg_data[ligand_name] = avg_decomp
        
    return all_ligand_avg_data

def get_master_residue_list(all_ligand_avg_data, dyad, top_n):
    """Gets the union of Top N from all ligands + the dyad."""
    master_set = set(dyad)
    
    for ligand_name, data in all_ligand_avg_data.items():
        
        # Filter out the ligand (UNL) before finding top contributors
        data_no_ligand = data[~data.index.str.contains('UNL', case=False)]
        
        # Find top N *negative* contributors (most favorable)
        top_n_residues = data_no_ligand.nsmallest(top_n, 'Mean').index
        master_set.update(top_n_residues)
        
    # Sort the final list for plotting
    return sorted(list(master_set), key=lambda x: (x.split(':')[1], int(x.split(':')[-1])))

# --- 3. MAIN EXECUTION ---
if __name__ == "__main__":
    print("Analyzing all replicates...")
    all_ligand_data = get_mean_std_all_ligands(LIGAND_FILES)

    print("Finding top contributors (excluding ligand)...")
    plot_residues = get_master_residue_list(all_ligand_data, DYAD_RESIDUES, TOP_N_CONTRIBUTORS)
    plot_labels = [format_residue_name(r) for r in plot_residues]
    num_residues = len(plot_residues)
    num_ligands = len(all_ligand_data)

    print(f"Master list of {num_residues} residues for plotting: {plot_labels}")

    # --- 4. PLOTTING ---
    print("Generating plot...")
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(max(15, num_residues * 1.5), 8))
    plt.rcParams['figure.dpi'] = 300 

    bar_width = 0.8 / num_ligands
    index = np.arange(num_residues)
    
    # 5 Colors matching the previous RMSD plots
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'] 

    for i, (ligand, data) in enumerate(all_ligand_data.items()):
        # Get the Mean and SD for only the residues we are plotting
        means = [data.loc[res]['Mean'] if res in data.index else 0 for res in plot_residues]
        std_devs = [data.loc[res]['Std_Dev'] if res in data.index else 0 for res in plot_residues]
        
        bar_pos = index + (i - num_ligands / 2 + 0.5) * bar_width
        
        ax.bar(bar_pos, means, bar_width, yerr=std_devs, label=ligand, 
               capsize=3, error_kw={'capthick': 1, 'elinewidth': 1}, color=colors[i])

    # --- 5. FORMATTING ---
    ax.set_ylabel('Mean Energy Contribution (kcal/mol)', fontsize=14, fontweight='bold')
    ax.set_title(f'Per-Residue Interaction Fingerprint (Averaged from Triplicates)', fontsize=16, fontweight='bold')
    ax.set_xticks(index)
    ax.set_xticklabels(plot_labels, rotation=45, ha='right', fontsize=12)
    ax.axhline(0, color='black', linewidth=0.8) 
    ax.legend(title="Ligand", fontsize=12, title_fontsize=13, loc='lower right')
    ax.grid(axis='x', linestyle='--', alpha=0) 

    # Highlight the catalytic dyad
    dyad_labels = [format_residue_name(r) for r in DYAD_RESIDUES]
    for i, label in enumerate(plot_labels):
        if label in dyad_labels:
            ax.get_xticklabels()[i].set_color('red')
            ax.get_xticklabels()[i].set_fontweight('bold')

    plt.tight_layout()
    plt.savefig(FIGURE_FILE_PATH)
    print(f"\nPlot saved successfully to {FIGURE_FILE_PATH}")
    print("This single plot visually proves your hypothesis.")
