#!/usr/bin/env python3
import math
import numpy as np
from scipy.integrate import odeint

class Chaboche1D:
    """


    Args:
        param1 (array): Array containing the material parameters.

    """


    def __init__(self, E, K, n, H, D, h, d):
        self.E = E
        self.K = K
        self.n = n
        self.H = H
        self.D = D
        self.h = h
        self.d = d
        self.solutions = []

    def total_strain(self, t):
        """

        Args:
            param1 (int): Current moment of time (t).

         Returns:
            The mechanical displacement for the current moment
            of time (t).
        """
        tc = 20.0               # Cyclic time for one cyclic loading
        Emax = 0.036            # Maximum mechanical displacement
        Emin = -Emax
        tcicle = t - tc*math.floor(t/tc)
        # Caculate total strain
        if tcicle <= tc/4.0:
            return 4.0*(Emax/tc)*tcicle
        if tc/4.0 < tcicle <= (3.0/4.0)*tc:
            return (-((4.0*Emax))/tc) * tcicle + (2.0) * Emax
        if (3.0/4.0)*tc < tcicle <= tc:
            return ((-4.0*Emin)/tc) * tcicle + 4.0*Emin


    def deriv(self, z, t, ET):
        """

        Args:
            param1 (np.array): Array containing the values of viscoplastic
                               strain, back stress and drag stress.
            param2 (np.array): A sequence of time points for which
                               to solve for z.
            param3 (int): The mechanical displacement for this step
        Returns:
            Array containing the derivatives of viscoplastic strain,
            back stress and drag stress in t, with the initial
            value z0 in the first row.

        """
        Evp = z[0]                  # Viscoplastic strain
        X = z[1]                    # Back stress
        R = z[2]                    # Drag stress
        S = self.E*(ET - Evp)       # Calculate Total Stress
        if abs(S - X) - R < 0:      # Elastic state
            dEvpdt = 0.
            dXdt = 0.
            dRdt = 0.
        else:                       # Plastic state
            dEvpdt = (((abs(S - X) - R) / self.K) ** self.n) * np.sign(S - X)
            dXdt = self.H * dEvpdt - self.D * X * abs(dEvpdt)
            dRdt = self.h * abs(dEvpdt) - self.d * R * abs(dEvpdt)
        return [dEvpdt, dXdt, dRdt]


    def solve(self, z0, t):
        """

        Args:
            param1 (np.array): Array containing the initial conditions.
            param2 (int): Total sequence of time points for which
                          to solve for z.

        """
        # Iterate through the sequence of time points
        for i in range(1, len(t)):
            # Mechanical displacement for next step
            ET = self.total_strain(t[i])
            # Time span for the next time step
            tspan = [t[i-1], t[i]]
            # Solve for next step
            z = odeint(self.deriv, z0, tspan, args=(ET,))
            # Store solution
            self.solutions.append(z)
            # Next initial condition
            z0 = z[1]

# Main program
if __name__ == "__main__":
    # initial conditions - Evp / X / R
    z0 = [0, 0, 50.0]
    # number of data points
    n = 3000
    # Define material parameters
    # E, K, n, H, D, h, d
    model_1D = Chaboche1D(5000.0, 50.0, 3.0, 5000.0, 100.0, 300.0, 0.6)
    # Time points
    t = np.linspace(0, 80, n)
    # Solve Chaboche's 1D model with given material parameters
    model_1D.solve(z0, t)
