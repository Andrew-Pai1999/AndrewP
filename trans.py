import numpy as np
import pandas as pd
from scipy.interpolate import griddata

# --- Parameters for OPAL Grid ---
r_min = 3000      # mm
dr = 10           # mm
nr = 161          # radial steps
theta_min = 0     # degrees
dtheta = -3       # degrees (negative for clockwise)
ntheta = 300      # angular steps

# --- Load and Preprocess ---
# Skip comment lines, read data only
raw_data = pd.read_csv("bz_raw.txt", comment='%', delim_whitespace=True,
                       names=["x_in", "y_in", "z_in", "Bz_T"])

# Filter for median plane (z ~ 0). Tolerance may be adjusted
data = raw_data[np.abs(raw_data["z_in"]) < 1e-2]

# Unit conversion
x_mm = data["x_in"] * 25.4
y_mm = data["y_in"] * 25.4
bz_kg = data["Bz_T"] * 10  # Tesla → kG

# Convert to polar coordinates
r = np.sqrt(x_mm**2 + y_mm**2)
theta = np.degrees(np.arctan2(y_mm, x_mm))  # in degrees
theta = np.mod(theta, 360)  # Normalize to [0, 360)

# --- Build Interpolation Grid ---
r_vals = r_min + dr * np.arange(nr)
theta_vals = theta_min + dtheta * np.arange(ntheta)

R, T = np.meshgrid(r_vals, theta_vals)
X = R * np.cos(np.radians(T))
Y = R * np.sin(np.radians(T))

# --- Interpolate ---
points = np.column_stack((x_mm, y_mm))
bz_values = bz_kg.values
grid_bz = griddata(points, bz_values, (X, Y), method='linear', fill_value=0)

# --- Flatten in θ-major order ---
bz_flat = grid_bz.flatten()

# --- Write to File ---
with open("opal_bz.dat", "w") as f:
    # Header
    f.write(f"{r_min:.1f}\n")
    f.write(f"{dr:.1f}\n")
    f.write(f"{theta_min:.1f}\n")
    f.write(f"{dtheta:.1f}\n")
    f.write(f"{ntheta}\n")
    f.write(f"{nr}\n")
    
    # Field values (5 per line for readability)
    for i, val in enumerate(bz_flat):
        f.write(f"{val:.6e} ")
        if (i + 1) % 5 == 0:
            f.write("\n")
