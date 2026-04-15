This folder contains all Extensive Docking data, including the triplicate, scripts, workflow, and structures.

Workflow Guide:

- Put ligand SMILES and an identifier (name) into re_dock.smi, separated by a /tab sign
- set_pH_5.py (Customizable to your protein's pH): using Dimorphite-DL to calibrate pH level 
- generate_pdb.py: using OpenBabel to convert SMILES structure to 3D PDB files
- Docking parameters: Customizable in config.txt
- dock_ligands.py: dock ligands using AutoDock Vina
- analyze_docking.py: summarize docking scores.
- average_docking.py: calculate average docking scores and standard deviation. You must copy all rep's docked csv content onto the file Docking_Summary.csv in the given format to use.
