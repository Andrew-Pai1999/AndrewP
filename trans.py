# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 10:39:50 2025

@author: mback
"""

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from scipy.interpolate import RegularGridInterpolator

import matplotlib.pyplot as plt

# Example: field defined on a grid
x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
X, Y = np.meshgrid(x, y)

print("X is ", X)
print("X[0][0]= ", X[0][0])
print("Y is ", Y)
print("Y[0][0]= ", Y[0][0])

F = np.sin(X**2 + Y**2)  # Example field
print("F is ", F)
print("F[0][0]= ", F[0][0])
print("F is shape:", F.shape)
#F = 5  # Example field


# Define the polar grid
r = np.linspace(0, np.sqrt(2), 100)         # radius from 0 to max diagonal
theta = np.linspace(0, 2*np.pi, 200)        # full circle
R, Theta = np.meshgrid(r, theta)

# Convert to Cartesian for interpolation
X_polar = R * np.cos(Theta)
Y_polar = R * np.sin(Theta)
print("X_polar: ", X_polar)
print("Y_polar: ", Y_polar)


#from scipy.interpolate import RegularGridInterpolator

# Create an interpolator for the Cartesian field
interp_func = RegularGridInterpolator((y, x), F, bounds_error=False)  # Note: y first, then x
print("interp_func: ", interp_func)

# Prepare points for interpolation
points = np.vstack([Y_polar.ravel(), X_polar.ravel()]).T
print("points: ", points)
this=Y_polar
this2=X_polar.ravel()
print("Points len is ", len(points))


#a = np.arange(6)
#print(R)
#print(len(R))
#print(R.shape)
F_polar = interp_func(points).reshape(R.shape)#R.shape is (200,100)

print("F: ", F[0])
print("F_polar: ", F_polar[0])
#F_polar = interp_func(points).reshape(200,100)

#F_polar = interp_func(points)



#import matplotlib.pyplot as plt

plt.subplot(1,1,1,projection='polar')
plt.pcolormesh(Theta, R, F_polar, shading='auto')
plt.xlabel("θ [rad]")
plt.ylabel("r")
plt.title("Field in Polar Coordinates")
plt.colorbar(label="Field value")
plt.show()