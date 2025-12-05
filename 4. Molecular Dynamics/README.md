The complete dataset of Molecular Dynamics Simulation data is host on Zenodo for its large size.

The complete dataset of Molecular Dynamics of four compounds 14XS, 32, 80, and 41 is the Supplemental Material for the research "Integrating Structure-Based Genetic Algorithms and Deep Reinforcement Learning for the De Novo Discovery of Novel BACE1 Inhibitors".

Specific DOIs to the respective Zenodo archives:
+ 14XS: 10.5281/zenodo.17824216
+ 32: 10.5281/zenodo.17824339
+ 41: 10.5281/zenodo.17825420
+ 80: 10.5281/zenodo.17826716

----------------------------------------------------------------------------------------------------
Each of these compressed folders includes:

+ Raw and processed Molecular Dynamics trajectory files of each replicate in corresponding folders (e.g. md_rep1.xtc (raw MD trajectory); centered.xtc (centered file); md_processed (processed XTC file))

+ All supporting files of each MD runs (TPR files, MDP files, GRO files, CPT files, TOP files, ITP files)

+ XVG files and PNG images of each replicate's Protein backbone RMSD and Ligand RMSD

+ MMGBSA.IN file specifying input of MMGBSA calculations

+ MMGBSA calculation results (COMPACT_MMXSA_RESULTS.mmxsa; FINAL_DECOMP_MMPBSA.dat; FINAL_RESULTS_MMPBSA.dat) and log files

+ MMGBSA summary files (CLEAN_FINAL_DECOMP_MMPBSA.csv)

+ VMD's hydrogen bonds occupancies processed files and images: hbonds.dat, hbonds-details.dat, and **_rep*_dyad.png provide information on ligand's hydrogen bond interactions with the catalytic dyad, and hbonds_protein.dat, hbonds-details_protein.dat, and **_protein_rep*.png provide information on ligand's hydrogen bond interactions with any residuals
----------------------------------------------------------------------------------------------------

This folder also includes a sub-folder of additional analysis files and results ('Other_data'), comprising:
+ Graphs of protein RMSD and ligand RMSD of each ligand
+ An analysis of MM/GBSA calculation (Table_S3_MMGBSA_Summary.csv)
+ All hydrogen bond occupancies of all replicates analyzed by VMD (h_bond_all.txt)

+ Detailed analysis of decomposition of MM/GBSA calculation and graph of top residue-specific contribution across all ligands
