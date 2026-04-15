import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Setup Publication-Quality Styling
# 'ticks' provides a clean background without distracting gridlines
sns.set_theme(style="ticks", context="paper", font_scale=1.3)

# 2. Define Paths (Ubuntu/WSL format)
input_path = "SBDD_Tanimoto_max.csv"
output_path = "Figure_SBDD_Generative_Novelty_Distribution.png"

# 3. Load Data
df = pd.read_csv(input_path)

# 4. Initialize the Figure
plt.figure(figsize=(8, 6))

# Define the pinkish-red color
# #D81B60 is a striking, colorblind-friendly pinkish-red often used in scientific plots
fill_color = "lightcoral" 

# 5. Plot Histogram with KDE
sns.histplot(
    data=df, 
    x='Tanimoto_max', 
    bins=30,             # Adjust this to change the bar width
  #  kde=True,            # Adds the smooth density curve
    color=fill_color,
    edgecolor='white',   # Distinct borders for the bars
    linewidth=1.2,
    alpha=0.75           # Slight transparency 
)

# 6. Customize Labels and Titles
plt.xlabel('Maximum Tanimoto Similarity', fontweight='bold', labelpad=10)
plt.ylabel('Number of Compounds', fontweight='bold', labelpad=10)
plt.title('(B) SBDD Generative Novelty Distribution', fontweight='bold', pad=15)

plt.grid(True, axis='both', linestyle='--', color='gray', alpha=0.3, zorder=0)

# 7. Clean up the axes (removes top and right borders)
# sns.despine()

# 8. Save with High Resolution (300 DPI for publication)
plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=False)

print(f"Graph successfully generated and saved to:\n{output_path}")

# Optional: Display the plot if running in an interactive environment (like Jupyter)
# plt.show()
