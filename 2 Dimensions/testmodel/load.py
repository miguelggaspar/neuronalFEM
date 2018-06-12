import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../dataset/data.csv")
pred = pd.read_csv("predictions_2d.csv")
style = 'ggplot'


# Plot Total, Elastic and Inelastic Strains
def save_graph(legends, n_hand, data, labels, name, condition):
    plt.figure(figsize=(8, 5), dpi=80)
    plt.style.use(style)
    # plt.ylim(-0.075, 0.075)                         # set the xlim to xmin, xmax
    color = ['b', 'r', 'k', 'g', 'y', 'brown']
    fig, ax = plt.subplots(3, 1, sharex=True, sharey=True)
    fig.text(0.51, 0.035, labels[0], ha='center')
    fig.text(0.02, 0.5, labels[1], va='center', rotation='vertical')
    for n in range(n_hand):
        plt.subplot(n_hand, 1, n+1)
        if condition == 1:
            plt.plot(data[0], data[n+1], color[n])
        else:
            plt.plot(data[0], data[2*n+1], color[2*n])
            plt.plot(data[0], data[2*n+2], color[2*n+1])
        plt.legend(legends[n:])
    plt.savefig(name)


# Plot and save graphs of back stress rate
legend = [r'Predicted $\dot \chi_{xx}$', r'Real $\dot \chi_{xx}$',
          r'Predicted $\dot \chi_{yy}$', r'Real $\dot \chi_{yy}$',
          r'Predicted $\dot \chi_{xy}$', r'Real $\dot \chi_{xy}$']
data = [df['Time'], pred['dX11'], df['dX11'],  pred['dX22'],
        df['dX22'], pred['dX12'], df['dX12']]
labels = ['Time [s]', r'Stress rate [$\frac{MPa}{s}$]']
save_graph(legend, 3, data, labels, 'graphs/comp_Back_stress_rate_2d', 0)

# Plot and save graphs of Back stress
legend = [r'Predicted $\chi_{xx}$', r'Real $\chi_{xx}$',
          r'Predicted $\chi_{yy}$', r'Real $\chi_{yy}$',
          r'Predicted $\chi_{xy}$', r'Real $\chi_{xy}$']
data = [df['Time'], pred['X11'], df['X11'], pred['X22'], df['X22'],
        pred['X12'], df['X12']]
labels = ['Time [s]', 'Stress [MPa]']
save_graph(legend, 3, data, labels, 'graphs/comp_Back_stress_2d', 0)

# Plot and save graphs of Total Stress
legend = [r'Predicted $\sigma_{xx}$', r'Real $\sigma_{xx}$',
          r'Predicted $\sigma_{yy}$', r'Real $\sigma_{yy}$',
          r'Predicted $\sigma_{xy}$', r'Real $\sigma_{xy}$']
data = [df['Time'], pred['S11'], df['S11'], pred['S22'], df['S22'],
        pred['S12'], df['S12']]
labels = ['Time [s]', 'Stress [MPa]']
save_graph(legend, 3, data, labels, 'graphs/comp_Total_stress_2d', 0)

# Plot and save graphs of Drag stress and it's rate
legend = [r'Predicted $\dot R$', r'Real $\dot R$', r'Predicted R', r'Real R']
data = [df['Time'], pred['dR'], df['dR'], pred['R'], df['R']]
labels = ['Time [s]', 'Stress [MPa]']
save_graph(legend, 2, data, labels, 'graphs/comp_Drag_stress_andrate_2d', 0)

# Plot and save graphs of Total Strain
legend = [r'$\varepsilon^t_{xx}$',
          r'$\varepsilon^t_{yy}$',
          r'$\varepsilon^t_{xy}$']
data = [df['Time'], df['ET11'], df['ET22'], df['ET12']]
labels = ['Time [s]', 'Strain [%]']
save_graph(legend, 3, data, labels, 'graphs/Total_strain_2d', 1)

# Plot and save graphs of Inelastic Strain
legend = [r'Predicted $\varepsilon^{in}_{xx}$', r'Real $\varepsilon^{in}_{xx}$',
          r'Predicted $\varepsilon^{in}_{yy}$', r'Real $\varepsilon^{in}_{yy}$',
          r'Predicted $\varepsilon^{in}_{xy}$', r'Real $\varepsilon^{in}_{xy}$']
data = [df['Time'], pred['Ei11'], df['Ei11'], pred['Ei22'], df['Ei22'],
        pred['Ei12'] ,df['Ei12']]
labels = ['Time [s]', 'Strain [%]']
save_graph(legend, 3, data, labels, 'graphs/comp_inelastic_strain_2d', 0)

# Plot and save graphs of Inelastic Strain rate
legend = [r'Predicted $\dot \varepsilon^{in}_{xx}$',
          r'Real $\dot \varepsilon^{in}_{xx}$',
          r'Predicted $\dot \varepsilon^{in}_{yy}$',
          r'Real $\dot \varepsilon^{in}_{yy}$',
          r'Predicted $\dot \varepsilon^{in}_{xy}$',
          r'Real $\dot \varepsilon^{in}_{xy}$']
data = [df['Time'], pred['dEi11'], df['dEi11'], pred['dEi22'], df['dEi22'],
        pred['dEi12'], df['dEi12']]
labels = ['Time [s]', 'Strain [%]']
save_graph(legend, 3, data, labels, 'graphs/comp_inelastic_strain_2d', 0)

# Plot and save graphs of Plastic Strain and it's rate
legend = [r'Predicted $\dot p$', r'Real $p$']
data = [df['Time'], pred['dpStrain'], df['dpStrain'], pred['pStrain'], df['pStrain']]
labels = ['Time [s]', 'Strain [%]']
save_graph(legend, 2, data, labels, 'graphs/comp_plastic_strain_and_rate_2d', 0)

#Duvidas :
    # - Como e que eu represento o reverse cyclic loading
    # -
