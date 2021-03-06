import pandas as pd
import matplotlib.pyplot as plt
import sys
print ('Creating and saving graphs for the dataset')
workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/dataset/graphs/'
trials = ['xx', 'yy', 'xy']
# Ploting style
style = 'ggplot'
Emaxs = []
for k in range(len(sys.argv)):
    if (len(sys.argv) - k) == 1:
        break
    Emaxs.append(float(sys.argv[k+1]))

for Emax in Emaxs:
    for trial in trials:
        print ('Trial:', trial)
        # Import data to make graphs
        df = pd.read_csv(workdir + "../results/data_"+ str(Emax) + "_" + trial + ".csv")

        # Plot Total, Elastic and Inelastic Strains
        def save_graph(legends, n_hand, data, labels, name, condition):
            plt.figure(figsize=(8, 5), dpi=80)
            # plt.style.use(style)
            # plt.ylim(-0.075, 0.075)                      # set the xlim to xmin, xmax
            color = ['b', 'r', 'k']
            fig, ax = plt.subplots(3, 1, sharex=True, sharey=True)
            fig.text(0.51, 0.035, labels[0], ha='center')
            fig.text(0.02, 0.5, labels[1], va='center', rotation='vertical')
            for n in range(n_hand):
                plt.subplot(n_hand, 1, n+1)
                if condition == 1:
                    plt.plot(data[2*n], data[2*n+1], label=legend[n], color=color[n])
                elif condition == 0:
                    plt.plot(data[0], data[n+1], label=legend[n], color=color[n])
                elif condition == 2:
                    plt.plot(data[0], data[1], label=legend[n])
                    plt.plot(data[0], data[2], label=legend[n+1])
                    plt.plot(data[0], data[3], label=legend[n+2])
                plt.axis('auto')
                plt.grid()
                plt.ylim([-0.16,0.16])
                plt.xlim([0,80])
                # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
                plt.legend(legends[n:], loc='best')
            plt.savefig(name + '.png', bbox_inches='tight')
        #
        # # Plot and save graphs of back stress rate
        # legend = [r'$\dot \chi_{x}$',
        #           r'$\dot \chi_{y}$',
        #           r'$\dot \chi_{xy}$']
        # data = [df['Time'], df['dX11'], df['dX22'], df['dX12']]
        # labels = ['Time [s]', r'Stress rate [$\frac{MPa}{s}$]']
        # save_graph(legend, 3, data, labels, workdir + trial + '/' + str(Emax) + '_dX_2d', 0)
        #
        # # Plot and save graphs of Back stress
        # legend = [r'$\chi_{x}$',
        #           r'$\chi_{y}$',
        #           r'$\chi_{xy}$']
        # data = [df['Time'], df['X11'], df['X22'], df['X12']]
        # labels = ['Time [s]', 'Stress [MPa]']
        # save_graph(legend, 3, data, labels, workdir + trial + '/' + str(Emax) + '_X_2d', 0)
        #
        # # Plot and save graphs of Total Stress
        # legend = [r'$\sigma_{x}$',
        #           r'$\sigma_{y}$',
        #           r'$\sigma_{xy}$']
        # data = [df['Time'], df['S11'], df['S22'], df['S12']]
        # labels = ['Time [s]', 'Stress [MPa]']
        # save_graph(legend, 3, data, labels, workdir + trial + '/' + str(Emax) + '_S_2d', 0)
        #
        # # Plot and save graphs of Drag stress and it's rate
        # legend = [r'$\dot R$', r'R']
        # data = [df['Time'], df['dR'], df['R']]
        # labels = ['Time [s]', 'Stress [MPa]']
        # save_graph(legend, 2, data, labels, workdir + trial + '/' + str(Emax) + '_R_dR_2d', 0)
        #
        # # Plot and save graphs of Total Strain
        # legend = [r'$\varepsilon^t_{x}$',
        #           r'$\varepsilon^t_{y}$',
        #           r'$\varepsilon^t_{xy}$']
        # data = [df['Time'], df['ET11'], df['ET22'], df['ET12']]
        # labels = ['Time [s]', 'Strain [%]']
        # save_graph(legend, 3, data, labels, workdir + trial + '/' + str(Emax) + '_ET_2d', 0)
        #
        # # Plot and save graphs of Elastic Strain
        # legend = [r'$\varepsilon^e_{x}$',
        #           r'$\varepsilon^e_{y}$',
        #           r'$\varepsilon^e_{xy}$']
        # data = [df['Time'], df['Ee11'], df['Ee22'], df['Ee12']]
        # labels = ['Time [s]', 'Strain [%]']
        # save_graph(legend, 3, data, labels, workdir + trial + '/' + str(Emax) + '_Ee_2d', 0)
        #
        # # Plot and save graphs of Inelastic Strain
        # legend = [r'$\varepsilon^{in}_{x}$',
        #           r'$\varepsilon^{in}_{y}$',
        #           r'$\varepsilon^{in}_{xy}$']
        # data = [df['Time'], df['Ei11'], df['Ei22'], df['Ei12']]
        # labels = ['Time [s]', 'Strain [%]']
        # save_graph(legend, 3, data, labels, workdir + trial + '/' + str(Emax) + '_Ei_2d', 0)
        #
        # # Plot and save graphs of Inelastic Strain rate
        # legend = [r'$\dot \varepsilon^{in}_{x}$',
        #           r'$\dot \varepsilon^{in}_{y}$',
        #           r'$\dot \varepsilon^{in}_{xy}$']
        # data = [df['Time'], df['dEi11'], df['dEi22'], df['dEi12']]
        # labels = ['Time [s]','Strain [%]']
        # save_graph(legend, 3, data, labels, workdir + trial + '/' + str(Emax) + '_dEi_2d', 0)
        #
        # # Plot and save graphs of Plastic Strain and it's rate
        # legend = [r'$\dot p$', r'$p$']
        # data = [df['Time'], df['dpStrain'], df['pStrain']]
        # labels = ['Time [s]', 'Strain [%]']
        # save_graph(legend, 2, data, labels, workdir + trial + '/' + str(Emax) + '_p_dp_2d', 0)
        #
        # # Plot and save graphs for reverse cyclcic loading
        # legend = ['xx', 'yy', 'xy']
        # data = [df['ET11'], df['S11'], df['ET22'], df['S22'], df['ET12'],  df['S12']]
        # labels = ['Strain [%]', 'Stress [MPa]']
        # save_graph(legend, 3, data, labels, workdir + trial + '/' + str(Emax) + '_ET_S_2d', 1)
        #

        legend = [r'$\varepsilon^{t}_{xx}$',
                  r'$\varepsilon^{t}_{yy}$',
                  r'$\varepsilon^{t}_{xy}$']
        data = [df['Time'][:1564], df['ET11'][:1564], df['ET22'][:1564], df['ET12'][:1564]]
        labels = ['Time [s]', 'Strain']
        save_graph(legend, 1, data, labels, workdir + trial + '/' + str(Emax) + '_ET_5s_2d', 2)

        # Close all figures
        plt.close('all')
    # Duvidas :
    # - Como e que eu represento o reverse cyclic loading
    # -
print ('Done creating graphs')
