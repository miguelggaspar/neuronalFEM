import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import odeint
from functions import viscoPlastic1D


# initial conditions - inelastic strain  / X / R
z0 = [0, 0, 50.0]

# number of time points
n = 100000

# Define material parameters for viscoplastic behaviour
# K, n, H, D, h, d
model = viscoPlastic1D(50.0, 3.0, 5000.0, 100.0, 300.0, 0.6)
# Time points
t = np.linspace(0, 80, n)
# Solve Chaboche's 1D model with given material parameters
model.solve(n, z0, t)

# Calculate elastic strain
elastic = model.ttotalstrain - model.inelastic

# Save Results to csv file
df = pd.DataFrame({"IStrain": model.inelastic,
                   "TStrain": model.ttotalstrain, "X": model.X, "R": model.R,
                   "Stress": model.sigma, "dIStrain": model.dinelastic,
                   "dX": model.dX, "dR": model.dR, "Time": t})
df.to_csv("data.csv", float_format='%.5f', index=False)


# plot results
style = 'ggplot'

# Plot Total, Elastic and Inelastic Strains
plt.figure(figsize=(8, 5), dpi=80)
plt.style.use(style)
plt.ylim(-0.075, 0.075)     # set the xlim to xmin, xmax
totalstrain_hand, = plt.plot(t, model.ttotalstrain, 'b-')   #Total strain
inelastic_hand, = plt.plot(t, model.inelastic, 'r-')        #Inelastic strain
elastic_hand, = plt.plot(t, elastic, 'y-')                  #Elastic strain
first_legend = plt.legend(handles=[totalstrain_hand, inelastic_hand, elastic_hand], loc=0)
plt.legend((totalstrain_hand, inelastic_hand, elastic_hand),
           (r' Total Strain ($\varepsilon$)', r'Inelastic Strain ($\varepsilon^{vp}$)',r'Elastic Strain ($\varepsilon^e$)'))
plt.ylabel('Strain [%]')
plt.xlabel('Time [s]')
plt.savefig('total_el_in_strain_1d.png')

# Plot computed derivatives (inelastic strain, back and drag stress)
plt.figure(figsize=(8, 5), dpi=80)
plt.style.use(style)
plt.axis('auto')
dX_hand, = plt.plot(t, model.dX, 'y-',)                 # Back stress rate
dR_hand, = plt.plot(t, model.dR, 'r-',)                 # Drag stress rate
dinelastic_hand, = plt.plot(t, model.dinelastic, 'b-')  # Inelastic strain rate
plt.xlabel('Time [s]')
plt.legend((dX_hand, dR_hand, dinelastic_hand),
           (r'Back stress ($\dot \chi$)', r'Drag stress ($\dot R$)',
            r'Inelastic Strain($\dot \epsilon^{vp}$)'))
plt.savefig('dX_dR_din_1d.png')

# Plot Back stress rate
plt.figure(figsize=(8, 5), dpi=80)
plt.style.use(style)
plt.axis('auto')
dX_hand = plt.plot(t, model.dX, 'y-')
plt.ylabel(r'Stress rate [$\frac{MPa}{s}$]')
plt.xlabel('Time [s]')
plt.legend(dX_hand,(r'Back stress rate ($\dot \chi$)',))
plt.savefig('dXdt_1d.png')

# Plot Drag stress rate
plt.figure(figsize=(8, 5), dpi=80)
plt.style.use(style)
plt.axis('auto')
# plt.subplot(1, 3, 2)
dR_hand = plt.plot(t, model.dR, 'r-')
plt.ylabel(r'Stress rate [$\frac{MPa}{s}$]')
plt.xlabel('Time [s]')
plt.legend(dR_hand,(r'Drag stress rate ($\dot R$)',))
plt.savefig('dRdt_1d.png')

# PLot Inelastic strain rate
plt.figure(figsize=(8, 5), dpi=80)
plt.style.use(style)
plt.ylim(-0.0075, 0.0075)     # set the xlim to xmin, xmax
dinelastic_hand = plt.plot(t, model.dinelastic, 'b-')
plt.ylabel(r'Strain Rate [$\frac{\%}{s}$]')
plt.xlabel('Time [s]')
plt.legend(dinelastic_hand, (r'Inelastic Strain Rate($\dot \epsilon^{vp}$)',))
plt.savefig('depsdt_1d.png')

#Plot all stress
plt.figure(figsize=(8, 5), dpi=80)
plt.style.use(style)
plt.ylim(-200, 250)     # set the xlim to xmin, xmax
# plt.subplot(1, 3, 3)
X_hand, = plt.plot(t, model.X, 'y-')            # Plot Back stress
R_hand, = plt.plot(t, model.R, 'r-')            # Plot Drag stress
stress_hand, = plt.plot(t, model.sigma, 'b-')   # Plot Total stress
plt.ylabel('Stress [MPa]')
plt.xlabel('Time [s]')
plt.legend((X_hand, R_hand, stress_hand),
           (r'Back stress ($\chi$)', r'Drag stress (R)', r'Total Stress ($\sigma$)'))
plt.savefig('X_R_eps_1d.png')

# Plot total stress in function of total stress
plt.figure(figsize=(8, 5), dpi=80)
plt.style.use(style)
plt.axis('auto')
h, = plt.plot(model.ttotalstrain,model.sigma, 'k-')
plt.ylabel('Stress [MPa]')
plt.xlabel('Srain [%]')
plt.savefig('stress_strain_1d.png')

plt.show() # Show plots
