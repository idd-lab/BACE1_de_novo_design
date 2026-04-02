import os
import subprocess

# Define paths
input_file = "/mnt/c/Users/THANG/Desktop/Lead_Optimization_76/re_dock_pH5.smi"
output_dir = "/mnt/c/Users/THANG/Desktop/Lead_Optimization_76/pdb_files"

# Create output directory if it doesn’t exist
os.makedirs(output_dir, exist_ok=True)

# Read the input file and process each line
with open(input_file, 'r') as f:
    for line in f:
        # Check for empty lines to avoid errors
        if not line.strip():
            continue

        try:
            smiles, identifier = line.strip().split('\t')
            
            # Use Open Babel to convert SMILES directly to PDB
            # We use --gen3D to generate 3D coordinates.
            # We do NOT use the --pH flag, so the protonation state from
            # Dimorphite-DL is preserved.
            subprocess.run([
                'obabel',
                '-:' + smiles,
                '-O', os.path.join(output_dir, f"{identifier}.pdb"),
                '--gen3D'
            ], check=True)
            
            print(f"Generated {os.path.join(output_dir, identifier)}.pdb")

        except ValueError:
            print(f"Skipping malformed line: {line.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to process {identifier}: {e}")

print("\nAll conversions complete.")