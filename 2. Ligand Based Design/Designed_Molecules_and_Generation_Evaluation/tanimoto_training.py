import pandas as pd
import numpy as np
import os

# --- CONFIGURATION ---
# Converted Windows path to Ubuntu/WSL path
INPUT_FILE = "/mnt/c/Users/THANG/Desktop/qsar/cleaned/Designed_Molecules_cleaned/candidates_zoned_full_CNS.csv"

def analyze_tanimoto(filepath):
    print(f"Reading data from {filepath}...\n")
    
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return
    except Exception as e:
        print(f"Error loading file: {e}")
        return
    
    # Ensure the required columns exist
    if 'Max_Sim_AD' not in df.columns or 'Zone' not in df.columns:
        print("Error: Required columns ('Max_Sim_AD' or 'Zone') not found in the dataset.")
        print(f"Available columns: {df.columns.tolist()}")
        return
        
    # Helper function to calculate and format statistics
    def get_stats(data_series, group_name):
        if data_series.empty:
            return f"--- {group_name} ---\nNo data available.\n"
        
        n = len(data_series)
        val_min = data_series.min()
        val_max = data_series.max()
        val_mean = data_series.mean()
        
        # Sample standard deviation (ddof=1) for rigorous publication standards
        val_std = data_series.std(ddof=1) if n > 1 else 0.0
        
        # Standard Error of the Mean (SEM) - Optional but good for high-impact journals
        val_sem = val_std / np.sqrt(n) if n > 0 else 0.0
        
        return (f"--- {group_name} (N = {n}) ---\n"
                f"Range: {val_min:.4f} to {val_max:.4f}\n"
                f"Mean:  {val_mean:.4f}\n"
                f"SD:    {val_std:.4f}\n"
                f"SEM:   {val_sem:.4f}\n")

    # (a) All compounds
    print(get_stats(df['Max_Sim_AD'], "All Compounds"))
    
    # (b) Zone A compounds
    # Ensure the casing matches your CSV (e.g., 'Zone A' vs 'A' - adjust if necessary)
    zone_a_df = df[df['Zone'].astype(str).str.contains('A', na=False)]
    print(get_stats(zone_a_df['Max_Sim_AD'], "Zone A Compounds"))
    
    # (c) Zone B compounds
    zone_b_df = df[df['Zone'].astype(str).str.contains('B', na=False)]
    print(get_stats(zone_b_df['Max_Sim_AD'], "Zone B Compounds"))

if __name__ == "__main__":
    analyze_tanimoto(INPUT_FILE)