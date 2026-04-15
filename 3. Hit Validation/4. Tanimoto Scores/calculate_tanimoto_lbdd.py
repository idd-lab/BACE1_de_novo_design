import pandas as pd

# Define WSL/Ubuntu Path
file_path = "candidates_with_max_tanimoto_LBDD.csv"

def calculate_and_print_stats(series, group_name):
    """Calculates and prints the range, mean, and standard deviation for a given pandas Series."""
    # Drop any NaN values just in case there were parsing errors
    clean_series = series.dropna()
    
    if clean_series.empty:
        print(f"--- {group_name} ---")
        print("No valid data available.\n")
        return

    val_min = clean_series.min()
    val_max = clean_series.max()
    val_mean = clean_series.mean()
    val_std = clean_series.std()
    
    print(f"--- {group_name} ---")
    print(f"Range: [{val_min:.4f}, {val_max:.4f}] (Span: {val_max - val_min:.4f})")
    print(f"Mean:  {val_mean:.4f}")
    print(f"SD:    {val_std:.4f}\n")

if __name__ == "__main__":
    print("Loading data...\n")
    df = pd.read_csv(file_path)

    # 1. Overall Dataset
    calculate_and_print_stats(df['LBDD_Tanimoto_max'], "Entire Dataset")

    # 2. Zone Groups
    # Using .str.contains in case the column has extra text like "Zone A (Safe)"
    zone_a_data = df[df['Zone'].astype(str).str.contains('Zone A')]['LBDD_Tanimoto_max']
    zone_b_data = df[df['Zone'].astype(str).str.contains('Zone B')]['LBDD_Tanimoto_max']

    calculate_and_print_stats(zone_a_data, "Zone A")
    calculate_and_print_stats(zone_b_data, "Zone B")
