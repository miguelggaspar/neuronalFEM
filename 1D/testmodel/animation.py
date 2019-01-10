import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import matplotlib.animation as animation
import matplotlib
import seaborn as sns
import time

def animate(i, df, pred, exp_name, ann_name):
    exp = df.iloc[:int(i+1)] #select data range
    # ann = pred.iloc[:int(i+1)] #select data range
    p = sns.lineplot(x=exp['Time'], y=exp[exp_name], data=exp, color='b')
    # p = sns.lineplot(x=ann['Time'], y=ann[ann_name], data=ann, color='r')

    p.tick_params(labelsize=7)
    plt.setp(p.lines,linewidth=3)

# Driver program
if __name__ == "__main__":

    pred = pd.read_csv("pred_025.csv")
    df = pd.read_csv("../dataset/data_025.csv")

    names = ['S_1d', 'X_1d', 'dX_1d', 'R_1d', 'dR_1d', 'Evp_1d', 'dEvp_1d', 'ET_1d']
    yranges= [[-100,100], [-35,35], [-15,15], [47,75], [-0.05,0.9],
              [-0.008,0.01], [-0.004,0.004], [-0.03, 0.03]]

    exp_name = ['Stress', 'X', 'dX', 'R', 'dR', 'IStrain', 'dIStrain', 'TStrain']
    ann_name = ['S', 'X', 'dX', 'R', 'dR', 'EI', 'dEI', 'ET']
    
    # exit()
    # yrange = [-100,100]  # S
    # yrange = [-35,35]  # X
    # yrange = [-15,15]  # dX
    # yrange = [47,75]  # R
    # yrange = [-0.05,0.9]  # dR
    # yrange = [-0.008,0.01]  # Evp
    # yrange = [-0.004,0.004]  # dEvp
    # yrange = [-0.03,0.03]  # ET
    # title = 'Back Stress'
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=300, metadata=dict(artist='Me'), bitrate=-1)
    #old (5 fps, 150 frames)
    for n in range(7,8):
        start_time = time.time()
        print('Making video for -> ', names[n])
        fig = plt.figure(figsize=(10,6))
        plt.xlim(0, 80)
        plt.ylim(yranges[n])
        plt.xlabel('Time',fontsize=20)
        # plt.ylabel('Stress',fontsize=20)
        # plt.title(' evolution',fontsize=20)
        ani = matplotlib.animation.FuncAnimation(fig, animate, frames=3000,
                            fargs=(df,pred, exp_name[n], ann_name[n]), repeat=True)
        ani.save('animations/' + names[n] + '.mp4', writer=writer)
        plt.close()
        print("--- %s seconds ---" % (time.time() - start_time))
