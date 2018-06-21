import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../dataset/data.csv")
pred = pd.read_csv("predictions_1d.csv")
style = 'ggplot'


# Save figure to png file
def save_graph(legends, n_hand, data, labels, name, condition):
    fig = plt.figure(figsize=(8, 5), dpi=80)
    plt.style.use(style)
    # plt.ylim(-0.075, 0.075)                   # set the xlim to xmin, xmax
    color = ['b', 'r', 'k', 'g', 'y', 'brown']
    fig.text(0.51, 0.035, labels[0], ha='center')
    fig.text(0.02, 0.5, labels[1], va='center', rotation='vertical')
    for n in range(n_hand):
        if condition == 1:
            plt.plot(data[2*n], data[2*n+1], color[n])
        else:
            plt.plot(data[0], data[n+1], color[n])
    plt.legend(legends[:], loc=0)
    plt.savefig(name)


# Plot Total, Elastic and Inelastic Strains
legend = [r'$\varepsilon^{vp}_{real}$',
          r'$\varepsilon^{vp}_{pred}$']
data = [df['Time'], df['IStrain'], pred['EI']]
labels = ['Time [s]', 'Strain [%]']
save_graph(legend, 2, data, labels, 'graphs/comp_instrain_1d', 0)

# Plot and save graphs of Back stress rate
legend = [r'$\dot \chi_{real}$',
          r'$\dot \chi_{pred}$']
data = [df['Time'], df['dX'], pred['dX']]
labels = ['Time [s]', r'Stress rate $[\frac{MPa}{s}]$']
save_graph(legend, 2, data, labels, 'graphs/comp_back_stress_rate_1d', 0)

# Plot and save graphs of Drag stress rate
legend = [r'$\dot R_{real}$',
          r'$\dot R_{pred}$']
data = [df['Time'], df['dR'], pred['dR']]
labels = ['Time [s]',  r'Stress rate $[\frac{MPa}{s}]$']
save_graph(legend, 2, data, labels, 'graphs/comp_drag_stress_rate_1d', 0)

# Plot and save graphs of Inelastic strain rate
legend = [r'$\dot \varepsilon^{vp}_{real}$',
          r'$\dot \varepsilon^{vp}_{pred}$']
data = [df['Time'], df['dIStrain'], pred['dEI']]
labels = ['Time [s]',  r'Strain rate $[\frac{\%}{s}]$']
save_graph(legend, 2, data, labels, 'graphs/comp_instrain_rate_1d', 0)

# Plot and save graphs of Back stress
legend = [r'$\chi_{real}$',
          r'$\chi_{pred}$']
data = [df['Time'], df['X'], pred['X']]
labels = ['Time [s]', r'Stress [MPa]']
save_graph(legend, 2, data, labels, 'graphs/comp_back_stress_1d', 0)

# Plot and save graphs of Drag stress
legend = [r'$R_{real}$',
          r'$R_{pred}$']
data = [df['Time'], df['R'], pred['R']]
labels = ['Time [s]', r'Stress [MPa]']
save_graph(legend, 2, data, labels, 'graphs/comp_drag_stress_1d', 0)

# Plot and save graphs of Stress
legend = [r'$R_{real}$', r'$R_{pred}$',
          r'$\chi_{real}$', r'$\chi_{pred}$',
          r'$\sigma_{real}$', r'$\sigma_{pred}$']
data = [df['Time'], df['R'], pred['R'], df['X'], pred['X'], df['Stress'], pred['S']]
labels = ['Time [s]', 'Stress [MPa]']
save_graph(legend, 6, data, labels, 'graphs/comp_X_R_sigma_1d', 0)

# Plot and save graphs of Stress
legend = [r'$R_{pred}$',
          r'$\chi_{pred}$',
          r'$\sigma_{pred}$']
data = [df['Time'], pred['R'], pred['X'], pred['S']]
labels = ['Time [s]', 'Stress [MPa]']
save_graph(legend, 3, data, labels, 'graphs/X_R_sigma_1d', 0)

# Plot and save graphs of Stress - Strain
legend = ['Real cyclic loading',
          'Predicted cyclic loading']
data = [df['TStrain'], df['Stress'], pred['ET'], pred['S']]
labels = ['Total Strain [%]', 'Total Stress [MPa]']
save_graph(legend, 2, data, labels, 'graphs/comp_strain_stress_1d', 1)

plt.show()
