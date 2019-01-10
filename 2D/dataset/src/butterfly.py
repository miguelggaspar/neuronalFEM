import numpy as np
import pandas as pd
from functions import viscoPlastic2D
import sys

workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/dataset/results/'
print ('Chaboche Constitutive Viscoplasticity Model')

# trials = ['xy']
trials = ['xx', 'yy', 'xy']

# number of time points
n = int(sys.argv[1])
# Time points
t = np.linspace(0, int(sys.argv[2]), n)
# initial conditions - inelastic strain  / X / R
z0 = [0, 0, 0, 0, 0, 0, 50.0, 0]
#

# Load ET t


for Emax in Emaxs:
    for trial in trials:
        print ('Trial: ', trial, 'Emax: ', Emax)
        # Define material parameters for viscoplastic behaviour
        # E, v, R1, k, K, a, b, c, n, time_points, trial
        # # Steel 316 20C
        # model = viscoPlastic2D(200000.0, 0.3, 436.0, 80.0, 85.2, 93.57, 21.3, 843, 4.55, n, trial)
        model = viscoPlastic2D(5000.0, 0.3, 500.0, 0.0, 50.0, 7500.0,
                               0.6, 100.0, 3.0, n, trial, Emax)

        # Solve Chaboche's 1D model with given material parameters
        model.solve(n, z0, t)
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

        df.to_csv(workdir + "data_" + str(Emax) +"_" + trial + ".csv",
                  float_format='%.5f', index=False)
    # break

print ('Dataset Generated')
