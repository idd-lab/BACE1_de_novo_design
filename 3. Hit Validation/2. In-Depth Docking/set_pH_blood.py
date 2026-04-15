import os
import dimorphite_dl
import csv

# Define paths for input and output files
input_file = All_hits.smi    #Adjust to your local files
output_file = All_hits_pH_blood.smi

# Define the pH and precision settings
target_ph = 7.4
pka_precision = 1.0
max_variants = 1

# List to store the results
protonated_molecules = []

# Open the input file and process each line
with open(input_file, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        try:
            smiles, identifier = row
            
            # Use Dimorphite-DL's protonate_smiles function
            # Note: Dimorphite-DL uses a pH range. To target a single pH,
            # we set both min_ph and max_ph to the same value.
            protonated_smiles_list = dimorphite_dl.protonate_smiles(
                smiles,
                ph_min=target_ph,
                ph_max=target_ph,
                precision=pka_precision,
                max_variants=max_variants
            )
            
            # Since max_variants is 1, the list should have only one item.
            if protonated_smiles_list:
                protonated_smiles = protonated_smiles_list[0]
                protonated_molecules.append(f"{protonated_smiles}\t{identifier}")
                print(f"Processed {identifier}: {smiles} -> {protonated_smiles}")
            else:
                print(f"No protonation state found for {identifier} at pH {target_ph}")

        except Exception as e:
            print(f"Failed to process line for {row}: {e}")

# Write the results to the output file
with open(output_file, 'w') as out_f:
    for line in protonated_molecules:
        out_f.write(line + '\n')

print(f"\nProtonation complete. Results saved to {output_file}")
