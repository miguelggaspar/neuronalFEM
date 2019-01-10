#!/usr/bin/env python3
import math
import numpy as np
import copy
from scipy.integrate import odeint

class Chaboche2D:
    """


    Args:
        param1 (int): Array containing the material parameters,
                      as well as the maximum strain for the
                      specified test.
    Attributes:
        E,v,R1,k,K,a,b,c,n (int): Material parameters
        test (str): Type of mechanical test, it can be a tensile
                    test (xx,yy) or simple shear (xy).
        Emax (int): Maximum mechanical displacement

    """


    def __init__(self, E, v, R1, k, K, a, b, c, n, test, Emax):
        self.E = E
        self.v = v
        self.R1 = R1
        self.k = k
        self.K = K
        self.a = a
        self.b = b
        self.c = c
        self.n = n
        self.test = test
        self.Emax = Emax
        self.solutions = []

    def total_strain(self, t):
        """

        Args:
            param1 (int): Current moment of time (t).

         Returns:
            The mechanical displacement for the current moment
            of time (t).
        """
        tc = 20.0                   # Cyclic time for one cyclic loading
        Emax = self.Emax            # Maximum mechanical displacement
        Emin = -Emax
        tcicle = t - tc*math.floor(t/tc)
        # Caculate total strain
        if tcicle <= tc/4.0:
            return 4.0*(Emax/tc)*tcicle
        if tc/4.0 < tcicle <= (3.0/4.0)*tc:
            return (-((4.0*Emax))/tc) * tcicle + (2.0) * Emax
        if (3.0/4.0)*tc < tcicle <= tc:
            return ((-4.0*Emin)/tc) * tcicle + 4.0*Emin


    def deriv(self, z, t, stiff, ET):
        """

        Args:
            param1 (np.array): Array containing the values of viscoplastic
                               strain tensor, back stress tensor, drag stress
                               and plastic strain.
            param2 (np.array): A sequence of time points for which
                               to solve for z.
            param3 (int): The mechanical displacement for this step
        Returns:
            Array containing the derivatives of viscoplastic strain tensor,
            back stress tensor, drag stress and plastic strain in t, with
            the initial value z0 in the first row.

        """
        Evp = z[:3].reshape(3, 1)       # Inelastic strain tensor
        X = z[3:6].reshape(3, 1)        # Back stress tensor
        R = copy.deepcopy(z[6])         # Drag stress
        p = copy.deepcopy(z[7])         # plastic strain
        ET = ET.reshape(3, 1)           # Total strain
        # Calculate Stress
        S = np.matmul(stiff, ET-Evp)
        if self.test == 'xx':                 # Txx
            S[1] = 0                          # S22 = 0
        elif self.test == 'yy':               # Txy
            S[0] = 0                          # S11 = 0
        # Calculate deviatoric Stress
        S_dev = copy.deepcopy(S)
        S_dev[0][0] -= (1./2.)*(S[0]+S[1])
        S_dev[1][0] -= (1./2.)*(S[0]+S[1])
        # Calculate deviatoric back stress
        X_dev = copy.deepcopy(X)
        X_dev[0][0] -= (1./2.)*(X[0] + X[1])
        X_dev[1][0] -= (1./2.)*(X[0] + X[1])
        # Calculate J invariant
        J = math.sqrt((3./2.)*np.matmul((S_dev-X_dev).transpose(), S_dev-X_dev))

        if (J/self.K) < ((R + self.k)/self.K):          # Elastic State
            dpdt = 0
            dEvpdt = np.array([[0], [0], [0]])
            dXdt = np.array([[0], [0], [0]])
            dRdt = 0
        else:                                           # Plastic State
            # Calculate plastic strain rate
            dpdt = ((J - R - self.k) / self.K) ** self.n
            # Calculate viscoplastic strain rate tensor
            dEvpdt = (3./2.) * dpdt * (S_dev-X_dev)/J
            # Calculate Back stress rate tensor
            dXdt = (3./2.) * self.a * dEvpdt - self.c * X * dpdt
            # Calculate Drag stress rate
            dRdt = self.b * (self.R1 - R) * dpdt

        dzdt = [dEvpdt[0][0], dEvpdt[1][0], dEvpdt[2][0], dXdt[0, 0], dXdt[1, 0],
                dXdt[2, 0], dRdt, dpdt]
        return dzdt

    def solve(self, z0, t):
        """

        Args:
            param1 (np.array): Array containing the initial conditions.
            param2 (int): Total sequence of time points for which
                          to solve for z.

        """
        # Define Stiff matrix
        stiff = self.E/(1-self.v**2) * np.array([[1,      self.v,         0      ],
                                                 [self.v,   1 ,           0      ],
                                                 [0,        0,      (1-self.v)/2]])
        # Initialize Total strain tensor
        ET = np.zeros((1, 3))
        # Iterate through the sequence of time points
        for i in range(1, len(t)):
            # Mechanical displacements for next step
            if self.test == 'xx':                           # Txx test
                ET[0, 0] = self.total_strain(t[i])
                ET[0, 1] = -self.v * ET[0, 0]
            elif self.test == 'yy':                         # Tyy test
                ET[0, 1] = self.total_strain(t[i])
                ET[0, 0] = -self.v * ET[0, 1]
            elif self.test == 'xy':                         # Sxy test
                ET[0, 0] = 0
                ET[0, 1] = 0
                ET[0, 2] = self.total_strain(t[i])
            # Time span for next time step
            tspan = [t[i-1], t[i]]
            # Solve for next step
            z = odeint(self.deriv, z0, tspan, args=(stiff, ET))
            # store solution for plotting
            self.solutions.append(z)
            # Next initial condition
            z0 = z[1]

# Main program
if __name__ == "__main__":
    # initial conditions - Evp(tensor) / X(tensor) / R / p
    z0 = [0, 0, 0, 0, 0, 0, 50.0, 0]
    # number of data points
    n = 1000
    # Choose one test from -> (xx,yy,xy)
    test = 'xx'
    # Maximum mechanical displacement for cyclic loading
    Emax = 0.18
    # Define material and test parameters
    # E, v, R1, k, K, a, b, c, n, test, Emax
    model_2D = Chaboche2D(5000.0, 0.3, 500.0, 0.0, 50.0, 7500.0,
                           0.6, 100.0, 3.0, test, Emax)
    # Time points
    t = np.linspace(0, 80, n)
    # Solve Chaboche's 1D model with given material parameters
    model_2D.solve(z0, t)
