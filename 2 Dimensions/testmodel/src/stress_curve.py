import pandas as pd
import matplotlib.pyplot as plt
from compare_utils import save_graphs, get_index
import sys

print ('Creating and saving graphs for the tested model')
workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/testmodel/'
workd_gra = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/testmodel/graphs/stress_curves/'
trials = ['xx', 'yy', 'xy']
style = 'ggplot'


Emaxs = []
for k in range(len(sys.argv)):
    if (len(sys.argv) - k) == 3:
        break
    Emaxs.append(float(sys.argv[k+3]))

index = get_index(5, 0, int(sys.argv[2]), int(sys.argv[1]))
index2 = get_index(20, 0, int(sys.argv[2]), int(sys.argv[1]))

for Emax in Emaxs:
    for trial in trials:
        print ('Trial: ', trial, 'Emax: ', Emax)
        df = pd.read_csv(workdir + "../dataset/results/data_" + str(Emax) + "_" + trial + ".csv")
        pred = pd.read_csv(workdir + "results/predictions_" + str(Emax) + "_" + trial + "_2d.csv")

        legend = ['Predicted', 'Real']

        if trial == 'xx':
            data = [df['ET11'], pred['S11'], df['S11']]
        elif trial == 'yy':
            data = [df['ET22'], pred['S22'], df['S22']]
        elif trial == 'xy':
            data = [df['ET12'], pred['S12'], df['S12']]

        labels = ['Strain', 'Stress [MPa]',
                  'Trial ' + trial + r' with $\pm$' + str(Emax) + ' cyclic strain range']

        save_graphs(legend, 1, data, labels, workd_gra + 'comp_'
        + str(Emax) + '_ET_S_' + trial + '_2d', 2)

        if trial == 'xx':
            data = [df['ET11'][:index], pred['S11'][:index], df['S11'][:index]]
        elif trial == 'yy':
            data = [df['ET22'][:index], pred['S22'][:index], df['S22'][:index]]
        elif trial == 'xy':
            data = [df['ET12'][:index], pred['S12'][:index], df['S12'][:index]]

        save_graphs(legend, 1, data, labels, workd_gra + 'comp_s_'
        + str(Emax) + '_ET_S_' + trial + '_2d', 2)


        if trial == 'xx':
            data = [df['ET11'][:index2], pred['S11'][:index2], df['S11'][:index2]]
        elif trial == 'yy':
            data = [df['ET22'][:index2], pred['S22'][:index2], df['S22'][:index2]]
        elif trial == 'xy':
            data = [df['ET12'][:index2], pred['S12'][:index2], df['S12'][:index2]]

        save_graphs(legend, 1, data, labels, workd_gra + 'comp_sts_'
        + str(Emax) + '_ET_S_' + trial + '_2d', 2)

        # Close all figures
        plt.close('all')

print ('Done creating graphs')
