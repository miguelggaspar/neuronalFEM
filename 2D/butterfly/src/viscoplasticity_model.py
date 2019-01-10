import numpy as np
import pandas as pd
from functions import viscoPlastic2D
import sys


def load_csv(dir, propertie):
     df = pd.read_csv(dir + propertie + ".csv")
     return df


dir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/butterfly/results/'
P = '1'
 # Get strain values for simulation
ET11 = load_csv(dir + 'P_' + P + '/', 'abaqus_ET11_P_' + P)
ET22 = load_csv(dir + 'P_' + P + '/', 'abaqus_ET22_P_' + P)
ET12 = load_csv(dir + 'P_' + P + '/', 'abaqus_ET12_P_' + P)
time = load_csv(dir, 'abaqus_time')

ET = pd.concat([ET11, ET22, ET12], axis=1, join='inner')

# Time points
t = time['time'].values
# number of time points
n = t.shape[0]
# initial conditions - inelastic strain  / X / R
z0 = [0, 0, 0, 0, 0, 0, 50.0, 0]
# Define material parameters for viscoplastic behaviour
# E, v, R1, k, K, a, b, c, n, time_points, trial
# # Steel 316 20C
# model = viscoPlastic2D(200000.0, 0.3, 436.0, 80.0, 85.2, 93.57, 21.3, 843, 4.55, n, trial)
model = viscoPlastic2D(5000.0, 0.3, 500.0, 0.0, 50.0, 7500.0,
                       0.6, 100.0, 3.0, n)

# Solve Chaboche's 1D model with given material parameters
model.solve(n, z0, t, ET.values)
# Calculate Elastic strain
model.Ee = model.ET - model.Ei
# Save Results to csv file
df = pd.DataFrame({"ET11": model.ET[:, 0], "ET22": model.ET[:, 1], "ET12": model.ET[:, 2],
                   "Ei11": model.Ei[:, 0], "Ei22": model.Ei[:, 1], "Ei12": model.Ei[:, 2],
                   "dEi11": model.dEi[:, 0], "dEi22": model.dEi[:, 1], "dEi12": model.dEi[:, 2],
                   "X11": model.X[:, 0], "X22": model.X[:, 1], "X12": model.X[:, 2],
                   "dX11": model.dX[:, 0], "dX22": model.dX[:, 1], "dX12": model.dX[:, 2],
                   "pStrain": model.p, "R": model.R, "dpStrain": model.dp, "dR": model.dR,
                   "S11": model.stress[:, 0], "S22": model.stress[:, 1], "S12": model.stress[:, 2],
                   "Ee11": model.Ee[:, 0], "Ee22": model.Ee[:, 1], "Ee12": model.Ee[:, 2],
                   "Time": t})

df.to_csv(dir + 'P_' + P + '/' + "data_P_" + P + ".csv",
          float_format='%.5f', index=False)
# break

print ('Dataset Generated')
