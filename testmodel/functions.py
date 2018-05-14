# function that returns [deps/dt, dX/dt, dR/dt]
import numpy as np
from scipy.integrate import odeint


class viscoPlastic1D:

    def __init__(self, K, n, H, D, h, d):
        self.K = K
        self.n = n
        self.H = H
        self.D = D
        self.h = h
        self.d = d

    def model(self, z, t, totalstrain, i, ann, scaler):
        eps = z[0]
        X = z[1]
        R = z[2]

        sigma = 200*(totalstrain - eps)

        # input = scaler.transform([[eps, R, sigma, totalstrain, X]])
        input = [[eps, R, sigma, totalstrain, X]]
        output = ann.predict(input)

        depsdt = output[0][0]
        dRdt = output[0][1]
        dXdt = output[0][2]

        # p = scaler.transform([[0.00016, 0.04893, 3.78436, 0.01909, 0.80891]])
        # a = final_model.predict(p)
        # # a = final_model.predict([[0.00016, 0.04893, 3.78436, 0.01909, 0.80891]])
        # print (a[0][0])
        # print (a[0][1])
        # print (a[0][2])

        self.dinelastic[i-1] = depsdt
        self.dX[i-1] = dXdt
        self.dR[i-1] = dRdt
        self.sigma[i-1] = sigma

        return [depsdt, dXdt, dRdt]

    def solve(self, n, z0, totalstrain, t, ann, scaler):

        self.inelastic = np.empty_like(t)
        self.dinelastic = np.empty_like(t)
        self.X = np.empty_like(t)
        self.dX = np.empty_like(t)
        self.R = np.empty_like(t)
        self.dR = np.empty_like(t)
        self.sigma = np.empty_like(t)
        # record initial conditions
        self.inelastic[0] = z0[0]
        self.X[0] = z0[1]
        self.R[0] = z0[2]

        for i in range(1, n):
            # span for next time step
            tspan = [t[i-1], t[i]]

            # solve for next step
            (z, d) = odeint(self.model, z0, tspan, args=(totalstrain[i-1], i,
                                                         ann, scaler), full_output=1)

            # store solution for plotting
            self.inelastic[i] = z[1][0]
            self.X[i] = z[1][1]
            self.R[i] = z[1][2]

            # next initial condition
            z0 = z[1]
