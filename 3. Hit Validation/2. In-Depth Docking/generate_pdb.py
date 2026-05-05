import os
import sys

# Try importing RDKit
try:
    from rdkit import Chem
    from rdkit.Chem import AllChem
except ImportError:
    print("Error: RDKit not found. Please ensure your RDKit environment is activated.")
    sys.exit(1)

# Define paths
input_file = "docking_list_pH.smi"
output_dir = "pdb_files"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def generate_3d_with_rdkit(smiles_string, output_pdb):
    """
    Uses RDKit to generate a 3D conformation.
    """
    mol = Chem.MolFromSmiles(smiles_string)
    if not mol:
        raise ValueError("RDKit could not parse SMILES.")

    # Add Hydrogens (Crucial for 3D embedding)
    mol = Chem.AddHs(mol)

    # Generate 3D Coords using ETKDGv3
    params = AllChem.ETKDGv3()
    params.useRandomCoords = True # Helps if standard embedding gets stuck
    params.randomSeed = 0xf00d    # Deterministic seed
    
    embed_stat = AllChem.EmbedMolecule(mol, params)
    
    if embed_stat != 0:
        print("   > Warning: Standard embedding failed. Trying random coordinates...")
        # Fallback to random coordinates
        params.useRandomCoords = True
        AllChem.EmbedMolecule(mol, params)
    
    # Energy Minimize to clean up geometry
    try:
        # Check if MMFF94 parameters are available for this molecule
        if AllChem.MMFFHasAllParams(mol):
            AllChem.MMFFOptimizeMolecule(mol)
        else:
            # Fallback to UFF if MMFF is missing parameters for certain atoms
            AllChem.UFFOptimizeMolecule(mol)
    except Exception as e:
        print(f"   > Warning: Minimization failed ({e}). Proceeding with unminimized 3D coords.")
        
    # Write to PDB
    Chem.MolToPDBFile(mol, output_pdb)

# Read the input file and process each line
print("Starting 3D conversion pipeline using RDKit...\n")
with open(input_file, 'r') as f:
    for line in f:
        # Check for empty lines
        if not line.strip():
            continue

        try:
            # Safely unpack the line (handles variable whitespace/tabs)
            parts = line.strip().split()
            if len(parts) >= 2:
                smiles = parts[0]
                identifier = parts[1]
            else:
                print(f"Skipping malformed line: {line.strip()}")
                continue
            
            output_pdb = os.path.join(output_dir, f"{identifier}.pdb")
            print(f"Processing {identifier}...")
            
            # Generate 3D and save
            generate_3d_with_rdkit(smiles, output_pdb)
            print(f"   > Successfully saved {output_pdb}")

        except ValueError as ve:
            print(f"   > Skipping {identifier}: {ve}")
        except Exception as e:
            print(f"   > Failed to process {identifier}: {e}")

print("\nAll conversions complete.")