import numpy as np
import pandas as pd
from scipy.interpolate import griddata

# Load data (x, y, z in inches; Bz in Tesla)
data = pd.read_csv("data.txt", sep='\s+', header=None, names=["x", "y", "z", "Bz"])

# Filter for median plane
data = data[np.abs(data["z"]) < 1e-3]  # or a narrow z band

# Unit conversion
x_mm = data["x"] * 25.4
y_mm = data["y"] * 25.4
bz_kg = data["Bz"] * 10

# Polar coordinates
r = np.sqrt(x_mm**2 + y_mm**2)
theta = np.degrees(np.arctan2(y_mm, x_mm))

# Set up grid
r_min = 3000  # example
dr = 10
nr = 161
theta_min = 0
dtheta = -3
ntheta = 300

r_vals = r_min + dr * np.arange(nr)
theta_vals = theta_min + dtheta * np.arange(ntheta)

# Create mesh grid
R, T = np.meshgrid(r_vals, theta_vals)
X = R * np.cos(np.radians(T))
Y = R * np.sin(np.radians(T))

# Interpolate onto grid
points = np.column_stack((x_mm, y_mm))
bz_grid = griddata(points, bz_kg, (X, Y), method='linear', fill_value=0)

# Flatten (θ-major)
bz_flat = bz_grid.flatten()

# Write to file
with open("bz_opal.dat", "w") as f:
    f.write(f"{r_min:.1f}\n")
    f.write(f"{dr:.1f}\n")
    f.write(f"{theta_min:.1f}\n")
    f.write(f"{dtheta:.1f}\n")
    f.write(f"{ntheta}\n")
    f.write(f"{nr}\n")
    # Write field data
    for i, val in enumerate(bz_flat):
        f.write(f"{val:.6e} ")
        if (i + 1) % 5 == 0:
            f.write("\n")
