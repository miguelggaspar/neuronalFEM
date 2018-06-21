import pandas as pd
import matplotlib.pyplot as plt

# Import data to make graphs
df = pd.read_csv("data.csv")
# Ploting style
style = 'ggplot'


# Plot Total, Elastic and Inelastic Strains
def save_graph(legends, n_hand, data, labels, name):
    plt.figure(figsize=(8, 5), dpi=80)
    plt.style.use(style)
    # plt.ylim(-0.075, 0.075)                      # set the xlim to xmin, xmax
    color = ['b', 'r', 'k']
    fig, ax = plt.subplots(3, 1, sharex=True, sharey=True)
    fig.text(0.51, 0.035, labels[0], ha='center')
    fig.text(0.02, 0.5, labels[1], va='center', rotation='vertical')
    for n in range(n_hand):
        plt.subplot(n_hand, 1, n+1)
        plt.plot(data[0], data[n+1], color[n])
        plt.axis('auto')
        plt.legend(legends[n:], loc=0)
    plt.savefig(name)


# Plot and save graphs of back stress rate
legend = [r'$\dot \chi_{x}$',
          r'$\dot \chi_{y}$',
          r'$\dot \chi_{xy}$']
data = [df['Time'], df['dX11'], df['dX22'], df['dX12']]
labels = ['Time [s]', r'Stress rate [$\frac{MPa}{s}$]']
save_graph(legend, 3, data, labels, 'graphs/dX_2d')

# Plot and save graphs of Back stress
legend = [r'$\chi_{x}$',
          r'$\chi_{y}$',
          r'$\chi_{xy}$']
data = [df['Time'], df['X11'], df['X22'], df['X12']]
labels = ['Time [s]', 'Stress [MPa]']
save_graph(legend, 3, data, labels, 'graphs/X_2d')

# Plot and save graphs of Total Stress
legend = [r'$\sigma_{x}$',
          r'$\sigma_{y}$',
          r'$\sigma_{xy}$']
data = [df['Time'], df['S11'], df['S22'], df['S12']]
labels = ['Time [s]', 'Stress [MPa]']
save_graph(legend, 3, data, labels, 'graphs/S_2d')

# Plot and save graphs of Drag stress and it's rate
legend = [r'$\dot R$', r'R']
data = [df['Time'], df['dR'], df['R']]
labels = ['Time [s]', 'Stress [MPa]']
save_graph(legend, 2, data, labels, 'graphs/R_dR_2d')

# Plot and save graphs of Total Strain
legend = [r'$\varepsilon^t_{x}$',
          r'$\varepsilon^t_{y}$',
          r'$\varepsilon^t_{xy}$']
data = [df['Time'], df['ET11'], df['ET22'], df['ET12']]
labels = ['Time [s]', 'Strain [%]']
save_graph(legend, 3, data, labels, 'graphs/ET_2d')

# Plot and save graphs of Inelastic Strain
legend = [r'$\varepsilon^{in}_{x}$',
          r'$\varepsilon^{in}_{y}$',
          r'$\varepsilon^{in}_{xy}$']
data = [df['Time'], df['Ei11'], df['Ei22'], df['Ei12']]
labels = ['Time [s]', 'Strain [%]']
save_graph(legend, 3, data, labels, 'graphs/Ei_2d')

# Plot and save graphs of Inelastic Strain rate
legend = [r'$\dot \varepsilon^{in}_{x}$',
          r'$\dot \varepsilon^{in}_{y}$',
          r'$\dot \varepsilon^{in}_{xy}$']
data = [df['Time'], df['dEi11'], df['dEi22'], df['dEi12']]
labels = ['Time [s]', 'Strain [%]']
save_graph(legend, 3, data, labels, 'graphs/dEi_2d')

# Plot and save graphs of Plastic Strain and it's rate
legend = [r'$\dot p$', r'$p$']
data = [df['Time'], df['dpStrain'], df['pStrain']]
labels = ['Time [s]', 'Strain [%]']
save_graph(legend, 2, data, labels, 'graphs/p_dp_2d')

# Duvidas :
# - Como e que eu represento o reverse cyclic loading
# -
