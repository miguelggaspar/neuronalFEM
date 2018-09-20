import pandas as pd
import matplotlib.pyplot as plt
from compare_utils import save_graphs, get_score


print ('Creating and saving graphs for the tested model')
workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/testmodel/'
workd_gra = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/testmodel/graphs/'
trials = ['xx', 'yy', 'xy']
style = 'ggplot'
Emaxs = [0.025, 0.036, 0.05]

for Emax in Emaxs:
    for trial in trials:
        print ('Trial: ', trial, 'Emax: ', Emax)
        df = pd.read_csv(workdir + "../dataset/results/data_" + str(Emax) + "_" + trial + ".csv")
        pred = pd.read_csv(workdir + "results/predictions_" + str(Emax) + "_" + trial + "_2d.csv")

        # Plot and save graphs of back stress rate
        legend = [r'Predicted $\dot \chi_{x}$', r'Real $\dot \chi_{x}$',
                  r'Predicted $\dot \chi_{y}$', r'Real $\dot \chi_{y}$',
                  r'Predicted $\dot \chi_{xy}$', r'Real $\dot \chi_{xy}$']
        data = [df['Time'], pred['dX11'], df['dX11'],  pred['dX22'],
                df['dX22'], pred['dX12'], df['dX12']]
        labels = ['Time [s]', r'Stress rate [$\frac{MPa}{s}$]', trial]
        save_graphs(legend, 3, data, labels, workd_gra + trial + '/comp_'
                    + str(Emax) +'_dX_' + trial + '_2d', 0)

        # Plot and save graphs of Back stress
        legend = [r'Predicted $\chi_{x}$', r'Real $\chi_{x}$',
                  r'Predicted $\chi_{y}$', r'Real $\chi_{y}$',
                  r'Predicted $\chi_{xy}$', r'Real $\chi_{xy}$']
        data = [df['Time'], pred['X11'], df['X11'], pred['X22'], df['X22'],
                pred['X12'], df['X12']]
        labels = ['Time [s]', 'Stress [MPa]', trial]
        save_graphs(legend, 3, data, labels, workd_gra + trial + '/comp_'
                    + str(Emax) +'_X_' + trial + '_2d', 0)

        # Plot and save graphs of Total Stress
        legend = [r'Predicted $\sigma_{x}$', r'Real $\sigma_{x}$',
                  r'Predicted $\sigma_{y}$', r'Real $\sigma_{y}$',
                  r'Predicted $\sigma_{xy}$', r'Real $\sigma_{xy}$']
        data = [df['Time'], pred['S11'], df['S11'], pred['S22'], df['S22'],
                pred['S12'], df['S12']]
        labels = ['Time [s]', 'Stress [MPa]', trial]
        save_graphs(legend, 3, data, labels, workd_gra + trial + '/comp_'
                    + str(Emax) + '_S_' + trial + '_2d', 0)

        # Plot and save graphs of Drag stress and it's rate
        legend = [r'Predicted $\dot R$', r'Real $\dot R$', r'Predicted R', r'Real R']
        data = [df['Time'], pred['dR'], df['dR'], pred['R'], df['R']]
        labels = ['Time [s]', 'Stress [MPa]', trial]
        save_graphs(legend, 2, data, labels, workd_gra + trial + '/comp_'
                    + str(Emax) + '_R_dR_' + trial + '_2d', 0)

        # Plot and save graphs of Total Strain
        legend = [r'$\varepsilon^t_{x}$',
                  r'$\varepsilon^t_{y}$',
                  r'$\varepsilon^t_{xy}$']
        data = [df['Time'], df['ET11'], df['ET22'], df['ET12']]
        labels = ['Time [s]', 'Strain [%]', trial]
        save_graphs(legend, 3, data, labels, workd_gra + trial + '/comp_'
                    + str(Emax) + '_ET_' + trial + '_2d', 1)

        # Plot and save graphs of Inelastic Strain
        legend = [r'Predicted $\varepsilon^{in}_{x}$', r'Real $\varepsilon^{in}_{x}$',
                  r'Predicted $\varepsilon^{in}_{y}$', r'Real $\varepsilon^{in}_{y}$',
                  r'Predicted $\varepsilon^{in}_{xy}$', r'Real $\varepsilon^{in}_{xy}$']
        data = [df['Time'], pred['Ei11'], df['Ei11'], pred['Ei22'], df['Ei22'],
                pred['Ei12'], df['Ei12']]
        labels = ['Time [s]', 'Strain [%]', trial]
        save_graphs(legend, 3, data, labels, workd_gra + trial + '/comp_'
                    + str(Emax) + '_Ei_' + trial + '_2d', 0)

        # Plot and save graphs of Inelastic Strain rate
        legend = [r'Predicted $\dot \varepsilon^{in}_{x}$',
                  r'Real $\dot \varepsilon^{in}_{x}$',
                  r'Predicted $\dot \varepsilon^{in}_{y}$',
                  r'Real $\dot \varepsilon^{in}_{y}$',
                  r'Predicted $\dot \varepsilon^{in}_{xy}$',
                  r'Real $\dot \varepsilon^{in}_{xy}$']
        data = [df['Time'], pred['dEi11'], df['dEi11'], pred['dEi22'], df['dEi22'],
                pred['dEi12'], df['dEi12']]
        labels = ['Time [s]', 'Strain [%]', trial]
        save_graphs(legend, 3, data, labels, workd_gra + trial + '/comp_'
                    + str(Emax) + '_dEi_' + trial + '_2d', 0)

        # Plot and save graphs of Plastic Strain and it's rate
        legend = [r'Predicted $\dot p$', r'Real $\dot p$',
                  r'Predicted $p$', r'Real $p$' ]
        data = [df['Time'], pred['dpStrain'], df['dpStrain'], pred['pStrain'], df['pStrain']]
        labels = ['Time [s]', 'Strain [%]', trial]
        save_graphs(legend, 2, data, labels, workd_gra + trial + '/comp_'
                    + str(Emax) + '_p_dp_' + trial + '_2d', 0)
        # Close all figures
        plt.close('all')

        workdir_ann = '../train/model/'
        get_score(workdir_ann, df)
print ('Done creating graphs')
