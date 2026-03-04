# Integrating Structure-Based Genetic Algorithms and Reinforcement Learning for De Novo Design of Novel BACE1 Inhibitors

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17823717.svg)](https://doi.org/10.5281/zenodo.17823717)

**Independent Drug Discovery Lab (IDD Lab)** **Authors:** Thang T. Dang, Mai N. Luong

This repository contains the official code, supplemental information, parameter files, and data summaries for the research article: *"Integrating Structure-Based Genetic Algorithms and Reinforcement Learning for De Novo Design of Novel BACE1 Inhibitors"*.

## 📖 Abstract
Alzheimer’s disease (AD) remains a pressing neurodegenerative challenge, with β-secretase 1 (BACE1) serving as a primary therapeutic target. This repository hosts the dual-pronged generative framework that synergistically couples ligand-based reinforcement learning (RL) with structure-based genetic algorithm (GA) evolution to comprehensively explore novel chemical space. It includes all generated datasets, QSAR modeling scripts, molecular docking configurations, and explicit-solvent Molecular Dynamics (MD) / MM/GBSA validation data.

## ⚙️ System Requirements & Installation

To ensure full reproducibility, the Python environment can be perfectly reconstructed using the provided `environment.yml` file. 

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/idd-lab/BACE1_de_novo_design.git](https://github.com/idd-lab/BACE1_de_novo_design.git)
   cd BACE1_de_novo_design

2. Install the Conda environment:
conda env create -f environment.yml
conda activate idd_bace1_pipeline

External Dependencies: While the Python environment handles data processing and machine learning, the following standalone software packages were utilized for physics-based simulations and must be installed separately:
AutoDock Vina (v1.2.3 / v1.2.5)
AutoGrow4 (v4.0.3)
GROMACS (v2023.2 for preparation; v2024.1 for production dynamics)

Gemini said
To answer your question about the images: No, you do not need to download or upload the "badges" at the top of the README. Those links (from shields.io and zenodo.org) are dynamic. When you paste that exact code into GitHub, GitHub will automatically fetch those images from the web and display them as professional, clickable buttons at the top of your repository page.

However, if you ever decide you want to display an actual figure from your paper (like Scheme 1) inside the README, that is when you would need to save the image as a .png, upload it to your repository, and link it. But for the text provided below, everything is fully automated.

Here is the complete, single-block version of your professional README. You can copy this directly into your README.md file on GitHub.

Markdown
# Integrating Structure-Based Genetic Algorithms and Reinforcement Learning for De Novo Design of Novel BACE1 Inhibitors

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17823717.svg)](https://doi.org/10.5281/zenodo.17823717)

**Independent Drug Discovery Lab (IDD Lab)** **Authors:** Thang T. Dang, Mai N. Luong

This repository contains the official code, supplemental information, parameter files, and data summaries for the research article: *"Integrating Structure-Based Genetic Algorithms and Reinforcement Learning for De Novo Design of Novel BACE1 Inhibitors"*.

## 📖 Abstract
Alzheimer’s disease (AD) remains a pressing neurodegenerative challenge, with β-secretase 1 (BACE1) serving as a primary therapeutic target. This repository hosts the dual-pronged generative framework that synergistically couples ligand-based reinforcement learning (RL) with structure-based genetic algorithm (GA) evolution to comprehensively explore novel chemical space. It includes all generated datasets, QSAR modeling scripts, molecular docking configurations, and explicit-solvent Molecular Dynamics (MD) / MM/GBSA validation data.

## ⚙️ System Requirements & Installation

To ensure full reproducibility, the Python environment can be perfectly reconstructed using the provided `environment.yml` file. 

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/idd-lab/BACE1_de_novo_design.git](https://github.com/idd-lab/BACE1_de_novo_design.git)
   cd BACE1_de_novo_design
Install the Conda environment:

Bash
conda env create -f environment.yml
conda activate idd_bace1_pipeline
External Dependencies: While the Python environment handles data processing and machine learning, the following standalone software packages were utilized for physics-based simulations and must be installed separately:

AutoDock Vina (v1.2.3 / v1.2.5)

AutoGrow4 (v4.0.3)

GROMACS (v2023.2 for preparation; v2024.1 for production dynamics)

📂 Repository Structure
The repository is organized into five primary modules corresponding to the methodological pipeline:

0_Curated_Data/ Contains the foundational datasets for both generative pipelines. Includes the BACE1 inhibitors dataset curated from BindingDB (pK 
i
​
  values), the prepared BACE1 protein target (4xxs_charged_minimized.pdb / .pdbqt), H++ server outputs, and fragment libraries utilized for both SBDD and LBDD.

1_Structure_Based_Design/ Note: Due to file size constraints, the complete evolutionary trajectory data for the SBDD pathway is hosted externally on Zenodo. Contains the specific README and access protocols for the AutoGrow4 generational data.

🔗 Zenodo Archive: 10.5281/zenodo.17823717

2_Ligand_Based_Design/ Houses the complete machine learning architecture. Includes the LBDD fragment library, training subsets, generated candidate pools, and independent rediscovery mapping. Contains three executable Google Colab notebooks: Data Processing, QSAR Modeling, and LSTM Molecule Generation / Reinforcement Learning fine-tuning.

3_Hit_Validation/ Contains rigorous post-generation filtering data. Includes ADME and synthetic accessibility (SA) screening data, triplicate exhaustive docking logs and poses, Tanimoto similarity calculations for novelty assessment, and a comprehensive PLIP server interaction map. Included is the script utilized for standardizing candidate protonation states (set_pH_5.py).

4_Molecular_Dynamics/ Contains supporting analytical data for dynamic validation, including RMSD/RMSF graphs, H-bond occupancy data, and MM/GBSA energy decomposition summaries.

Note: The raw 100 ns explicit-solvent MD trajectories for the top candidates (triplicates) exceed GitHub storage limits and are permanently archived on Zenodo:

+ Compound 14XS: 10.5281/zenodo.17824216

+ Compound 32: 10.5281/zenodo.17824339

+ Compound 41: 10.5281/zenodo.17825420

+ Compound 96: 10.5281/zenodo.18851235

+ Compound 73: 10.5281/zenodo.18851674

📜 Citation & Usage
If you utilize the code, generative models, or raw simulation data provided in this repository, please cite the main manuscript alongside the specific Zenodo DOIs associated with the datasets.

@article{Dang2026BACE1,
  title={Integrating Structure-Based Genetic Algorithms and Reinforcement Learning for De Novo Design of Novel BACE1 Inhibitors},
  author={Dang, Thang T. and Luong, Mai N.},
  journal={Journal of Chemical Information and Modeling},
  year={2026},
  note={Submitted}
}
