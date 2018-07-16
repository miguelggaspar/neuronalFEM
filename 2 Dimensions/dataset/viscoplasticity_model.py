import numpy as np
import pandas as pd
from functions import viscoPlastic2D

workdir = '/home/miguel/UA/tese/ViscoPlastic-ML/2 Dimensions/dataset/results/'
# number of time points
n = 2300
# Time points
t = np.linspace(0, 80, n)
# initial conditions - inelastic strain  / X / R
z0 = [0, 0, 0, 0, 0, 0, 0, 0]
trials = ['xx', 'yy', 'xy']
print ('Chaboche Constitutive Viscoplasticity Model')

for trial in trials:
    print ('Trial: ', trial)
    # Define material parameters for viscoplastic behaviour
    # E, v, R1, k, K, a, b, c, n
    # Steel 400C
    # model = viscoPlastic2D(160000.0, 0.3, 0.05, 96.0, 50.0, 2000.0, 100.0, 300.0, 5.0, n)
    # # St37 20C
    # model = viscoPlastic2D(168600.0, 0.3, 0., 167.88, 63.12, 2500.0, 0.0, 20.3, 4.22, n)
    # # St37 20C
    # model = viscoPlastic2D(113066.0, 0.3, 0., 180.0, 11.45, 98939.30, 0., 1533.41, 8.15, n)
    # # Steel 316 20C
    # model = viscoPlastic2D(196000.0, 0.3, 60.0, 82.0, 151.0, 162.4, 8.0, 2800.0, 24, n)
    # # Steel 316 20C
    model = viscoPlastic2D(200000.0, 0.3, 436.0, 80.0, 85.2, 93.57, 21.3, 843, 4.55, n, trial)
    # Steel 20C
    # neural pattern recognition network
    # model = viscoPlastic2D(223000.0, 0.3, -138.48, 210.15, 14.085, 611700.0, 16.74,
                        #    38840.0, 9.51, n)
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

    df.to_csv(workdir + "data_" + trial + ".csv",
              float_format='%.5f', index=False)

print ('Dataset Generated')
