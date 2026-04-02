This folder contains all LBDD results and designed molecules, including:
+ The raw pool of 50,000 designed molecules: raw_mega_pool_CNS.csv
+ The filtered pool of 5,389 molecules, categorized into Zone A and Zone B, with max Tanimoto score against the training dataset (Max_Sim_AD) and against the full BindingDB dataset (LBDD_Tanimoto_max) calculated: candidates_with_max_tanimoto_LBDD.csv
+ Full set of 11 re-discovered known inhibitors SMILES, along with their InChI and BDB DOI, Zone category, maximum Tanimoto score, predicted pKi, and experimental pKi: re_discovered_inhibitors.txt, re_discovery_BDB_matched.csv
+ Full set of top 747 top scorers of the LBDD dataset calibrated to pH 7.4 (LBDD_hits_pH_blood), and SwissADME Output (LBDD_cleaned)
+ Along with the code of data processing and graphs demonstrating the distribution of predicted pKi score, and Tanimoto score distribution.