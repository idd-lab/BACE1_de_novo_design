# BACE1_de_novo_design**
**Integrating Structure-Based Genetic Algorithms and Deep Reinforcement Learning for the De Novo Discovery of Novel BACE1 Inhibitor Scaffolds**
Supplemental Material Repository

This repository contains the supplemental information, parameter files, and data summaries for the research article: "Integrating Structure-Based Genetic Algorithms and Deep Reinforcement Learning for the De Novo Discovery of Novel BACE1 Inhibitors".

Abstract: Synergistic de novo design of BACE1 inhibitors using structure-based evolution and deep reinforcement learning. Includes all generated datasets, docking/MD/MMGBSA validation data, and analysis pipelines.

📂 Repository Structure
The repository comprises five main component folders:

0. Curated Data: includes starting dataset for both pathway runs.
It includes the dataset of inhibitors and Ki curated from BindingDB (inhibitors_with_pKi_bindingDB), protein PDB files for AutoGrow (4xxs_charged_minimized), H++ server output and parameters, fragment libraries from both SBDD and LBDD generations and prior parent files.

1. Structure Based Design: due to its size, the data for this pathway would be hosted by Zenodo.
You can find the specific link or DOI to the data on Zenodo in the README file within the 1.Structure Based Design folder, or you can access it here: https://zenodo.org/records/17823717 (DOI: 10.5281/zenodo.17823717)
See the README file in the directory for specific content.

2. Ligand Based Design: includes data on the fragment library of LBDD, training molecules, designed molecules from this pathway, scoring, and parameter files (JOBLIB, H5, PKL, NPY).

3. Hit Validation: comprises data on ADME screening of hit compounds, docking results and files of each candidate (all three replicates), leads' poses for examination (including a comprehensive output file from PLIP server listing all interactions), and the Tanimoto Scores calculations of each pathway.
Docking protein file (4xxs_charged_minimized.pdbqt) and docking configuration file (config.txt) are also included with the script for calibrating pH of lead compounds (set_pH_5.py).

4. Molecular Dynamics: similarly, each compound's three replicates are stored in a different Zenodo archive. The folder also includes supplement data in the sub-folder 'Other_data' like graphs, MMGBSA summary, and decomposition analysis.
Specific DOIs to the respective Zenodo archives:
- 14XS: 10.5281/zenodo.17824216
- 32: 10.5281/zenodo.17824339
- 41: 10.5281/zenodo.17825420
- 80: 10.5281/zenodo.17826716
