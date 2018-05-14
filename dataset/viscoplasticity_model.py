import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import odeint
from functions import viscoPlastic1D


# function that returns de/dt (strain rate)
def total_strain(z, t, tc, j, rate, sign):
    dedt = 0  # Strain rate
    if 2*j*tc <= t < (2*j+1)*tc:
        if sign == 0:
            dedt = rate
        else:
            dedt = -rate
    elif (2*j+1)*tc <= t < 2*(j+1)*tc:
        if sign == 0:
            dedt = -rate
        else:
            dedt = rate
    return dedt

# initial conditions - inelastic strain  / X / R
z0 = [0, 0, 0]

# initial conditions - totalStrain
y0 = [0]

# number of time points
tc = 5          # time cycle
rate = 0.008
n = 10000
nc = 8
tpoints = n/nc

# Empty arrays for storage
stress = np.zeros(n)
totalstrain = np.array([])
t = np.array([])

# solve ODE to calculate total strain input
for j in range(0, nc):
    taux = np.linspace(2*j*tc, 2*(j+1)*tc, tpoints)
    if j % 2 == 0:
        sign = 0    # Even
    else:
        sign = 1    # Odd
    z = odeint(total_strain, y0, taux, args=(tc, j, rate, sign))
    totalstrain = np.append(totalstrain, z)
    t = np.append(t,taux)

# Define material parameters for viscoplastic behaviour
model = viscoPlastic1D(50, 3, 5000, 100, 300, 0.6)
# Solve
model.solve(n, z0, totalstrain, t)


# Save Results to csv file
df = pd.DataFrame({"IStrain": model.inelastic,
                   "TStrain": totalstrain, "X": model.X, "R": model.R,
                   "Stress": model.sigma, "dIStrain": model.dinelastic,
                   "dX": model.dX, "dR": model.dR, "Time": t})

df.to_csv("data.csv", float_format='%.5f', index=False)


# plot results
plt.figure(figsize=(8, 5), dpi=80)
plt.style.use('ggplot')
plt.subplot(1, 3, 1)
totalstrain_hand, = plt.plot(t, totalstrain, 'b-')
inelastic_hand, = plt.plot(t, model.inelastic, 'r-')
plt.ylabel('Strain %')
plt.xlabel('Time')
# plt.title('Elastic Strain - Time')
first_legend = plt.legend(handles=[totalstrain_hand, inelastic_hand], loc=0)
plt.legend((totalstrain_hand, inelastic_hand), ('Total Strain', 'Inelastic Strain'))

plt.subplot(1, 3, 2)
dX_hand, = plt.plot(t, model.dX, 'y-',)
dR_hand, = plt.plot(t, model.dR, 'r-',)
dinelastic_hand, = plt.plot(t, model.dinelastic, 'b-')
# plt.ylabel('Strain %')
plt.xlabel('Time')
# plt.title('Derivatives - Time')
plt.legend((dX_hand, dR_hand, dinelastic_hand),
           ('Back stress(X) / dt', 'Drag stress(R) / dt', 'dinelastic/dt'))

plt.subplot(1, 3, 3)
X_hand, = plt.plot(t, model.X, 'y-')
R_hand, = plt.plot(t, model.R, 'r-')
stress_hand, = plt.plot(t, model.sigma, 'b-')
plt.ylabel('All Strain')
plt.xlabel('Time')
#plt.title('All Strain - Time')
plt.legend((X_hand, R_hand, stress_hand),
           ('Back stress(X)', 'Drag stress(R)', 'Total Stress'))

plt.show()
