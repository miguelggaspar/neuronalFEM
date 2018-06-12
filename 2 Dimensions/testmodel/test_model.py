import numpy as np
import pandas as pd
from functions import viscoPlastic2D
from sklearn.externals import joblib

# Load trained model for further prediction and scalers to transform the data.
ann = joblib.load('../train/model/mlmodel.pkl')
scaler_x = joblib.load('../train/model/scaler_x.pkl')
scaler_y = joblib.load('../train/model/scaler_y.pkl')

# number of time points
n = 1000

# Define material parameters for viscoplastic behaviour
# E, v, R1, k, K, a, b, c, n
model = viscoPlastic2D(200000.0, 0.3, 436.0, 80.0, 85.2, 93.57, 21.3, 843, 4.55)
# Time points
t = np.linspace(0, 80, n)
# initial conditions - inelastic strain  / X / R
z0 = [0, 0, 0, 0, 0, 0, model.R1, 0]
# Solve Chaboche's 1D model with given material parameters
model.solve(n, z0, t, ann, scaler_x, scaler_y)

# Calculate elastic strain
#TODO

# Save Results to csv file
df = pd.DataFrame({"ET11": model.ET[:, 0], "ET22": model.ET[:, 1], "ET12": model.ET[:, 2],
                   "Ei11": model.Ei[:, 0], "Ei22": model.Ei[:, 1], "Ei12": model.Ei[:, 2],
                   "dEi11": model.dEi[:, 0], "dEi22": model.dEi[:, 1], "dEi12": model.dEi[:, 2],
                   "X11": model.X[:, 0], "X22": model.X[:, 1], "X12": model.X[:, 2],
                   "dX11": model.dX[:, 0], "dX22": model.dX[:, 1], "dX12": model.dX[:, 2],
                   "pStrain": model.p, "R": model.R, "dpStrain": model.dp, "dR": model.dR,
                   "S11": model.stress[:, 0], "S22": model.stress[:, 1], "S12": model.stress[:, 2],
                   "Time": t})

df.to_csv("predictions_2d.csv", float_format='%.5f', index=False)
