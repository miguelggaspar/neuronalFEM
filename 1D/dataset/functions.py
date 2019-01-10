# function that returns [deps/dt, dX/dt, dR/dt]
import math
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

# function that returns de/dt (strain rate)
    def total_strain(self, t):
        tc = 20.0
        # Emax = 0.036
        Emax = 0.025
        Emin = -Emax
        tcicle = t - tc*math.floor(t/tc)

        if tcicle <= tc/4.0:
            return 4.0*(Emax/tc)*tcicle

        if tc/4.0 < tcicle <= (3.0/4.0)*tc:
            return (-((4.0*Emax))/tc) * tcicle + (2.0) * Emax

        if (3.0/4.0)*tc < tcicle <= tc:
            return ((-4.0*Emin)/tc) * tcicle + 4.0*Emin

    def model(self, z, t, i, totalstrain):
        eps = z[0]
        X = z[1]
        R = z[2]
        sigma = 5000.0*(totalstrain - eps)
        if abs(sigma - X) - R < 0.:
            depsdt = 0.
            dXdt = 0.
            dRdt = 0.
        else:
            depsdt = (((abs(sigma - X) - R) / self.K) ** self.n) * np.sign(sigma - X)
            dXdt = self.H * depsdt - self.D * X * abs(depsdt)
            dRdt = self.h * abs(depsdt) - self.d * R * abs(depsdt)
        self.dinelastic[i] = depsdt
        self.dX[i] = dXdt
        self.dR[i] = dRdt
        self.sigma[i] = sigma
        return [depsdt, dXdt, dRdt]

    def solve(self, n, z0, t):

        self.inelastic = np.empty_like(t)
        self.dinelastic = np.empty_like(t)
        self.X = np.empty_like(t)
        self.dX = np.empty_like(t)
        self.R = np.empty_like(t)
        self.dR = np.empty_like(t)
        self.sigma = np.empty_like(t)
        self.ttotalstrain = np.empty_like(t)
        # record initial conditions
        self.inelastic[0] = z0[0]
        self.X[0] = z0[1]
        self.R[0] = z0[2]

        for i in range(1, n):
            self.ttotalstrain[i] = self.total_strain(t[i])
            # span for next time step
            tspan = [t[i-1], t[i]]

            # solve for next step
            (z, d) = odeint(self.model, z0, tspan, args=(i, self.ttotalstrain[i]),
                            full_output=1)

            # store solution for plotting
            self.inelastic[i] = z[1][0]
            self.X[i] = z[1][1]
            self.R[i] = z[1][2]

            # next initial condition
            z0 = z[1]
