## 📂 Data Availability
The complete dataset of Structure Based Design data is host on Zenodo for its large size.


### **[>> ACCESS FULL DATASET HERE (Zenodo) <<](https://zenodo.org/records/17823717)**
**(DOI: 10.5281/zenodo.17823717)**

The complete dataset of structure-based de novo design in the research "Integrating Structure-Based Genetic Algorithms and Deep Reinforcement Learning for the De Novo Discovery of Novel BACE1 Inhibitors".

The compressed folder includes:

+ AutoGrow runs from Run 0 to Run 8, along with all PDB files, docking files, and parameter vars.json files (within each Run folder)

+ Processed protein PDB file (4xxs_charged_minimized.pdb) and fragment library (augmented300.smi) for running AutoGrow

+ SILE re-scoring file (lig_efficiency.py) for AutoGrow run, editted on AutoGrow's default lig_efficiency file

+ SILE progression graphs over generations of each run (data_line_plot.png within each Run folder)

+ A complete dataset of 5,020 unique generated ligands (5020_designed_ligands.txt) along with their docking scores and heavy atom count

+ Docking Score distribution graph of all 5,020 generated ligands 

+SILE Validation plot against Docking Score and Ligand Efficiency and the fitting data (Figure4_Docking_Score_Distribution.pdf and fit_results_sile_validation.txt)

*GUIDE TO REPRODUCE AUTOGROW4 RUN/SETUP:

- Download and setup AutoGrow4 (https://github.com/durrantlab/autogrow4) according to the developer's instruction

- Copy the vars.json from our dataset or create a new one, adjust paths according to your protein files, fragment libraries, and tools

- How to apply the Size-Independent Ligand Efficiency score: REPLACE AutoGrow4's default lig_efficiency.py file with ours, and enable (rescore_lig_efficiency": true) in the vars.json file
