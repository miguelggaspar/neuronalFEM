import pandas as pd
import matplotlib.pyplot as plt
from compare_utils import get_index
import sys

print ('Creating and saving graphs for the tested model')
workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/testmodel/'
workd_gra = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/testmodel/graphs/'
trials = ['xx', 'yy', 'xy']
style = 'ggplot'

def get_values(idx, col, dataframe):
    print ( col, "  ->  ",dataframe.at[idx,col])


Emaxs = []
for k in range(len(sys.argv)):
    if (len(sys.argv) - k) == 3:
        break
    Emaxs.append(float(sys.argv[k+3]))

idx = get_index(5, 0, int(sys.argv[2]), int(sys.argv[1]))
pd.options.display.float_format = '{:.2E}'.format
for Emax in Emaxs:
    for trial in trials:
        print ('Trial: ', trial, 'Emax: ', Emax)
        df = pd.read_csv(workdir + "../dataset/results/data_" + str(Emax) + "_" + trial + ".csv")
        pred = pd.read_csv(workdir + "results/predictions_" + str(Emax) + "_" + trial + "_2d.csv")
        # a = [df['S11'][idx], pred['S11'][idx], df['S22'][idx], pred['S22'][idx],
        #      df['S12'][idx], pred['S12'][idx], df['X11'][idx], pred['X11'][idx],
        #      df['X22'][idx], pred['X22'][idx], df['X12'][idx], pred['X12'][idx],
        #      df['Ei11'][idx], pred['Ei11'][idx], df['Ei22'][idx], pred['Ei22'][idx],
        #      df['Ei12'][idx], pred['Ei12'][idx], df['pStrain'][idx],
        #      pred['pStrain'][idx], df['R'][idx], pred['R'][idx]]
        a = [df['Ei11'][idx], pred['Ei11'][idx], df['Ei22'][idx], pred['Ei22'][idx],
             df['Ei12'][idx], pred['Ei12'][idx], df['pStrain'][idx],
             pred['pStrain'][idx]]

        dfs = pd.DataFrame({'LOL': a})
        #%.5f
        #%.2E
        dfs.to_csv(workdir + "table_" + str(Emax) + "_" + trial + ".csv",
           float_format='%.2E', index=False, mode='a', header=False)
print ('DONE')
