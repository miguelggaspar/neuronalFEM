import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import odeint
from functions import viscoPlastic1D

# function that returns de/dt (strain rate)
def total_strain(z, t, rate):
    dedt = -rate  # Strain rate
    if (t < 4.44) | (13.88 < t < 23.32) | (32.76 < t < 42.2) | (51.64 < t < 61.08) | (t > 70.52):
        # print 'estou positivo -> t \n', t
        dedt = rate
    if (4.44 < t < 13.88) | (23.32 < t < 32.76) | (42.2 < t < 51.64 ) | (61.08 < t < 70.52):
        # print 'estou negativo -> t \n', t
        dedt = -rate
    return dedt


# initial conditions - inelastic strain  / X / R
z0 = [0, 0, 0]

# initial conditions - epsilon / X / R
y0 = [0]

# number of time points
n = 1000

# step input
stress = np.zeros(n)

# time points
t = np.linspace(0, 80, n)

# Vector of critical points (e.g. singularities) where integration care
# should be taken.
critpoints = [4.44, 13.88, 23.32, 32.76, 42.2, 51.64, 61.08, 70.52]
rate = 0.008
# solve ODE to calculate tottal strain input
totalstrain = odeint(total_strain, y0, t, args=(rate,), tcrit=critpoints)

# Define material parameters for viscoplastic behaviour
model = viscoPlastic1D(50, 3, 5000, 100, 300, 0.6)
# Solve
model.solve(n, z0, stress, totalstrain, critpoints)

# Rearrange the totalstrain vector for data save
totalstrain1 = np.empty_like(t)
for i in range(1, n):
    totalstrain1[i] = totalstrain[i]

# Save Results to csv file
df = pd.DataFrame({"IStrain": model.inelastic,
                   "TStrain": totalstrain1, "X": model.X, "R": model.R,
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
