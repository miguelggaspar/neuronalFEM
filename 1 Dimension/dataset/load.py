import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")
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
legend = [r'$\varepsilon^{t}$',
          r'$\varepsilon^{vp}$',
          r'$\varepsilon^e$']
data = [df['Time'], df['TStrain'], df['IStrain'], df['EStrain']]
labels = ['Time [s]', 'Strain [%]']
save_graph(legend, 3, data, labels, 'graphs/total_el_in_strain_1d', 0)

# Plot and save graphs of Back stress rate
legend = [r'$\dot \chi$']
data = [df['Time'], df['dX']]
labels = ['Time [s]', r'Stress rate $[\frac{MPa}{s}]$']
save_graph(legend, 1, data, labels, 'graphs/dXdt_1d', 0)

# Plot and save graphs of Drag stress rate
legend = [r'$\dot R$']
data = [df['Time'], df['dR']]
labels = ['Time [s]',  r'Stress rate $[\frac{MPa}{s}]$']
save_graph(legend, 1, data, labels, 'graphs/dRdt_1d', 0)

# Plot and save graphs of Inelastic strain rate
legend = [r'$\dot \varepsilon^{vp}$']
data = [df['Time'], df['dIStrain']]
labels = ['Time [s]',  r'Strain rate $[\frac{\%}{s}]$']
save_graph(legend, 1, data, labels, 'graphs/depsdt_1d', 0)

# Plot and save graphs of Stress
legend = [r'$R$', r'$\chi$', r'$\sigma$']
data = [df['Time'], df['R'], df['X'], df['Stress']]
labels = ['Time [s]', 'Stress [MPa]']
save_graph(legend, 3, data, labels, 'graphs/X_R_sigma_1d', 0)

# Plot and save graphs of Stress - Strain
legend = ['Reverse cyclic loading']
data = [df['TStrain'], df['Stress']]
labels = ['Total Strain [%]', 'Total Stress [MPa]']
save_graph(legend, 1, data, labels, 'graphs/stress_strain_1d', 1)

plt.show()
