#!/usr/bin/env python3
import numpy as np
from scipy.interpolate import griddata

# — after loading raw:
raw = np.loadtxt("data.txt", comments='%')
x_in, y_in, z_in, Bz_T = raw.T

# 1) compute radius in inches
r_in = np.sqrt(x_in**2 + y_in**2)

# 2) build mask for r ≤ 38 in
mask = r_in <= 38.0

# 3) apply mask
# … your masking code …
# mask = r_in <= 38.0
x_in = x_in[mask]
y_in = y_in[mask]
z_in = z_in[mask]
Bz_T = Bz_T[mask]

# — EXPORT FILTERED POINTS TO bfield.dat —
# Stack the columns back together:
filtered = np.vstack((x_in, y_in, z_in, Bz_T)).T

# Write out with a simple header (optional):
np.savetxt(
    "bfield.dat",
    filtered,
    fmt="%.6e",
    header="x [in]    y [in]    z [in]    Bz [T]",
    comments=""
)

print("→ bfield.dat written with all points having r ≤ 38 in.")
