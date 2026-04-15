import pandas as pd

# 1. Define WSL/Ubuntu Paths
input_path = "Docking_Scores.xlsx"    #Copy your summaries to an Excel file for analysis, put the file here
output_path = "Docking_Scores_Summary.csv"

print("Loading raw docking scores...")
# 2. Load Data
# Using pandas to read the Excel file. 
df = pd.read_excel(input_path)

# 3. Identify the score columns
# These match the standard output headers from your data
score_cols = ['Best Docking Score 0', 'Best Docking Score 1', 'Best Docking Score 2']

# 4. Initialize a new DataFrame for the clean summary
results_df = pd.DataFrame()

# The first column is the Ligand ID (pandas handles duplicated column names gracefully)
# We use iloc[:, 0] to grab the very first column regardless of how pandas named the duplicates
results_df['Ligand'] = df.iloc[:, 0]

print("Calculating Mean and Standard Deviation across triplicates...")
# 5. Calculate Mean and Standard Deviation
# axis=1 ensures the calculation is done row-by-row across the three triplicate columns
results_df['Mean_DS'] = df[score_cols].mean(axis=1)
results_df['SD_DS'] = df[score_cols].std(axis=1)

# Optional: Round the results to 4 decimal places for clean reporting in your manuscript
results_df['Mean_DS'] = results_df['Mean_DS'].round(4)
results_df['SD_DS'] = results_df['SD_DS'].round(4)

# 6. Save the summary to a CSV
results_df.to_csv(output_path, index=False)

print(f"Success! Averaged docking scores saved to:\n{output_path}")
