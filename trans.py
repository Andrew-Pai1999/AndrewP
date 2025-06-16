# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 10:39:50 2025

@author: mback
"""

import numpy as np
import pandas as pd

# === Step 1: read COMSOL data ===
df = pd.read_csv("data.txt", sep='\s+', comment='%', header=None,
                 names=["x", "y", "z", "Bz_T"])

# === Step 2: transfer unit ===
df[["x", "y", "z"]] *= 25.4           # 英吋轉公釐
df["Bz_kG"] = df["Bz_T"] * 10         # Tesla 轉 kG

# === Step 3: calculate polar coordinate r, θ ===
df["r"] = np.sqrt(df["x"]**2 + df["y"]**2)
df["theta"] = np.degrees(np.arctan2(df["y"], df["x"])) % 360

# === Step 4: set up grid===
dr = 2.0
dtheta = 1.0
rmin = 0.0
rmax = 72.0

# create index for r and theta
df["r_bin"] = np.floor(df["r"] / dr) * dr
df["r_bin"] = np.round(df["r"] / dr) * dr
df["theta_bin"] = np.round(df["theta"] / dtheta) * dtheta

# filter radius range
df = df[df["r_bin"] <= rmax]

# create index for r and theta bins
r_bins = np.arange(rmin, rmax + dr, dr)
theta_bins = np.arange(0.0, 360.0, dtheta)

# create pivot table（r 為行，θ 為列）
pivot = pd.DataFrame(index=r_bins, columns=theta_bins)

# refill Bz values into pivot table
for _, row in df.iterrows():
    r = round(row["r_bin"], 1)
    theta = round(row["theta_bin"], 1)
    if r in pivot.index and theta in pivot.columns:
        pivot.at[r, theta] = row["Bz_kG"]

# refill lose data as  0
pivot = pivot.fillna(0.0)

# === Step 5: exportdata with Header ===
Ntheta = len(theta_bins)
Nr = len(r_bins)
header_lines = [
    f"{rmin:.1f}",               # rmin [mm]
    f"{dr:.1f}",                 # Δr [mm]
    f"0.0",                      # thetamin [deg]
    f"{dtheta:.1f}",             # Δθ [deg]
    f"{Ntheta}",                 # Nθ
    f"{Nr}"                      # Nr
]

# === Step 6: export data ===
with open("Bz_output.txt", "w") as f:
    # 輸出 Header
    f.write('\n'.join(header_lines) + '\n')
    
    # 輸出每一行（每行一個 r 對應的 360 個角度）
    for r in pivot.index:
        values = pivot.loc[r].values
        line = ' '.join(f"{val:.6e}" for val in values)
        f.write(line + '\n')

print("✅ Bz_output.txt 已完成")
