import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.lines as mlines
import os

# --- WSL Paths ---
molecules_csv = "All_hits_ADME.csv"
output_image = "BOILED_Egg_All_Hits_JCIM.png"

# --- Parametric Ellipse Generator ---
# Preserves mathematical integrity from Daina & Zoete (2016) Figures S1 & S2
def get_ellipse_coords(xc, yc, a, b, angle_degrees, num_points=1000):
    theta = np.radians(angle_degrees)
    t = np.linspace(0, 2 * np.pi, num_points)
    
    # Parametric equations for a rotated ellipse
    x = xc + a * np.cos(t) * np.cos(theta) - b * np.sin(t) * np.sin(theta)
    y = yc + a * np.cos(t) * np.sin(theta) + b * np.sin(t) * np.cos(theta)
    
    return np.column_stack((x, y))

# --- 1. Generate Exact BOILED-Egg Boundaries ---

# Figure S1: HIA Ellipse (Egg White)
hia_coords = get_ellipse_coords(xc=71.051, yc=2.292, 
                                a=142.081/2, b=8.740/2, 
                                angle_degrees=-1.031325)

# Figure S2: BBB Ellipse (Egg Yolk)
bbb_coords = get_ellipse_coords(xc=38.117, yc=3.177, 
                                a=82.061/2, b=5.557/2, 
                                angle_degrees=-0.171887)

# --- 2. Load Molecule Data ---
try:
    df_mols = pd.read_csv(molecules_csv)
except FileNotFoundError:
    raise FileNotFoundError(f"Could not find the molecule file at: {molecules_csv}")

# --- 3. Construct the Plot ---
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_facecolor('#E5E7E9') # Non-permeant grey background

# Add the mathematically exact polygons
hia_poly = Polygon(hia_coords, closed=True, edgecolor='black', facecolor='white', linewidth=1.5, zorder=1)
bbb_poly = Polygon(bbb_coords, closed=True, edgecolor='black', facecolor='#FCEB69', linewidth=1.5, zorder=2)

ax.add_patch(hia_poly)
ax.add_patch(bbb_poly)

# --- 4. SwissADME P-gp Color Coding ---
# Blue dots = PGP+, Red dots = PGP-
if 'Pgp substrate' in df_mols.columns:
    colors = df_mols['Pgp substrate'].apply(lambda x: '#3232FF' if str(x).strip().lower() == 'yes' else '#FF3232')
else:
    colors = '#FF3232'

# Plot all molecules (No annotations to prevent clutter)
# Slightly reduced marker size (s=60) since there are more hits to display
scatter = ax.scatter(df_mols['TPSA'], df_mols['WLOGP'], 
                     c=colors, edgecolors='black', 
                     s=60, zorder=3, alpha=0.85)

# --- 5. Format Axes to SwissADME Standards ---
ax.set_xlim(-10, 200)
ax.set_ylim(-4, 8)

ax.set_xlabel('TPSA ($\AA^2$)', fontsize=14, fontweight='bold')
ax.set_ylabel('WLOGP', fontsize=14, fontweight='bold')
ax.set_title('BOILED-Egg Predictive Model (Hit Validation)', fontsize=16, fontweight='bold')

# --- 6. Legend ---
white_patch = mlines.Line2D([], [], color='#E5E7E9', marker='o', markerfacecolor='white', markeredgecolor='k', markersize=12, label='HIA Permeant (GI)')
yolk_patch = mlines.Line2D([], [], color='#E5E7E9', marker='o', markerfacecolor='#FCEB69', markeredgecolor='k', markersize=12, label='BBB Permeant (Brain)')
pgp_yes = mlines.Line2D([], [], color='w', marker='o', markerfacecolor='#3232FF', markeredgecolor='k', markersize=10, label='PGP+ (Effluxed)')
pgp_no = mlines.Line2D([], [], color='w', marker='o', markerfacecolor='#FF3232', markeredgecolor='k', markersize=10, label='PGP- (Not effluxed)')
ax.legend(handles=[white_patch, yolk_patch, pgp_yes, pgp_no], loc='upper right', frameon=True, facecolor='white', framealpha=0.95, fontsize=11)

# --- 7. High-Resolution Export ---
plt.tight_layout()
plt.savefig(output_image, dpi=300, format='png', bbox_inches='tight')
print(f"Plot for all hits successfully saved to: {output_image}")

plt.show()
