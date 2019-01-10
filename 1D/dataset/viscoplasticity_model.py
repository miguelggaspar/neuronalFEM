import numpy as np
import pandas as pd
from functions import viscoPlastic1D

# initial conditions - inelastic strain  / X / R
z0 = [0, 0, 50.0]

# number of time points (3000)
n = 150

# Define material parameters for viscoplastic behaviour
# K, n, H, D, h, d
model = viscoPlastic1D(50.0, 3.0, 5000.0, 100.0, 300.0, 0.6)
# Time points
t = np.linspace(0, 80, n)
# Solve Chaboche's 1D model with given material parameters
model.solve(n, z0, t)

# Calculate elastic strain
elastic = model.ttotalstrain - model.inelastic

# Save Results to csv file
df = pd.DataFrame({"IStrain": model.inelastic, "EStrain": elastic,
                   "TStrain": model.ttotalstrain, "X": model.X, "R": model.R,
                   "Stress": model.sigma, "dIStrain": model.dinelastic,
                   "dX": model.dX, "dR": model.dR, "Time": t})
df.to_csv("data_025_150.csv", float_format='%.5f', index=False)
