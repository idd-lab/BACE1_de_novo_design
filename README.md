Markdown
# A Dual-Paradigm De Novo Design Workflow: Exploring Chemical Space via Parallel Ligand- and Structure-Based Approaches on BACE1

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17823717.svg)](https://doi.org/10.5281/zenodo.17823717)

**Independent Drug Discovery Lab (IDD Lab)** **Authors:** Thang T. Dang, Mai N. Luong

This repository contains the official code, supplemental information, parameter files, and data summaries for the research article: *"A Dual-Paradigm De Novo Design Workflow: Exploring Chemical Space via Parallel Ligand- and Structure-Based Approaches on BACE1"*.

## 📖 Abstract
Despite the rapid proliferation of generative algorithms, a persistent translational gap remains between computational method development and practical application in drug design, leading to a need for generalized, ready-to-deploy workflows. 
This repository hosts the dual-pronged generative framework that synergistically couples ligand-based reinforcement learning (RL) with structure-based genetic algorithm (GA) evolution to comprehensively explore novel chemical space. It includes all generated datasets, QSAR modeling scripts, molecular docking configurations, and explicit-solvent Molecular Dynamics (MD) / MM/GBSA validation data.

## ⚙️ System Requirements & Installation

To ensure full reproducibility, the Python environment can be perfectly reconstructed using the provided `environment.yml` file. 

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/idd-lab/BACE1_de_novo_design.git](https://github.com/idd-lab/BACE1_de_novo_design.git)
   cd BACE1_de_novo_design
   
2. **Install Conda environment:**

Bash
conda env create -f environment.yml
conda activate idd_bace1_pipeline
External Dependencies: While the Python environment handles data processing and machine learning, the following standalone software packages were utilized for physics-based simulations and must be installed separately:

AutoDock Vina (v1.2.3 / v1.2.5)

AutoGrow4 (v4.0.3)

GROMACS (v2023.2 for preparation; v2024.1 for production dynamics)

VMD (v1.9.3) - Required for H-bond occupancy analysis

UCSF ChimeraX (v1.11.1) - Required for structural alignment

LigPlot+ (v2.3.1) - Required for 2D interaction mapping

🌐 Web Servers Utilized
Certain steps in the validation cascade were executed via public web servers:

H++ Server: For predicting optimal active-site protonation states at pH 5.0. (http://newbiophysics.cs.vt.edu/H++/)

SwissADME: For BOILED-Egg BBB permeability and Synthetic Accessibility (SA) filtering. (https://www.swissadme.ch/)

PLIP Server: For automated 3D protein-ligand interaction profiling. (https://plip-tool.biotec.tu-dresden.de/plip-web/plip/index)

📂 Repository Structure
The repository is organized into five primary modules corresponding to the methodological pipeline:

0_Curated_Data/ Contains the foundational datasets for both generative pipelines. Includes the BACE1 inhibitors dataset curated from BindingDB (pKi values), the prepared BACE1 protein target (4xxs_charged_minimized.pdb / .pdbqt), H++ server outputs, fragment libraries utilized for both SBDD and LBDD, and code for reproducibility.

1_Structure_Based_Design/ Note: Due to file size constraints, the complete evolutionary trajectory data for the SBDD pathway is hosted externally on Zenodo. Contains the specific README and access protocols for the AutoGrow4 generational data.

🔗 Zenodo Archive: 10.5281/zenodo.17823717

2_Ligand_Based_Design/ Houses the complete machine learning architecture. Includes the LBDD fragment library, training subsets, generated candidate pools, and independent rediscovery mapping. Contains three executable Google Colab notebooks: Data Processing, QSAR Modeling, and LSTM Molecule Generation / Reinforcement Learning fine-tuning.

3_Hit_Validation/ Contains rigorous post-generation filtering data. Includes ADME and synthetic accessibility (SA) screening data, triplicate exhaustive docking logs and poses, Tanimoto similarity calculations for novelty assessment, and a comprehensive PLIP server interaction map. Included is the script utilized for standardizing candidate protonation states (set_pH_5.py), docking configuration (config.txt), and full docking instruction.

4_Molecular_Dynamics/ Contains supporting analytical data for dynamic validation, including RMSD/RMSF graphs, H-bond occupancy data, and MM/GBSA energy decomposition summaries. Colab Notebooks for MD production are also provided.

Note: The raw 100 ns explicit-solvent MD trajectories for the top candidates (triplicates) exceed GitHub storage limits and are permanently archived on Zenodo:

+ Compound 14XS: 10.5281/zenodo.17824216

+ Compound 32: 10.5281/zenodo.17824339

+ Compound 41: 10.5281/zenodo.17825420

+ Compound 96: 10.5281/zenodo.18851235

+ Compound 73: 10.5281/zenodo.18851674
  
+ Compound 104: 10.5281/zenodo.19382117
  
+ Verubecestat: 10.5281/zenodo.19384070

5_Colab_Notebooks/ Summarizes all Colab Notebooks in LBDD pipeline and MD production, and post-MD processing workflow and procedure.

Other Python scripts for specific procedures with instructions of use are stored in their respective folders (most scripts only require updating paths according to your local machine).


📜 Citation & Usage
If you utilize the code, generative models, or raw simulation data provided in this repository, please cite the main manuscript alongside the specific Zenodo DOIs associated with the datasets.

@article{Dang2026BACE1,
  title={A Dual-Paradigm De Novo Design Workflow: Exploring Chemical Space via Parallel Ligand- and Structure-Based Approaches on BACE1},
  author={Dang, Thang T. and Luong, Mai N.},
  journal={Journal of Computational Chemistry},
  year={2026},
  note={Under Review}
}
