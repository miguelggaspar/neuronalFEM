import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import odeint
from functions import viscoPlastic1D


# initial conditions - inelastic strain  / X / R
z0 = [0, 0, 50.0]

# initial conditions - totalStrain
y0 = [0]

# number of time points
tc = 5          # time cycle
rate = 0.008
n = 100000
nc = 8
tpoints = n/nc

# Empty arrays for storage
stress = np.zeros(n)
totalstrain = np.array([])


# Define material parameters for viscoplastic behaviour
# K, n, H, D, h, d
model = viscoPlastic1D(50.0, 3.0, 5000.0, 100.0, 300.0, 0.6)
# Solve
t = np.linspace(0, 80, n)
model.solve(n, z0, totalstrain, t)

# Save Results to csv file
df = pd.DataFrame({"IStrain": model.inelastic,
                   "TStrain": model.ttotalstrain, "X": model.X, "R": model.R,
                   "Stress": model.sigma, "dIStrain": model.dinelastic,
                   "dX": model.dX, "dR": model.dR, "Time": t})

df.to_csv("data.csv", float_format='%.5f', index=False)

# plot results
plt.figure(figsize=(8, 5), dpi=80)
plt.style.use('ggplot')
plt.subplot(1, 3, 1)
totalstrain_hand, = plt.plot(t, model.ttotalstrain, 'b-')
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
plt.plot(model.ttotalstrain,model.sigma)
plt.show()
