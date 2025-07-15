import pandas as pd
import numpy as np

# Load the COMSOL-exported data
df = pd.read_csv("data.txt", comment='%', sep=r'\s+',
                 names=["x", "y", "z", "mf.By (T)"])

# Compute radius
r = np.sqrt(df["x"]**2 + df["z"]**2)

# Filter: keep only rows with r ≤ 38 inches (965.2 mm)
filtered_by = df.loc[r <= 38, "mf.By (T)"]

# Convert Tesla to kilogauss (OPAL expects kG)
by_kG = filtered_by * 10
by_values = [f"{val:.6e}" for val in by_kG]

# OPAL header values (edit these as needed)
header_lines = [
    "0",   # RMIN [mm]
    "10.0",      # DR [mm]
    "0.0",       # THETAMIN [deg]
    "-3.0",      # DTHETA [deg]
    "300",       # Ntheta
    str(len(by_kG))  # Nr = number of radius points
]

# Write output
with open("bfield.dat", "w") as f:
    # Write OPAL header
    for line in header_lines:
        f.write(line + "\n")

    # Write By values, 5 per line
    for i in range(0, len(by_values), 5):
        f.write(" ".join(by_values[i:i+5]) + "\n")
