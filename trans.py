# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 10:39:50 2025

@author: mback
"""

import numpy as np
import pandas as pd

# 讀取資料（跳過表頭）
df = pd.read_csv("data.txt", sep='\s+', comment='%', header=None,
                 names=["x", "y", "z", "Bz_T"])

# 轉換為極座標 r [mm]，theta [deg]
df["r"] = np.sqrt(df["x"]**2 + df["y"]**2)
df["theta"] = np.degrees(np.arctan2(df["y"], df["x"])) % 360
df["Bz_kG"] = df["Bz_T"] * 10  # Tesla 轉換為 kG

# 四捨五入網格精度（可自訂）
dr = 2.0
dtheta = 1.0
df["r_rounded"] = np.round(df["r"] / dr) * dr
df["theta_rounded"] = np.round(df["theta"] / dtheta) * dtheta

# 排序
df = df.sort_values(by=["r_rounded", "theta_rounded"])

# 推算 header 參數
rmin = df["r_rounded"].min()
thetamin = df["theta_rounded"].min()
Nr = df["r_rounded"].nunique()
Ntheta = df["theta_rounded"].nunique()

# 注意：如需小數網格，dr/dtheta 可寫為負數
header = f"{rmin:.3f} {dr:.3f} {thetamin:.3f} {dtheta:.3f} {Ntheta} {Nr}"

# 輸出格式：r theta Bz[kG]
output_data = df[["r_rounded", "theta_rounded", "Bz_kG"]]
output_data.columns = ["r", "theta", "Bz_kG"]

# 寫入檔案
with open("converted_field.txt", "w") as f:
    f.write(header + "\n")
    output_data.to_csv(f, sep=' ', index=False, header=False, float_format="%.6f")
