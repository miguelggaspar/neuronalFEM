import pandas as pd
import matplotlib.pyplot as plt
import sys
from mpl_toolkits.mplot3d import Axes3D

print ('Creating and saving graphs for the tested model')
workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/testmodel/'
workd_gra = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/testmodel/graphs/'
trials = ['xx', 'yy', 'xy']
style = 'ggplot'


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

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(pred['ET11'], pred['ET22'], pred['S11'], label='parametric curve')
        ax.legend()
        plt.show()
