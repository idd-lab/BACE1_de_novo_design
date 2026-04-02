import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import os

# 1. WSL Paths
base_dir = "/mnt/d/Archive/github_data/3. Hit Validation/3. Leads Pose Examination"

# Define the exact layout for the 6 PLIP 3D Poses (2 Rows, 3 Columns)
img_paths = [
    # ROW 1 (SBDD Candidates): (A), (B), (C)
    os.path.join(base_dir, "14XS/14XS_PLIP.png"),
    os.path.join(base_dir, "41/41_PLIP.png"),
    os.path.join(base_dir, "32/32_PLIP.png"),
    
    # ROW 2 (LBDD Candidates): (D), (E), (F)
    os.path.join(base_dir, "104/104_PLIP.png"),
    os.path.join(base_dir, "96/96_PLIP.png"),
    os.path.join(base_dir, "73/73_PLIP.png")
]

output_path = os.path.join(base_dir, "Figure_8_PLIP_Poses_2x3_600DPI.png")

# Compound names corresponding to the panels
compound_labels = [
    "Compound 14XS", "Compound 41", "Compound 32",
    "Compound 104", "Compound 96", "Compound 73"
]

# 2. Load Images
images = []
for p in img_paths:
    try:
        images.append(Image.open(p))
    except FileNotFoundError:
        print(f"⚠️ ERROR: Could not find {p}")
        exit()

# 3. Setup the Grid (2 Rows, 3 Columns)
fig, axes = plt.subplots(2, 3, figsize=(6.69, 4.5), dpi=600)
axes = axes.flatten()

# Corner labels A through F
panel_letters = ['(A)', '(B)', '(C)', '(D)', '(E)', '(F)']

print("Stitching 6-panel PLIP figure (Figure 8)...")

for i in range(6):
    axes[i].imshow(images[i])
    axes[i].axis('off') 
    
    # Pushed OUTSIDE and ABOVE the image (y=1.05, va='bottom')
    axes[i].text(0.0, 1.05, panel_letters[i], transform=axes[i].transAxes, 
                 fontsize=11, fontweight='bold', va='bottom', ha='left', clip_on=False)
                 
    # Pushed OUTSIDE and BELOW the image (y=-0.10)
    axes[i].text(0.5, -0.10, compound_labels[i], transform=axes[i].transAxes,
                 fontsize=10, va='top', ha='center', clip_on=False) 

# Tighten the layout. 
# hspace=0.35 gives plenty of vertical room so rows don't crash into each other's labels.
# top=0.90 leaves room for A, B, C at the very top of the figure.
plt.subplots_adjust(wspace=0.02, hspace=0.35, left=0.02, right=0.98, top=0.90, bottom=0.10)

plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0.05)
print(f"✅ Success! Saved publication-ready 2x3 PLIP grid to:\n{output_path}")