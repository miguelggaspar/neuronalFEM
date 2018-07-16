import pandas as pd
import matplotlib.pyplot as plt

print ('Creating and saving graphs for the dataset')
workdir = '/home/miguel/UA/tese/ViscoPlastic-ML/2 Dimensions/dataset/graphs/'
trials = ['xx', 'yy', 'xy']
# Ploting style
style = 'ggplot'
for trial in trials:
    print ('Trial:', trial)
    # Import data to make graphs
    df = pd.read_csv(workdir + "../results/data_" + trial + ".csv")

    # Plot Total, Elastic and Inelastic Strains
    def save_graph(legends, n_hand, data, labels, name, condition):
        plt.figure(figsize=(8, 5), dpi=80)
        plt.style.use(style)
        # plt.ylim(-0.075, 0.075)                      # set the xlim to xmin, xmax
        color = ['b', 'r', 'k']
        fig, ax = plt.subplots(3, 1, sharex=True, sharey=True)
        fig.text(0.51, 0.035, labels[0], ha='center')
        fig.text(0.02, 0.5, labels[1], va='center', rotation='vertical')
        for n in range(n_hand):
            plt.subplot(n_hand, 1, n+1)
            if condition == 1:
                plt.plot(data[2*n], data[2*n+1], color[n])
            else:
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
    save_graph(legend, 3, data, labels, workdir + trial + '/dX_2d', 0)

    # Plot and save graphs of Back stress
    legend = [r'$\chi_{x}$',
              r'$\chi_{y}$',
              r'$\chi_{xy}$']
    data = [df['Time'], df['X11'], df['X22'], df['X12']]
    labels = ['Time [s]', 'Stress [MPa]']
    save_graph(legend, 3, data, labels, workdir + trial + '/X_2d', 0)

    # Plot and save graphs of Total Stress
    legend = [r'$\sigma_{x}$',
              r'$\sigma_{y}$',
              r'$\sigma_{xy}$']
    data = [df['Time'], df['S11'], df['S22'], df['S12']]
    labels = ['Time [s]', 'Stress [MPa]']
    save_graph(legend, 3, data, labels, workdir + trial + '/S_2d', 0)

    # Plot and save graphs of Drag stress and it's rate
    legend = [r'$\dot R$', r'R']
    data = [df['Time'], df['dR'], df['R']]
    labels = ['Time [s]', 'Stress [MPa]']
    save_graph(legend, 2, data, labels, workdir + trial + '/R_dR_2d', 0)

    # Plot and save graphs of Total Strain
    legend = [r'$\varepsilon^t_{x}$',
              r'$\varepsilon^t_{y}$',
              r'$\varepsilon^t_{xy}$']
    data = [df['Time'], df['ET11'], df['ET22'], df['ET12']]
    labels = ['Time [s]', 'Strain [%]']
    save_graph(legend, 3, data, labels, workdir + trial + '/ET_2d', 0)

    # Plot and save graphs of Elastic Strain
    legend = [r'$\varepsilon^e_{x}$',
              r'$\varepsilon^e_{y}$',
              r'$\varepsilon^e_{xy}$']
    data = [df['Time'], df['Ee11'], df['Ee22'], df['Ee12']]
    labels = ['Time [s]', 'Strain [%]']
    save_graph(legend, 3, data, labels, workdir + trial + '/Ee_2d', 0)

    # Plot and save graphs of Inelastic Strain
    legend = [r'$\varepsilon^{in}_{x}$',
              r'$\varepsilon^{in}_{y}$',
              r'$\varepsilon^{in}_{xy}$']
    data = [df['Time'], df['Ei11'], df['Ei22'], df['Ei12']]
    labels = ['Time [s]', 'Strain [%]']
    save_graph(legend, 3, data, labels, workdir + trial + '/Ei_2d', 0)

    # Plot and save graphs of Inelastic Strain rate
    legend = [r'$\dot \varepsilon^{in}_{x}$',
              r'$\dot \varepsilon^{in}_{y}$',
              r'$\dot \varepsilon^{in}_{xy}$']
    data = [df['Time'], df['dEi11'], df['dEi22'], df['dEi12']]
    labels = ['Time [s]','Strain [%]']
    save_graph(legend, 3, data, labels, workdir + trial + '/dEi_2d', 0)

    # Plot and save graphs of Plastic Strain and it's rate
    legend = [r'$\dot p$', r'$p$']
    data = [df['Time'], df['dpStrain'], df['pStrain']]
    labels = ['Time [s]', 'Strain [%]']
    save_graph(legend, 2, data, labels, workdir + trial + '/p_dp_2d', 0)

    # Plot and save graphs of Plastic Strain and it's rate
    legend = ['xx', 'yy', 'xy']
    data = [df['ET11'], df['S11'], df['ET22'], df['S22'], df['ET12'],  df['S12']]
    labels = ['Strain [%]', 'Stress [MPa]']
    save_graph(legend, 3, data, labels, workdir + trial + '/ET_S_2d', 1)

    # Close all figures
    plt.close('all')
    # Duvidas :
    # - Como e que eu represento o reverse cyclic loading
    # -
print ('Done creating graphs')
