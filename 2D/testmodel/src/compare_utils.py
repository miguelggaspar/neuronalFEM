import matplotlib.pyplot as plt
from sklearn.externals import joblib
import numpy as np

# Plot Total, Elastic and Inelastic Strains
def save_graphs(legends, n_hand, data, labels, name, condition):
    # plt.figure(figsize=(8, 5), dpi=80)
    # plt.style.use(style)
    # plt.ylim(-0.075, 0.075)                         # set the xlim to xmin, xmax
    color = ['r', 'b', 'r', 'b', 'r', 'b']
    fig, ax = plt.subplots(3, 1, sharex=True, sharey=True)
    fig.text(0.51, 0.035, labels[0], ha='center')
    fig.text(0.02, 0.5, labels[1], va='center', rotation='vertical')
    for n in range(n_hand):
        plt.subplot(n_hand, 1, n+1)
        if condition == 0:
            plt.plot(data[0], data[2*n+1], label=legends[2*n], color=color[2*n])
            plt.plot(data[0], data[2*n+2], label=legends[2*n+1], color=color[2*n+1])
            plt.grid()
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            fig.suptitle(labels[2], fontsize=13, x=0.5, y=0.93)
        elif condition == 1:
            plt.plot(data[0], data[n+1], label=legends[n], color=color[n])
            plt.grid()
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            fig.suptitle(labels[2], fontsize=13, x=0.5, y=0.93)
        elif condition == 2:
            plt.plot(data[3*n], data[3*n+1], label=legends[2*n], color=color[2*n])
            plt.plot(data[3*n], data[3*n+2], label=legends[2*n+1], color=color[2*n+1])
            plt.grid()
            # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            plt.legend(loc=2)
            print("lol")
        plt.savefig(name + '.png', bbox_inches='tight')


def get_score(workdir_ann, df, pred,name):
    # Load trained model for further prediction and scalers to transform the data.
    ann = joblib.load(workdir_ann + 'mlmodel.pkl')
    scaler_x = joblib.load(workdir_ann + 'scaler_x.pkl')
    scaler_y = joblib.load(workdir_ann + 'scaler_y.pkl')

    # Choose features
    X = df.drop(["ET11", "ET22", "ET12", "dEi11", "dEi22", "dEi12", "Ee11",
                 "Ee22", "Ee12", "dX11", "dX12", "dX22", "dpStrain", "dR",
                 "Time"], axis=1)
    # Choose targets
    y = pred.drop(["ET11", "ET22", "ET12", "Ei11", "Ei22", "Ei12", "Time",
                 "X11", "X22", "X12", "pStrain", "R", "S11",
                 "S22", "S12"], axis=1)
    X = scaler_x.transform(X)
    y = scaler_y.transform(y)
    return (ann.score(X, y))


def save_scores(trial, score, Emax, pd, workdir):
    # df = pd.DataFrame({'Trial': [trial], 'Emax': [Emax], 'Score': [score]})
    df = pd.DataFrame({'Score': [score]})
    df.to_csv(workdir + "for_writing.csv",
               float_format='%.2f', index=False, mode='a', header=False)


def get_index(value, start, stop, num_el):
    index = int(np.floor((value-start)*(num_el-1)/(stop-start)+1))
    return index
