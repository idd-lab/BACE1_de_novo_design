import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Setup Publication-Quality Styling
sns.set_theme(style="ticks", context="paper", font_scale=1.3)

# 2. Define Paths (Ubuntu/WSL format)
input_path = "/mnt/c/Users/THANG/Desktop/qsar/cleaned/Designed_Molecules_cleaned/candidates_with_max_tanimoto_LBDD.csv"
output_path = "/mnt/c/Users/THANG/Desktop/qsar/cleaned/Designed_Molecules_cleaned/Figure_LBDD_Generative_Novelty_Distribution.png"

# 3. Load Data
df = pd.read_csv(input_path)

# Clean up the Zone names just in case they have extra text like "Zone A (Safe)"
# This ensures our color mapping works perfectly
df['Zone_Clean'] = df['Zone'].astype(str).apply(
    lambda x: 'Zone A' if 'Zone A' in x else ('Zone B' if 'Zone B' in x else 'Other')
)

# 4. Initialize the Figure
plt.figure(figsize=(8, 6))

# Define the custom color palette for the zones
# Using standard matplotlib named colors for light green and light blue
zone_colors = {
    'Zone A': '#2ecc71',
    'Zone B': '#3498db'
}

# 5. Plot Histogram with Hue for Zones
ax = sns.histplot(
    data=df, 
    x='LBDD_Tanimoto_max', 
    hue='Zone_Clean',
    palette=zone_colors,
    bins=30,             # Adjust this to change the bar width
    multiple="stack",    # Stacks the bars so total counts are accurate and colors don't hide each other
    edgecolor='white',   # Distinct borders for the bars
    linewidth=1.2,
    alpha=0.85           # Slightly less transparent to make the light colors pop
)

# 6. Customize Labels and Titles
plt.xlabel('Maximum Tanimoto Similarity', fontweight='bold', labelpad=10)
plt.ylabel('Number of Compounds', fontweight='bold', labelpad=10)
plt.title('(A) LBDD Generative Novelty Distribution', fontweight='bold', pad=15)

# 7. Add a light grid
# Setting zorder behind the bars and using a low alpha (0.3) keeps it subtle
plt.grid(True, axis='both', linestyle='--', color='gray', alpha=0.3, zorder=0)

# 8. Customize the Legend (Move to top left)
sns.move_legend(ax, "upper right", title=None, frameon=True, framealpha=0.9)

# 9. Clean up the axes (Optional: uncomment if you prefer the open look)
# sns.despine()

# 10. Save with High Resolution (300 DPI for publication)
plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=False)

print(f"Graph successfully generated and saved to:\n{output_path}")

# Optional: Display the plot if running in an interactive environment (like Jupyter)
# plt.show()