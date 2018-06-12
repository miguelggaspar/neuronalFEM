# function that returns [deps/dt, dX/dt, dR/dt]
import math
import numpy as np
import copy
from scipy.integrate import odeint


class viscoPlastic2D:

    def __init__(self, E, v, R1, k, K, a, b, c, n):
        self.E = E
        self.v = v
        self.R1 = R1
        self.k = k
        self.K = K
        self.a = a
        self.b = b
        self.c = c
        self.n = n

# function that returns de/dt (strain rate)
    def total_strain(self, t):
        tc = 20.0
        Emax = 0.036
        Emin = -Emax
        tcicle = t - tc*math.floor(t/tc)

        if tcicle <= tc/4.0:
            return 4.0*(Emax/tc)*tcicle

        if tc/4.0 < tcicle <= (3.0/4.0)*tc:
            return (-((4.0*Emax))/tc) * tcicle + (2.0) * Emax

        if (3.0/4.0)*tc < tcicle <= tc:
            return ((-4.0*Emin)/tc) * tcicle + 4.0*Emin

    def model(self, z, t, i, stiff, ET):

        # a partir de z retirar:
        Ei = z[:3].reshape(3, 1)       # Inelastic strain tensor (EIxx,EIyy,EIxy=EIyx)
        X = z[3:6].reshape(3, 1)       # Back stress tensor
        R = copy.deepcopy(z[6])        # Drag stress
        p = copy.deepcopy(z[7])        # plastic strain
        ET = ET.reshape(3, 1)

        stress = np.matmul(stiff, ET-Ei)

        # Calculate deviatoric Stress
        S_dev = copy.deepcopy(stress)
        S_dev[0][0] -= (1./3.)*(stress[0]+stress[1])
        S_dev[1][0] -= (1./3.)*(stress[0]+stress[1])
        # Calculate deviatoric back stress
        X_dev = copy.deepcopy(X)
        X_dev[0][0] -= (1./3.)*(X[0] + X[1])
        X_dev[1][0] -= (1./3.)*(X[0] + X[1])
        # Calculate J invariant
        J = math.sqrt((3./2.)*np.matmul((S_dev-X_dev).transpose(), S_dev-X_dev))
        # Calculate plastic strain rate
        crit = (J - R - self.k) / self.K
        # print "crit ->> \n", crit
        if crit < 0:          # Elastic behavior
            dpdt = 0
            dEIdt = np.array([[0], [0], [0]])
            dXdt = np.array([[0], [0], [0]])
            dRdt = 0
        else:               # Plastic behavior
            dpdt = ((1./2.) * (crit + abs(crit)))**self.n
            # Calculate Inelastic strain rate tensor
            dEIdt = (3./2.) * dpdt * (S_dev-X_dev)/J
            # Calculate Back stress rate tensor
            dXdt = (3./2.) * self.a * dEIdt - self.c * X * dpdt
            # Calculate Drag stress rate
            dRdt = self.b * (self.R1 - R) * dpdt
        # Store solutions
        self.stress[i, 0] = stress[0, 0]
        self.stress[i, 1] = stress[1, 0]
        self.stress[i, 2] = stress[2, 0]
        self.dEi[i, 0] = dEIdt[0, 0]
        self.dEi[i, 1] = dEIdt[1, 0]
        self.dEi[i, 2] = dEIdt[2, 0]
        self.dX[i, 0] = dXdt[0, 0]
        self.dX[i, 1] = dXdt[1, 0]
        self.dX[i, 2] = dXdt[2, 0]
        self.dp[i] = dpdt
        self.dR[i] = dRdt
        dzdt = [dEIdt[0][0], dEIdt[1][0], dEIdt[2][0], dXdt[0, 0], dXdt[1, 0],
                dXdt[2, 0], dRdt, dpdt]
        return dzdt

    def solve(self, n, z0, t):
        self.ET = np.zeros((n, 3))
        self.Ei = np.zeros((n, 3))
        self.X = np.zeros((n, 3))
        self.p = np.zeros(n)
        self.R = np.zeros(n)
        self.dEi = np.zeros((n, 3))
        self.dX = np.zeros((n, 3))
        self.dp = np.zeros(n)
        self.dR = np.zeros(n)
        self.stress = np.zeros((n, 3))
        # record initial conditions
        self.Ei[0, 0] = z0[0]        # Inelastic strain xx direction
        self.Ei[0, 1] = z0[1]        # Inelastic strain yy direction
        self.Ei[0, 2] = z0[2]        # Inelastic strain xy direction
        self.X[0, 0] = z0[3]         # Back stress xx direction
        self.X[0, 1] = z0[4]         # Back stress yy direction
        self.X[0, 2] = z0[5]         # Back stress xy direction
        self.p[0] = z0[6]            # Plastic strain
        self.R[0] = z0[7]            # Drag stress
        stiff = self.E/(1-self.v**2) * np.array([[1,      self.v,         0      ],
                                                 [self.v,   1 ,           0      ],
                                                 [0,        0,      (1-self.v)/2]])
        # Calculate total strain
        # TODO

        for i in range(1, n):
            # Calculate Strain xx direction
            self.ET[i, 0] = self.total_strain(t[i])
            # self.ET[i, 1] = self.total_strain(t[i])
            # span for next time step
            tspan = [t[i-1], t[i]]
            # solves for next step
            (z, d) = odeint(self.model, z0, tspan, args=(i, stiff, self.ET[i, :]),
                            full_output=1)
            # store solution for plotting
            self.Ei[i, 0] = z[1][0]
            self.Ei[i, 1] = z[1][1]
            self.Ei[i, 2] = z[1][2]
            self.X[i, 0] = z[1][3]
            self.X[i, 1] = z[1][4]
            self.X[i, 2] = z[1][5]
            self.p[i] = z[1][6]
            self.R[i] = z[1][7]
            # next initial condition
            z0 = z[1]