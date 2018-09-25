import pandas as pd
import matplotlib.pyplot as plt
from compare_utils import get_score, save_scores
import sys

print ('Creating and saving graphs for the tested model')
workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/testmodel/'
workd_gra = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/testmodel/graphs/'
workdir_ann = '../train/model/'

trials = ['xx', 'yy', 'xy']
Emaxs = []
for k in range(len(sys.argv)):
    if (len(sys.argv) - k) == 1:
        break
    Emaxs.append(float(sys.argv[k+1]))

for Emax in Emaxs:
    for trial in trials:
        print ('Trial: ', trial, 'Emax: ', Emax)
        df = pd.read_csv(workdir + "../dataset/results/data_" + str(Emax) + "_" + trial + ".csv")
        pred = pd.read_csv(workdir + "results/predictions_" + str(Emax) + "_" + trial + "_2d.csv")

        # Close all figures
        plt.close('all')

        score = get_score(workdir_ann, df)
        save_scores(trial, score, Emax, pd, workdir)


print ('Done creating graphs')
