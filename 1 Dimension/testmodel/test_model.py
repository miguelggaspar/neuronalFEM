import numpy as np
import pandas as pd
from functions import viscoPlastic1D
from sklearn.externals import joblib

# Load trained model for further prediction and scalers to transform the data.
ann = joblib.load('../train/model/mlmodel.pkl')
scaler_x = joblib.load('../train/model/scaler_x.pkl')
scaler_y = joblib.load('../train/model/scaler_y.pkl')
# Load real data to compare results
df = pd.read_csv("../dataset/data.csv")
# initial conditions - inelastic strain  / X / R
z0 = [0, 0, 50.0]
# number of time points
n = 3000
# Define material parameters for viscoplastic behaviour
# K, n, H, D, h, d
model = viscoPlastic1D(50.0, 3.0, 5000.0, 100.0, 300.0, 0.6)
# Time points
t = np.linspace(0, 80, n)
# Solve Chaboche's 1D model with given material parameters
model.solve(n, z0, t, ann, scaler_x, scaler_y)
# Calculate elastic strain
elastic = model.ttotalstrain - model.inelastic

# Save Results to csv file
df1 = pd.DataFrame({"EI": model.inelastic, "EL": elastic,
                    "ET": model.ttotalstrain, "X": model.X, "R": model.R,
                    "S": model.sigma, "dEI": model.dinelastic,
                    "dX": model.dX, "dR": model.dR, "Time": t})
df1.to_csv("predictions_1d.csv", float_format='%.5f', index=False)
