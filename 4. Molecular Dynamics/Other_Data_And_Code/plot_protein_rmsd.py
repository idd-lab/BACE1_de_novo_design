import matplotlib
# MUST BE CALLED BEFORE PYPLOT
# Use the 'Agg' backend for non-interactive plotting (saving files)
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np

XVG_FILE = 'rmsd_protein.xvg'
OUTPUT_IMAGE = 'rmsd_protein_plot.png'
PLOT_TITLE = 'Protein RMSD vs. Time'

# --- Load Data ---
# This assumes your .xvg file has comments starting with # or @
try:
    data = np.loadtxt(XVG_FILE, comments=['#', '@'])
    time = data[:, 0]
    rmsd = data[:, 1]
except Exception as e:
    print(f"Error loading {XVG_FILE}: {e}")
    # Exit or handle error appropriately
    exit()

# --- Plotting ---
plt.style.use('seaborn-v0_8-whitegrid')
# 'plt.figure()' is preferred over 'plt.subplots()' when using 'Agg'
# if you only have one plot.
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)

ax.plot(time, rmsd, color='#007ACC', linewidth=2.0)

# --- Set Labels and Titles ---
ax.set_title(PLOT_TITLE, fontsize=16, fontweight='bold')
ax.set_xlabel('Time (ns)', fontsize=12, fontweight='bold')
ax.set_ylabel('RMSD (nm)', fontsize=12, fontweight='bold')

# --- Set Axis Limits ---
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

# --- Save and Finish ---
plt.tight_layout()
plt.savefig(OUTPUT_IMAGE, dpi=300)
print(f"Plot saved as {OUTPUT_IMAGE}")

# We do not call plt.show() because we are in a non-interactive backend
# plt.show()