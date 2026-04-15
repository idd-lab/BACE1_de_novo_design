import os
import re
import csv

# Define the directory containing the log files
directory = "docking_results_3"    #Adjust to your docked folder

# Initialize a list to store ligand names and their best docking scores
results = []

# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        # Extract the ligand name by removing "_log.txt" from the filename
        ligand_name = filename.replace("_log.txt", "")
        log_file_path = os.path.join(directory, filename)
        
        try:
            with open(log_file_path, 'r') as file:
                for line in file:
                    # Look for the line starting with "   1" to get the best docking score
                    match = re.search(r'^\s*1\s+(-?\d+\.\d+)', line)
                    if match:
                        best_score = float(match.group(1))
                        results.append((ligand_name, best_score))
                        break
                else:
                    print(f"No docking score found in {filename}")
        except Exception as e:
            print(f"Error reading {filename}: {e}")

# Sort the results by the best docking score (ascending order)
results.sort(key=lambda x: x[1])

# Write the results to a CSV file
output_file = os.path.join(directory, "docking_summary.csv")
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Ligand", "Best Docking Score"])
    for ligand, score in results:
        writer.writerow([ligand, score])

print(f"Summary saved to {output_file}")
