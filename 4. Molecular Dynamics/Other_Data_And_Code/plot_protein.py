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

# 1. Define all data, converting Windows paths to Ubuntu/WSL paths
# Note: Ligand names are simplified for the plot legend
LIGAND_DATA = [
    {
        "name": "Ligand 14XS",
        "color": "#1f77b4", # Blue
        "files": [
            "/mnt/d/4. Molecular Dynamics/14XS/rep_1/rmsd_protein.xvg",
            "/mnt/d/4. Molecular Dynamics/14XS/rep_2/rmsd_protein.xvg",
            "/mnt/d/4. Molecular Dynamics/14XS/rep_3/rmsd_protein.xvg",
        ]
    },
    {
        "name": "Ligand 32",
        "color": "#ff7f0e", # Orange
        "files": [
            "/mnt/d/4. Molecular Dynamics/32/rep_1/rmsd_protein.xvg",
            "/mnt/d/4. Molecular Dynamics/32/rep_2/rmsd_protein.xvg",
            "/mnt/d/4. Molecular Dynamics/32/rep_3/rmsd_protein.xvg",
        ]
    },
    {
        "name": "Ligand 41",
        "color": "#2ca02c", # Green
        "files": [
            "/mnt/d/4. Molecular Dynamics/41/rep_1/rmsd_protein.xvg",
            "/mnt/d/4. Molecular Dynamics/41/rep_2/rmsd_protein.xvg",
            "/mnt/d/4. Molecular Dynamics/41/rep_3/rmsd_protein.xvg",
        ]
    },
    {
        "name": "Ligand 73",
        "color": "#d62728", # Red
        "files": [
            "/mnt/d/4. Molecular Dynamics/73/rep_1/rmsd_protein.xvg",
            "/mnt/d/4. Molecular Dynamics/73/rep_2/rmsd_protein.xvg",
            "/mnt/d/4. Molecular Dynamics/73/rep_3/rmsd_protein.xvg",
        ]
    },
    {
        "name": "Ligand 96",
        "color": "#9467bd", # Purple
        "files": [
            "/mnt/d/4. Molecular Dynamics/96/rep_1/rmsd_protein.xvg",
            "/mnt/d/4. Molecular Dynamics/96/rep_2/rmsd_protein.xvg",
            "/mnt/d/4. Molecular Dynamics/96/rep_3/rmsd_protein.xvg",
        ]
    }
]

# 2. Define linestyles for each replicate
LINESTYLES = ['-', '--', ':'] # Rep 1 (solid), Rep 2 (dashed), Rep 3 (dotted)

# --- Plotting Function 1: All Replicates ---

def plot_all_replicates(data):
    """
    Generates the plot showing every individual replicate (color by ligand, style by rep).
    """
    print("Generating all-replicates plot...")
    plt.figure(figsize=(13, 8))
    
    for ligand in data:
        color = ligand["color"]
        name = ligand["name"]
        for i, filepath in enumerate(ligand["files"]):
            time, rmsd = load_xvg(filepath)
            if time is not None and rmsd is not None:
                style = LINESTYLES[i]
                rep_num = i + 1
                plt.plot(time, rmsd, 
                         label=f"{name} - Rep {rep_num}", 
                         color=color, 
                         linestyle=style, 
                         linewidth=1.2)

    plt.title("Protein RMSD (All Replicates)", fontsize=18, pad=20)
    plt.xlabel("Time (ns)", fontsize=14)
    plt.ylabel("Protein RMSD (nm)", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Place legend outside of the plot to avoid covering data
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize='small')
    
    plt.xlim(0) # Ensure plot starts at time 0
    plt.ylim(0) # Ensure plot starts at RMSD 0
    
    output_filename = "protein_rmsd_all_reps.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Saved all-replicates plot to {output_filename}")
    plt.close()

# --- Plotting Function 2: Averaged Plot (Publication Style) ---

def plot_averages_with_shaded_range(data):
    """
    Generates the averaged plot (one for each ligand) with the average
    of the 3 reps and a shaded region showing the min/max range.
    """
    print("Generating averaged plot...")
    plt.figure(figsize=(10, 7))

    for ligand in data:
        color = ligand["color"]
        name = ligand["name"]
        
        replicate_data = []
        common_time = None
        min_len = float('inf')

        # Load all data for this ligand
        for filepath in ligand["files"]:
            time, rmsd = load_xvg(filepath)
            if time is not None and rmsd is not None:
                replicate_data.append(rmsd)
                if common_time is None:
                    common_time = time
                min_len = min(min_len, len(rmsd))
        
        if not replicate_data:
            print(f"No data found for {name}, skipping.")
            continue

        # Trim all arrays to the shortest length to ensure they match
        common_time = common_time[:min_len]
        replicate_matrix = np.array([rmsd[:min_len] for rmsd in replicate_data])

        # Calculate mean, min, and max
        mean_rmsd = np.mean(replicate_matrix, axis=0)
        min_rmsd = np.min(replicate_matrix, axis=0)
        max_rmsd = np.max(replicate_matrix, axis=0)

        # Plot the average line
        plt.plot(common_time, mean_rmsd, 
                 label=f"{name} (Avg.)", 
                 color=color, 
                 linewidth=2.5)
        
        # Plot the shaded min/max range
        plt.fill_between(common_time, min_rmsd, max_rmsd, 
                         color=color, 
                         alpha=0.2, 
                         label=f"{name} (Range)")

    plt.title("Protein RMSD (Averaged by Ligand)", fontsize=18, pad=20)
    plt.xlabel("Time (ns)", fontsize=14)
    plt.ylabel("Protein RMSD (nm)", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='upper left')
    
    plt.xlim(0)
    plt.ylim(0)

    output_filename = "protein_rmsd_averaged.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Saved averaged plot to {output_filename}")
    plt.close()

# --- Main execution ---
if __name__ == "__main__":
    # --- CHOOSE YOUR PLOT ---
    
    # Option 1: Plot all individual lines (can be crowded)
    #plot_all_replicates(LIGAND_DATA)
    
    # Option 2: Plot averages with shaded range (cleaner for publication)
    # To use this, comment out the line above and uncomment the line below.
    plot_averages_with_shaded_range(LIGAND_DATA)
    
    print("\nPlotting complete.")