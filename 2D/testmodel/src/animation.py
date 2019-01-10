import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from compare_utils import save_graphs, get_score, save_scores
import sys
import seaborn as sns
import matplotlib

def resize(dff, factor):
    for i in range(0, factor):
        dff= dff.iloc[::2]
        dff.index = range(len(dff))
    return dff



def animate(i,full):
    dats = full.iloc[:int(i+1)] #select data range

    # Stress
    # p = sns.lineplot(x='ET', y='pred_S', data=dats, color='r', sort=False)
    # p = sns.lineplot(x='ET', y='S', data=dats, color='b', sort=False)

    # Total Strain
    #
    p = sns.lineplot(x='Time', y='ET11', data=dats, color='tab:blue', sort=False)
    p = sns.lineplot(x='Time', y='ET22', data=dats, color='tab:orange', sort=False)
    p = sns.lineplot(x='Time', y='ET12', data=dats, color='tab:green', sort=False)

    p.tick_params(labelsize=7)
    plt.setp(p.lines,linewidth=3)



workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/testmodel/'
workd_vid = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/testmodel/animations/'

trials = ['xx', 'yy', 'xy']
Emax = 0.18


S = ['S11', 'S22', 'S12']
ET = ['ET11', 'ET22', 'ET12']

# yranges = [[-800, 800], [-0.2, 0.2]]
# xranges = [[-0.2, 0.2], [0, 80]]

# trial = 'xx'
n = 0
for trial in trials:
    print ('trial -> ', trial)
    df = pd.read_csv(workdir + "../dataset/results/data_" + str(Emax) + "_" + trial + ".csv")
    pred = pd.read_csv(workdir + "results/predictions_" + str(Emax) + "_" + trial + "_2d.csv")

    df = resize(df, 3)
    pred = resize(pred, 3)


    # Stress
    # full = pd.DataFrame({"ET": df[ET[n]].values, "S": df[S[n]].values,
    #                      "pred_S": pred[S[n]].values})
    #
    # Frames = 3124
    # fps = 312
    # resize = 3

    # full = pd.DataFrame({"t": df['Time'].values, "ET11": df[ET11].values})

    #Strains
    # full = pd.DataFrame({"ET11": df['ET11'].values, "ET12": df['ET12'].values,
    #                      "ET22": df['ET22'].values, "t": df['Time'].values})
    #
    #

    title = 'Back Stress'
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=312, metadata=dict(artist='Me'), bitrate=-1)
    fig = plt.figure(figsize=(10,6))
    # plt.xlim(-0.18, 0.18)
    # if trial == 'xy':
        # plt.ylim(-350, 350)
    # else:
        # plt.ylim(-800, 800)
    plt.xlim(0, 80)
    plt.ylim(-0.2, 0.2)
    # plt.xlim(0, 80)
    # plt.ylim(-110, 110)
    # plt.xlabel('Time',fontsize=20)
    # plt.ylabel('Stress',fontsize=20)
    # plt.title('viscoplastic evolution',fontsize=20)
    ani = matplotlib.animation.FuncAnimation(fig, animate, fargs=(df,), frames=3124)
    # ani.save(workd_vid + S[n] + '_' + ET[n] + '.mp4', writer=writer)
    ani.save(workd_vid + ET[n] + '.mp4', writer=writer)
    plt.close()
    n += 1
