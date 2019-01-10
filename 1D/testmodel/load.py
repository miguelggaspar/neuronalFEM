import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../dataset/data_025_150.csv")
pred = pd.read_csv("pred_025_150.csv")
# style = 'ggplot'


def error(exact, pred):
    error = 100 - (pred * 100.0) / exact
    error2 = (abs(pred-exact)/exact)*100
    return error, error2

# Save figure to png file
def save_graph(legends, n_hand, data, labels, name, condition):
    fig = plt.figure(figsize=(8, 5), dpi=80)
    # plt.style.use(style)
    plt.grid()
    # plt.ylim(-0.075, 0.075)                   # set the xlim to xmin, xmax
    color = ['b', 'r', 'k', 'g', 'y', 'brown']
    fig.text(0.51, 0.015, labels[0], ha='center')
    # fig.text(0.02, 0.5, labels[1], va='center', rotation='vertical')

    for n in range(n_hand):
        if condition == 1:
            plt.plot(data[2*n], data[2*n+1], color[n])
            plt.legend(legends[:], loc=0, prop={'size': 11})
            fig.text(0.03, 0.5, labels[1], va='center', rotation='vertical')
            plt.xlim([-0.025,0.025])
        elif condition == 0:
            plt.plot(data[0], data[n+1], color[n])
            plt.legend(legends[:], loc=0)
            fig.text(0.03, 0.5, labels[1], va='center', rotation='vertical')
            plt.xlim([0,80])
        elif condition == 2:
            plt.plot(data[0], data[n+1], label=legend[n], color=color[n])
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., prop={'size': 10})
            fig.text(0.03, 0.5, labels[1], va='center', rotation='vertical')
            plt.xlim([0,80])
        elif condition == 3:
            plt.plot(data[0], data[n+1], color[n])
            plt.legend(legends[:], loc=0)
            fig.text(0.02, 0.5, labels[1], va='center', rotation='vertical')
            plt.xlim([0,80])
    plt.savefig(name, bbox_inches='tight')


# Plot Total, Elastic and Inelastic Strains
legend = ['Experimental',
          'ANN-model']
data = [df['Time'], df['IStrain'], pred['EI']]
labels = ['Time [s]', 'Strain [%]']
save_graph(legend, 2, data, labels, 'graphs_1d/comp_instrain_1d', 3)

# Plot and save graphs_1d of Back stress rate
# legend = [r'$\dot \chi_{real}$',
#           r'$\dot \chi_{pred}$']
data = [df['Time'], df['dX'], pred['dX']]
labels = ['Time [s]', r'Stress rate $[\frac{MPa}{s}]$']
save_graph(legend, 2, data, labels, 'graphs_1d/comp_back_stress_rate_1d', 0)

# Plot and save graphs_1d of Drag stress rate
# legend = [r'$\dot R_{real}$',
#           r'$\dot R_{pred}$']
data = [df['Time'], df['dR'], pred['dR']]
labels = ['Time [s]',  r'Stress rate $[\frac{MPa}{s}]$']
save_graph(legend, 2, data, labels, 'graphs_1d/comp_drag_stress_rate_1d', 0)

# Plot and save graphs_1d of Inelastic strain rate
# legend = [r'$\dot \varepsilon^{vp}_{real}$',
#           r'$\dot \varepsilon^{vp}_{pred}$']
data = [df['Time'], df['dIStrain'], pred['dEI']]
labels = ['Time [s]',  r'Strain rate $[\frac{\%}{s}]$']
save_graph(legend, 2, data, labels, 'graphs_1d/comp_instrain_rate_1d', 3)

# Plot and save graphs_1d of Back stress
# legend = [r'$\chi_{real}$',
#           r'$\chi_{pred}$']
data = [df['Time'], df['X'], pred['X']]
labels = ['Time [s]', r'Stress [MPa]']
save_graph(legend, 2, data, labels, 'graphs_1d/comp_back_stress_1d', 0)

# Plot and save graphs_1d of Drag stress
# legend = [r'$R_{real}$',
#           r'$R_{pred}$']
data = [df['Time'], df['R'], pred['R']]
labels = ['Time [s]', r'Stress [MPa]']
save_graph(legend, 2, data, labels, 'graphs_1d/comp_drag_stress_1d', 0)

# Plot and save graphs_1d of Stress
legend = [r'$R$ - Experimental', r'$R$ - ANN-model',
          r'$\chi$ - Experimental', r'$\chi$ - ANN-model',
          r'$\sigma$ - Experimental', r'$\sigma$ - ANN-model']
data = [df['Time'], df['R'], pred['R'], df['X'], pred['X'], df['Stress'], pred['S']]
labels = ['Time [s]', 'Stress [MPa]']
save_graph(legend, 6, data, labels, 'graphs_1d/comp_X_R_sigma_1d', 2)

# Plot and save graphs_1d of Stress
legend = [r'$R_{pred}$',
          r'$\chi_{pred}$',
          r'$\sigma_{pred}$']
data = [df['Time'], pred['R'], pred['X'], pred['S']]
labels = ['Time [s]', 'Stress [MPa]']
save_graph(legend, 3, data, labels, 'graphs_1d/X_R_sigma_1d', 2)

# Plot and save graphs_1d of Stress - Strain
legend = ['Experimental cyclic loading',
          'ANN-model cyclic loading']
data = [df['TStrain'], df['Stress'], pred['ET'], pred['S']]
labels = ['Total Strain [%]', 'Total Stress [MPa]']
save_graph(legend, 2, data, labels, 'graphs_1d/comp_strain_stress_1d', 1)

# Plot Total, Elastic and Inelastic Strains
legend = [r'$\varepsilon^{tot}$']
data = [df['Time'], pred['ET']]
labels = ['Time [s]', 'Strain [%]']
save_graph(legend, 1, data, labels, 'graphs_1d/comp_totstrain_1d', 3)

# plt.show()
