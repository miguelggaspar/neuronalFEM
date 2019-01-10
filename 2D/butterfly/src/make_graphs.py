import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from utils import get_data, rename_headers, get_dataframe

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
        plt.grid()
        if condition == 1:
            plt.plot(data[2*n], data[2*n+1], label=legend[n], color=color[n])
        elif condition == 0:
            plt.plot(data[0], data[n+1], label=legend[n], color=color[n])
        elif condition == 2:
            plt.plot(data[0], data[2], label=legends[2*n], color='b')
            plt.plot(data[1], data[3], label=legends[2*n+1], color='r', marker='.')
        elif condition == 3:
            # plots = []
            # plots.append(plt.plot(data[0], data[2], label=legends[0]))
            plt.plot(data[0], data[2], label=legends[0])
            plt.plot(data[1], data[3], label=legends[1], marker='.')
            plt.plot(data[0], data[4], label=legends[2])
            plt.plot(data[1], data[5], label=legends[3], marker='.')
            plt.plot(data[0], data[6], label=legends[4])
            plt.plot(data[1], data[7], label=legends[5], marker='.')
            # for i in range(0,6):
            #     print(plots[i][0].get_color())
        elif condition == 4:
            plt.plot(data[3*n], data[3*n+1], label=legends[2*n], color=color[2*n])
            plt.plot(data[3*n], data[3*n+2], label=legends[2*n+1], color=color[2*n+1])
        elif condition == 5:
            plt.plot(data[3*n], data[3*n+1], label=legends[2*n], color='b')
            plt.plot(data[3*n], data[3*n+2], label=legends[2*n+1], color='r', marker='*')
        plt.axis('auto')
        # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.legend(loc='best',prop={'size': 9})
        # plt.legend(legends[n:], loc=0)
    plt.savefig(name + '.png', bbox_inches='tight')


# Driver program
if __name__ == "__main__":
    workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/butterfly/'
    abaqus_dir = '/home/miguel/Documents/tese/ViscoPlastic-ML/abaqus_deploy/butterfly/'

    P = 'P_1'
    el_num = 75

    P = ['P_1', 'P_2', 'P_3']
    el_num = [75, 322, 229]

    for n in range(0,3):
        data_dir = []
        data_dir.append(abaqus_dir + 'state_butterfly_hist.txt')
        data_dir.append(workdir + '/results/' + P[n] + '/data_' + P[n] + '.csv')
        data_dir.append(abaqus_dir + 'deriv_butterfly_hist.txt')
        abaqus, chaboche = get_data(data_dir)
        abaqus = rename_headers(abaqus)

        # Select from abaqus dataframe info about el_num and int_point
        fea = get_dataframe(abaqus, el_num[n], 2)
        # remove repeated values
        # Plot and save graphs of Back stress

        #TODO make the graphs

        legend = [r'Experimental $\chi_{xx}$',r'ANN $\chi_{xx}$',
                  r'Experimental $\chi_{yy}$',r'ANN $\chi_{yy}$',
                  r'Experimental $\chi_{xy}$',r'ANN $\chi_{xy}$']

        data = [chaboche['Time'], fea['t'], chaboche['X11'], fea['X11'], chaboche['X22'],
                fea['X22'], chaboche['X12'], fea['X12']]
        labels = ['Time [s]', 'Stress [MPa]']
        save_graph(legend, 1, data, labels, workdir + 'graphs/' + P[n] + '/comp_X_but', 3)


        legend = [r'Experimental $\sigma_{xx}$',r'ANN $\sigma_{xx}$',
                  r'Experimental $\sigma_{yy}$',r'ANN $\sigma_{yy}$',
                  r'Experimental $\tau_{xy}$',r'ANN $\tau_{xy}$']

        data = [chaboche['Time'], fea['t'], chaboche['S11'], fea['S11'], chaboche['S22'],
                fea['S22'], chaboche['S12'], fea['S12']]
        labels = ['Time [s]', 'Stress [MPa]']
        save_graph(legend, 1, data, labels, workdir + 'graphs/' + P[n] + '/comp_S_but', 3)


        legend = [r'Experimental $\varepsilon^{vp}_{xx}$',r'ANN $\varepsilon^{vp}_{xx}$',
                  r'Experimental $\varepsilon^{vp}_{yy}$',r'ANN $\varepsilon^{vp}_{yy}$',
                  r'Experimental $\varepsilon^{vp}_{xy}$',r'ANN $\varepsilon^{vp}_{xy}$']

        data = [chaboche['Time'], fea['t'], chaboche['Ei11'], fea['Ei11'], chaboche['Ei22'],
                fea['Ei22'], chaboche['Ei12'], fea['Ei12']]
        labels = ['Time [s]', 'Strain']
        save_graph(legend, 1, data, labels, workdir + 'graphs/' + P[n] + '/comp_EI_but', 3)

        legend = ['Experimental', 'ANN']

        data = [chaboche['Time'], fea['t'], chaboche['R'], fea['R']]
        labels = ['Time [s]', 'Stress [MPa]']
        save_graph(legend, 1, data, labels, workdir + 'graphs/' + P[n] + '/comp_R_but', 2)


        data = [chaboche['Time'], fea['t'], chaboche['pStrain'], fea['p']]
        labels = ['Time [s]', 'Strain']
        save_graph(legend, 1, data, labels, workdir + 'graphs/' + P[n] + '/comp_p_but', 2)


        break
