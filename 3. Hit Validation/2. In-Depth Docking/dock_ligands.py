import os
import subprocess

# Define paths (adjusted for WSL)
pdb_dir = "/mnt/c/Users/THANG/Desktop/Lead_Optimization_76/pdb_files"
pdbqt_dir = "/mnt/c/Users/THANG/Desktop/Lead_Optimization_76/pdbqt_files"
docking_results_dir = "/mnt/c/Users/THANG/Desktop/Lead_Optimization_76/docking_results"
config_file = "/mnt/c/Users/THANG/Desktop/Lead_Optimization_76/config.txt"
receptor_path = "/mnt/c/Users/THANG/Desktop/Lead_Optimization_76/4xxs_charged_minimized.pdbqt"

# Create directories if they don't exist
for directory in [pdbqt_dir, docking_results_dir]:
    os.makedirs(directory, exist_ok=True)

# Get list of PDB files
pdb_files = [f for f in os.listdir(pdb_dir) if f.endswith('.pdb')]

for pdb_file in pdb_files:
    base = os.path.splitext(pdb_file)[0]
    pdb_path = os.path.join(pdb_dir, pdb_file)
    pdbqt_path = os.path.join(pdbqt_dir, f"{base}.pdbqt")
    docked_path = os.path.join(docking_results_dir, f"{base}_docked.pdbqt")
    log_path = os.path.join(docking_results_dir, f"{base}_log.txt")

    # Convert PDB to PDBQT with Gasteiger charges
    try:
        subprocess.run([
            'obabel',
            '-i', 'pdb',
            pdb_path,
            '-o', 'pdbqt',
            '-O', pdbqt_path,
            '--partialcharge', 'gasteiger'
        ], check=True)
        print(f"Converted {pdb_file} to PDBQT")
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert {pdb_file}: {e}")
        continue

    # Run docking and save log
    if not os.path.exists(config_file):
        print(f"Config file {config_file} not found!")
        continue
    try:
        with open(log_path, 'w') as log_file:
            subprocess.run([
                'vina',
                '--config', config_file,
                '--ligand', pdbqt_path,
                '--out', docked_path,
                '--receptor', receptor_path
            ], stdout=log_file, stderr=log_file, check=True)
        print(f"Docked {base}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to dock {base}: {e}")