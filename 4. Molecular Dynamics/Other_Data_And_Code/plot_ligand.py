import matplotlib.pyplot as plt
import numpy as np
import os

def load_xvg(filepath):
    """
    Loads data from a GROMACS .xvg file, skipping comment lines.
    Returns time (ns) and rmsd (nm) as numpy arrays.
    """
    time, rmsd = [], []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                # Skip comments
                if not line.startswith(('@', '#')):
                    cols = line.split()
                    if len(cols) >= 2:
                        try:
                            time.append(float(cols[0]))
                            rmsd.append(float(cols[1]))
                        except ValueError:
                            print(f"Warning: Could not parse line in {filepath}: {line}")
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}. Skipping.")
        return None, None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None, None
        
    return np.array(time), np.array(rmsd)

# --- Configuration ---

# 1. Define all data, converting Windows paths to Ubuntu/WSL paths, update to paths according to your local machine
LIGAND_DATA = [
    {
        "name": "Ligand 14XS",
        "output_file": "ligand_rmsd_14XS.png",
        "files": [
            "/mnt/d/4. Molecular Dynamics/14XS/rep_1/rmsd_ligand.xvg",
            "/mnt/d/4. Molecular Dynamics/14XS/rep_2/rmsd_ligand.xvg",
            "/mnt/d/4. Molecular Dynamics/14XS/rep_3/rmsd_ligand.xvg",
        ]
    },
    {
        "name": "Ligand 32",
        "output_file": "ligand_rmsd_32.png",
        "files": [
            "/mnt/d/4. Molecular Dynamics/32/rep_1/rmsd_ligand.xvg",
            "/mnt/d/4. Molecular Dynamics/32/rep_2/rmsd_ligand.xvg",
            "/mnt/d/4. Molecular Dynamics/32/rep_3/rmsd_ligand.xvg",
        ]
    },
    {
        "name": "Ligand 41",
        "output_file": "ligand_rmsd_41.png",
        "files": [
            "/mnt/d/4. Molecular Dynamics/41/rep_1/rmsd_ligand.xvg",
            "/mnt/d/4. Molecular Dynamics/41/rep_2/rmsd_ligand.xvg",
            "/mnt/d/4. Molecular Dynamics/41/rep_3/rmsd_ligand.xvg",
        ]
    },
    {
        "name": "Ligand 73",
        "output_file": "ligand_rmsd_73.png",
        "files": [
            "/mnt/d/4. Molecular Dynamics/73/rep_1/rmsd_ligand.xvg",
            "/mnt/d/4. Molecular Dynamics/73/rep_2/rmsd_ligand.xvg",
            "/mnt/d/4. Molecular Dynamics/73/rep_3/rmsd_ligand.xvg",
        ]
    },
    {
        "name": "Ligand 96",
        "output_file": "ligand_rmsd_96.png",
        "files": [
            "/mnt/d/4. Molecular Dynamics/96/rep_1/rmsd_ligand.xvg",
            "/mnt/d/4. Molecular Dynamics/96/rep_2/rmsd_ligand.xvg",
            "/mnt/d/4. Molecular Dynamics/96/rep_3/rmsd_ligand.xvg",
        ]
    }
]

# 2. Define colors and styles for the 3 replicates
REP_STYLES = [
    {'color': '#1f77b4', 'style': '-', 'label': 'Rep 1'}, # Blue, solid
    {'color': '#ff7f0e', 'style': '--', 'label': 'Rep 2'}, # Orange, dashed
    {'color': '#2ca02c', 'style': ':', 'label': 'Rep 3'}  # Green, dotted
]

# --- Plotting Loop ---

print("Generating 5 ligand RMSD plots...")

for ligand in LIGAND_DATA:
    plt.figure(figsize=(10, 6)) # Create a new figure for each ligand
    
    print(f"Processing {ligand['name']}...")
    
    for i, filepath in enumerate(ligand["files"]):
        time, rmsd = load_xvg(filepath)
        
        if time is not None and rmsd is not None:
            plt.plot(time, rmsd, 
                     label=REP_STYLES[i]['label'], 
                     color=REP_STYLES[i]['color'], 
                     linestyle=REP_STYLES[i]['style'], 
                     linewidth=1.5)

    # --- Formatting for each plot ---
    plt.title(f"{ligand['name']} - Ligand RMSD (All Reps)", fontsize=16)
    plt.xlabel("Time (ns)", fontsize=14)
    plt.ylabel("Ligand RMSD (nm)", fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xlim(0)
    plt.ylim(0)
    
    # Save the individual plot
    plt.savefig(ligand["output_file"], dpi=300, bbox_inches='tight')
    print(f"Saved plot to {ligand['output_file']}")
    plt.close() # Close the figure to start fresh for the next ligand

print("\nAll ligand plots complete.")
