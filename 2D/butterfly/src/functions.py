# function that returns [deps/dt, dX/dt, dR/dt]
import math
import numpy as np
import copy
from scipy.integrate import odeint


class viscoPlastic2D:

    def __init__(self, E, v, R1, k, K, a, b, c, n, nt):
        self.E = E
        self.v = v
        self.R1 = R1
        self.k = k
        self.K = K
        self.a = a
        self.b = b
        self.c = c
        self.n = n
        self.ET = np.zeros((nt, 3))
        self.Ee = np.zeros((nt, 3))
        self.Ei = np.zeros((nt, 3))
        self.X = np.zeros((nt, 3))
        self.p = np.zeros(nt)
        self.R = np.zeros(nt)
        self.dEi = np.zeros((nt, 3))
        self.dX = np.zeros((nt, 3))
        self.dp = np.zeros(nt)
        self.dR = np.zeros(nt)
        self.stress = np.zeros((nt, 3))
        self.stress_plas = np.zeros((nt, 3))
        self.crit = np.zeros(nt)
        self.J = np.zeros(nt)

    def model(self, z, t, i, stiff, ET):
        # from z separate function values:
        Ei = z[:3].reshape(3, 1)       # Inelastic strain tensor (EIxx,EIyy,EIxy=EIyx)
        X = z[3:6].reshape(3, 1)       # Back stress tensor
        R = copy.deepcopy(z[6])        # Drag stress
        p = copy.deepcopy(z[7])        # plastic strain
        ET = ET.reshape(3, 1)

        # stress = np.matmul(stiff, ET-Ei)
        stress = np.matmul(stiff, ET-Ei)
        # if self.trial == 'xx':                 # X axis traction
        #     stress[1] = 0                     # StressY = 0
        # elif self.trial == 'yy':               # Y axis traction
        #     stress[0] = 0                     # StressX = 0
        # Calculate deviatoric Stress
        S_dev = copy.deepcopy(stress)
        S_dev[0][0] -= (1./2.)*(stress[0]+stress[1])
        S_dev[1][0] -= (1./2.)*(stress[0]+stress[1])
        # Calculate deviatoric back stress
        X_dev = copy.deepcopy(X)
        X_dev[0][0] -= (1./2.)*(X[0] + X[1])
        X_dev[1][0] -= (1./2.)*(X[0] + X[1])
        # Calculate J invariant
        J = math.sqrt((3./2.)*np.matmul((S_dev-X_dev).transpose(), S_dev-X_dev))
        self.J[i] = J
        crit = (J - R - self.k) / self.K

        self.crit[i] = crit
        # print "crit ->> \n", crit
        if (J/self.K) < ((R + self.k)/self.K):          # Elastic behavior
            dpdt = 0
            dEIdt = np.array([[0], [0], [0]])
            dXdt = np.array([[0], [0], [0]])
            dRdt = 0
        else:               # Plastic behavior
            # Calculate plastic strain rate
            dpdt = crit**self.n
            # dpdt = ((1./2.) * (crit + abs(crit)))**self.n
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

    def solve(self, nt, z0, t, ET):
        print(ET)
        # record initial conditions
        self.Ei[0, 0] = z0[0]        # Inelastic strain xx direction
        self.Ei[0, 1] = z0[1]        # Inelastic strain yy direction
        self.Ei[0, 2] = z0[2]        # Inelastic strain xy direction
        self.X[0, 0] = z0[3]         # Back stress xx direction
        self.X[0, 1] = z0[4]         # Back stress yy direction
        self.X[0, 2] = z0[5]         # Back stress xy direction
        self.R[0] = z0[6]            # Drag stress
        self.p[0] = z0[7]            # Plastic strain

        stiff = self.E/(1-self.v**2) * np.array([[1,      self.v,         0      ],
                                                 [self.v,   1 ,           0      ],
                                                 [0,        0,      (1-self.v)/2]])

        for i in range(1, nt):
            self.ET[i,:] = ET[i,:]

            # span for next time step
            tspan = [t[i-1], t[i]]
            # solves for next step
            z = odeint(self.model, z0, tspan, args=(i, stiff, ET[i, :]))
            # store solution for plotting
            self.Ei[i, 0] = z[1][0]
            self.Ei[i, 1] = z[1][1]
            self.Ei[i, 2] = z[1][2]
            self.X[i, 0] = z[1][3]
            self.X[i, 1] = z[1][4]
            self.X[i, 2] = z[1][5]
            self.R[i] = z[1][6]
            self.p[i] = z[1][7]
            # next initial condition
            z0 = z[1]
