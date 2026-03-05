import matplotlib.pyplot as plt
import numpy as np

XVG_FILE = 'rmsd_ligand.xvg'
OUTPUT_IMAGE = 'rmsd_ligand_plot.png'
PLOT_TITLE = 'Ligand RMSD vs. Time'

data = np.loadtxt(XVG_FILE, comments=['#', '@'])
time = data[:, 0]
rmsd = data[:, 1]

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(time, rmsd, color='#007ACC', linewidth=2.0)
ax.set_title(PLOT_TITLE, fontsize=16, fontweight='bold')
ax.set_xlabel('Time (ns)', fontsize=12, fontweight='bold')
ax.set_ylabel('RMSD (nm)', fontsize=12, fontweight='bold')
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)
plt.tight_layout()
plt.savefig(OUTPUT_IMAGE, dpi=300)
print(f"Plot saved as {OUTPUT_IMAGE}")
plt.show()