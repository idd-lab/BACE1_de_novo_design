import pandas as pd
import sys
import os

def parse_decomp_file(input_filepath):
    """
    Parses the gmx_MMPBSA DECOMP.dat file and saves a clean CSV.
    (Version 2.0 - Corrected column indices)
    """
    
    # Define the precise column indices from the header
    # 'Residue' is col 0
    # 'TOTAL' Avg is col 16, Std. Dev is col 17
    COL_INDICES = {
        'Residue': 0,
        'TOTAL_Avg': 16,       # <-- CORRECTED (was 15)
        'TOTAL_Std_Dev': 17,   # <-- CORRECTED (was 16)
        'TOTAL_Std_Err': 18
    }
    
    # Find the start of the DELTAS section
    try:
        with open(input_filepath, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file {input_filepath}: {e}")
        return

    start_index = -1
    for i, line in enumerate(lines):
        if line.strip() == "DELTAS:":
            start_index = i
            break
            
    if start_index == -1:
        print(f"Error: Could not find 'DELTAS:' section in {input_filepath}")
        return

    # Find the data, skipping the 3 header lines after DELTAS:
    data_lines = lines[start_index + 4:]
    
    parsed_data = []
    
    for line in data_lines:
        if line.strip() == "":
            break # Stop at the first blank line (end of section)
        
        cols = line.split(',')
        
        try:
            residue = cols[COL_INDICES['Residue']].strip()
            # Skip empty lines or sub-total lines
            if not residue:
                continue
                
            total_avg = float(cols[COL_INDICES['TOTAL_Avg']])
            total_std_dev = float(cols[COL_INDICES['TOTAL_Std_Dev']])
            
            parsed_data.append({
                'Residue': residue,
                'Total_Avg': total_avg,
                'Total_Std_Dev': total_std_dev
            })
        except (IndexError, ValueError):
            # Reached the end or a non-data line
            continue
            
    # Create a DataFrame and save it
    df = pd.DataFrame(parsed_data)
    
    # Create an output filename
    base_name = os.path.basename(input_filepath)
    output_name = f"CLEAN_{base_name.replace('.dat', '.csv')}"
    output_path = os.path.join(os.path.dirname(input_filepath), output_name)
    
    df.to_csv(output_path, index=False)
    print(f"Successfully parsed '{input_filepath}' -> '{output_path}'")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_decomp_data.py <file1.dat> <file2.dat> ...")
        sys.exit(1)
        
    files_to_process = sys.argv[1:]
    
    for f in files_to_process:
        parse_decomp_file(f)