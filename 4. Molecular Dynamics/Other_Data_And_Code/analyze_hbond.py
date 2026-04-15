import pandas as pd
import numpy as np
import os

# --- 1. CONFIGURATION ---
INPUT_FILE = "h_bond_occupancy_all.txt"
OUTPUT_CSV = "Table_S4_HBond_Summary.csv"

def extract_protein_residue(row):
    """
    Identifies which column contains the protein residue (not the ligand)
    and strips the '-Main' or '-Side' suffix.
    """
    # .strip() added just in case there are invisible trailing spaces in the text file
    donor = str(row['donor']).strip()
    acceptor = str(row['acceptor']).strip()
    
    # Assuming the ligand is labeled as 'UNL' (e.g., UNL377)
    if 'UNL' not in donor:
        target_res = donor
    else:
        target_res = acceptor
        
    # Split by hyphen and take the first part (e.g., 'GLY39-Main' -> 'GLY39')
    return target_res.split('-')[0]

def analyze_hbond_data(filepath, output_path):
    print(f"Reading data from {filepath}...")
    
    # Read the file safely handling variable whitespace
    try:
        df = pd.read_csv(filepath, sep=r'\s+', engine='python')
    except Exception as e:
        print(f"Error loading file: {e}")
        return
    
    # 1. Clean the occupancy column (remove '%' and convert to float)
    df['occupancy'] = df['occupancy'].astype(str).str.replace('%', '').astype(float)
    
    # 2. Extract clean protein residue names
    df['Protein_Residue'] = df.apply(extract_protein_residue, axis=1)

    # --- TASK A: Aggregate All Sub-Interactions ---
    # Sum occupancies for the SAME residue in the SAME rep (combining Main/Side, Donor/Acceptor)
    res_aggregated = df.groupby(['Compound', 'Rep', 'Protein_Residue'])['occupancy'].sum().reset_index()
    
    # Calculate Total Occupancy per Rep
    rep_totals = res_aggregated.groupby(['Compound', 'Rep'])['occupancy'].sum().reset_index()
    rep_totals.rename(columns={'occupancy': 'Total_Rep_Occupancy'}, inplace=True)
    
    # --- NEW TASK B: Extract Catalytic Dyad (ASH37 & ASP224) Occupancies ---
    # Pivot the data so residues become columns, allowing us to easily pull the dyad
    pivot_res = res_aggregated.pivot(index=['Compound', 'Rep'], columns='Protein_Residue', values='occupancy').fillna(0).reset_index()
    
    # Failsafe: If a rep completely lost the H-bond, the column might not exist, so we force it to 0.0
    if 'ASH37' not in pivot_res.columns:
        pivot_res['ASH37'] = 0.0
    if 'ASP224' not in pivot_res.columns:
        pivot_res['ASP224'] = 0.0
        
    # Extract only the dyad columns
    dyad_stats = pivot_res[['Compound', 'Rep', 'ASH37', 'ASP224']].copy()
    dyad_stats.rename(columns={'ASH37': 'ASH37_Occupancy', 'ASP224': 'ASP224_Occupancy'}, inplace=True)
    
    # Calculate total dyad interaction
    dyad_stats['Dyad_Total_Occupancy'] = dyad_stats['ASH37_Occupancy'] + dyad_stats['ASP224_Occupancy']

    # --- TASK C: Top 3 Residues per Rep ---
    # Sort by occupancy descending, then group by Compound and Rep, and take the top 3
    top_residues = res_aggregated.sort_values(['Compound', 'Rep', 'occupancy'], ascending=[True, True, False])
    top_3_per_rep = top_residues.groupby(['Compound', 'Rep']).head(3)
    
    def format_top_3(group):
        items = [f"{row['Protein_Residue']} ({row['occupancy']:.2f}%)" for _, row in group.iterrows()]
        return " | ".join(items)
        
    top_3_strings = top_3_per_rep.groupby(['Compound', 'Rep']).apply(format_top_3).reset_index(name='Top_3_Interactions')
    
    # Merge Totals, Dyad Stats, and Top 3 Interactions
    rep_summary = pd.merge(rep_totals, dyad_stats, on=['Compound', 'Rep'])
    rep_summary = pd.merge(rep_summary, top_3_strings, on=['Compound', 'Rep'])

    # --- TASK D: Mean and SD across the three reps for each compound ---
    # Calculate Mean and Sample SD (ddof=1)
    compound_stats = rep_totals.groupby('Compound')['Total_Rep_Occupancy'].agg(
        Mean_Occupancy='mean',
        SD_Occupancy=lambda x: np.std(x, ddof=1) if len(x) > 1 else 0.0
    ).reset_index()
    
    # Format Mean ± SD for publication
    compound_stats['Total_Occupancy (Mean ± SD)'] = compound_stats.apply(
        lambda row: f"{row['Mean_Occupancy']:.2f}% ± {row['SD_Occupancy']:.2f}%", axis=1
    )
    
    # Merge the compound stats back into the full report
    final_report = pd.merge(rep_summary, compound_stats[['Compound', 'Total_Occupancy (Mean ± SD)']], on='Compound')
    
    # Reorder columns for a clean, logical presentation
    final_report = final_report[[
        'Compound', 'Total_Occupancy (Mean ± SD)', 'Rep', 'Total_Rep_Occupancy', 
        'ASH37_Occupancy', 'ASP224_Occupancy', 'Dyad_Total_Occupancy',
        'Top_3_Interactions'
    ]]
    
    # --- OUTPUT ---
    print("\n--- H-BOND OCCUPANCY SUMMARY ---")
    print(final_report.to_string(index=False))
    
    final_report.to_csv(output_path, index=False)
    print(f"\nSaved detailed H-bond report to {output_path}")

if __name__ == "__main__":
    analyze_hbond_data(INPUT_FILE, OUTPUT_CSV)
