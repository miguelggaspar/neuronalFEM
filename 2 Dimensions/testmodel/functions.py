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
        Emax = 0.001
        Emin = -Emax
        tcicle = t - tc*math.floor(t/tc)

        if tcicle <= tc/4.0:
            return 4.0*(Emax/tc)*tcicle

        if tc/4.0 < tcicle <= (3.0/4.0)*tc:
            return (-((4.0*Emax))/tc) * tcicle + (2.0) * Emax

        if (3.0/4.0)*tc < tcicle <= tc:
            return ((-4.0*Emin)/tc) * tcicle + 4.0*Emin

    def model(self, z, t, i, stiff, ET, ann, scaler_x, scaler_y):
        # A verificar: - Se nao utilizando o S' se consegue os mesmo resultados
        Ei = z[:3].reshape(3, 1)       # Inelastic strain tensor
        X = z[3:6].reshape(3, 1)       # Back stress tensor
        R = copy.deepcopy(z[6])        # Drag stress
        p = copy.deepcopy(z[7])        # Plastic strain
        ET = ET.reshape(3, 1)          # Total strain
        # Calculate Stress
        stress = np.matmul(stiff, ET-Ei)
        stress[1] = 0                     # StressY = 0
        input = scaler_x.transform([[Ei[0, 0], Ei[1, 0], R, stress[0, 0],
                                     X[0, 0], X[1, 0], p]])
        # input = scaler_x.transform([[Ei[0, 0], Ei[2, 0], Ei[1, 0], R,
        #                              stress[0, 0], stress[2, 0], stress[1, 0],
        #                              X[0, 0], X[2, 0], X[1, 0], p]])
        output = scaler_y.inverse_transform((ann.predict(input)))
        # dEIdt = np.array([[output[0][0]], [output[0][2]], [output[0][1]]])
        # dRdt = output[0][3]
        # dXdt = np.array([[output[0][4]], [output[0][6]], [output[0][5]]])
        # dpdt = output[0][7]
        dEIdt = np.array([[output[0][0]], [output[0][1]], [0]])
        dRdt = output[0][2]
        dXdt = np.array([[output[0][3]], [output[0][4]], [0]])
        dpdt = output[0][5]

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

    def solve(self, n, z0, t, ann, scaler_x, scaler_y):
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
            # Calculate Strain
            self.ET[i, 0] = self.total_strain(t[i])
            self.ET[i, 1] = -self.v * self.ET[i, 0]
            # self.ET[i, 1] = self.total_strain(t[i])
            # span for next time step
            tspan = [t[i-1], t[i]]
            # solves for next step
            z = odeint(self.model, z0, tspan,
                            args=(i, stiff, self.ET[i, :], ann, scaler_x,
                                  scaler_y))
            #print (z[1][0])
            # store solution for plotting
            self.Ei[i, 0] = z[1][0]
            self.Ei[i, 1] = z[1][1]
            self.Ei[i, 2] = z[1][2]
            #print ("Ei x -> ", z[1][0],"Ei y -> ", z[1][1], "Ei xy -> ", z[1][2])
            self.X[i, 0] = z[1][3]
            self.X[i, 1] = z[1][4]
            self.X[i, 2] = z[1][5]
            #testing branch
            #print ("\nX x -> ", z[1][3],"X y -> ", z[1][4], "X xy -> ", z[1][5])
            self.R[i] = z[1][6]
            #print ("\nR -> ", z[1][6])
            self.p[i] = z[1][7]
            #print ("\np -> ", z[1][7])

            # next initial condition
            z0 = z[1]
