import numpy as np
import pandas as pd

# Load raw COMSOL-exported data
raw = pd.read_csv("data.txt", comment='%', sep=r'\s+',
                  names=["x_in", "y_in", "z_in", "Bz_T"])

# Select only z = 0 plane
data = raw[np.abs(raw["z_in"]) < 1e-5]

# Convert units
x_mm = data["x_in"].values * 25.4   # inches → mm
bz_kg = data["Bz_T"].values * 10    # Tesla → kg (OPAL unit)
r_mm = np.abs(x_mm)

# Filter out r < 38 inches (38 * 25.4 = 965.2 mm)
min_r_mm = 38 * 25.4
mask = r_mm >= min_r_mm
r_mm = r_mm[mask]
bz_kg = bz_kg[mask]

# Round radius to nearest 0.1 mm for binning
r_rounded = np.round(r_mm, 1)

# Group by rounded radius and average
df = pd.DataFrame({'r': r_rounded, 'bz': bz_kg})
grouped = df.groupby('r').mean().reset_index()

# Clean radial data
r_clean = grouped['r'].values
bz_clean = grouped['bz'].values

# Define OPAL radial grid
r_min = int(np.ceil(min_r_mm))         # Start at 38 inches in mm (→ 966)
r_max = int(np.ceil(76 * 25.4))        # 76 inches (→ 1931 mm)
dr = 1                                 # 1 mm step
nr = (r_max - r_min) + 1               # Total radial steps
r_grid = r_min + dr * np.arange(nr)

# Interpolate Bz(r) over defined radial grid
bz_r = np.interp(r_grid, r_clean, bz_clean, left=0, right=0)

# Tile across θ
theta_min = 0
dtheta = -3
ntheta = 1000
bz_grid = np.tile(bz_r, (ntheta, 1))   # Shape: (ntheta, nr)
bz_flat = bz_grid.flatten()

# Write to OPAL Bz file
with open("opal_bz.dat", "w") as f:
    f.write(f"{r_min:.1f}\n")
    f.write(f"{dr:.1f}\n")
    f.write(f"{theta_min:.1f}\n")
    f.write(f"{dtheta:.1f}\n")
    f.write(f"{ntheta}\n")
    f.write(f"{nr}\n")
    for i, val in enumerate(bz_flat):
        f.write(f"{val:.6e} ")
        if (i + 1) % 5 == 0:
            f.write("\n")

print("✅ Finished! Output saved to opal_bz.dat")