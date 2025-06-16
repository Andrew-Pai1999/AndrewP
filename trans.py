import numpy as np
import pandas as pd

# ----- Load data from COMSOL -----
raw = pd.read_csv("data.txt", comment='%', sep=r'\s+', 
                  names=["x_in", "y_in", "z_in", "Bz_T"])

# Only use data near z = 0
data = raw[np.abs(raw["z_in"]) < 1e-2]

# Convert to mm and kG
x_mm = data["x_in"].values * 25.4
bz_kg = data["Bz_T"].values * 10
r_mm = np.abs(x_mm)

# Round radius to nearest 0.1 mm for grouping
r_rounded = np.round(r_mm, 1)

# Create DataFrame and group by rounded radius
df = pd.DataFrame({'r': r_rounded, 'bz': bz_kg})
grouped = df.groupby('r').mean().reset_index()

# Sorted radial profile
r_clean = grouped['r'].values
bz_clean = grouped['bz'].values

# ----- Define OPAL radial grid -----
r_min = int(np.floor(r_clean.min()))       # ~1955
r_max = int(np.ceil(r_clean.max()))        # ~2769
dr = 1
nr = (r_max - r_min) + 1
r_grid = r_min + dr * np.arange(nr)

# Interpolate Bz(r)
bz_r = np.interp(r_grid, r_clean, bz_clean, left=0, right=0)

# ----- Tile across θ -----
theta_min = 0
dtheta = -3
ntheta = 300
bz_grid = np.tile(bz_r, (ntheta, 1))
bz_flat = bz_grid.flatten()

# ----- Write to OPAL plain Bz file -----
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
