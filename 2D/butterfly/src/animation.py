import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from utils import get_data, rename_headers, get_dataframe
import matplotlib.animation as animation
import matplotlib
import seaborn as sns

# 1f77b4
# ff7f0e
# 2ca02c
# d62728
# 9467bd
# 8c564b

def animate(i):
    ann = fea.iloc[:int(i+1)] #select data range
    exp = chaboche.iloc[:int(i+1)] #select data range

    p = sns.lineplot(x=exp['ET12'], y=exp['S12'], data=exp, color='b')
    p = sns.lineplot(x=ann['ET12'], y=ann['S12'], data=ann, color='r',marker='.')

    # p = sns.lineplot(x=exp['Time'], y=exp['X11'], data=exp, color='#1f77b4')
    # p = sns.lineplot(x=ann['t'], y=ann['X11'], data=ann, color='#ff7f0e',marker='.')
    # p = sns.lineplot(x=exp['Time'], y=exp['X11'], data=exp, color='#1f77b4')
    #
    # p = sns.lineplot(x=ann['t'], y=ann['X22'], data=ann, color='#d62728', marker='.')
    # p = sns.lineplot(x=exp['Time'], y=exp['X22'], data=exp, color='#2ca02c')
    #
    # p = sns.lineplot(x=ann['t'], y=ann['X12'], data=ann, color='#8c564b', marker='.')
    # p = sns.lineplot(x=exp['Time'], y=exp['X12'], data=exp, color='#9467bd')
    p.tick_params(labelsize=7)
    plt.setp(p.lines,linewidth=3)

# Driver program
if __name__ == "__main__":
    workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/butterfly/'
    abaqus_dir = '/home/miguel/Documents/tese/ViscoPlastic-ML/abaqus_deploy/butterfly/'
    workvid = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/butterfly/videos/'
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
        chaboche = chaboche.drop(chaboche.index[len(chaboche)-1])
        abaqus = rename_headers(abaqus)

        # Select from abaqus dataframe info about el_num and int_point
        fea = get_dataframe(abaqus, el_num[n], 2)
        exit()
        # remove repeated values
        # Plot and save graphs of Back stress
        title = 'Back Stress'
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=2, metadata=dict(artist='Me'), bitrate=-1)
        fig = plt.figure(figsize=(10,6))
        plt.xlim(0, 0.05)
        plt.ylim(0, 75)
        ani = matplotlib.animation.FuncAnimation(fig, animate, frames=24, repeat=True)
        ani.save(workvid + 'S12.mp4', writer=writer)
        plt.close()
        break
