import matplotlib.pyplot as plt
from sklearn.externals import joblib


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
        if condition == 1:
            plt.plot(data[0], data[n+1], label=legends[n], color=color[n])
            plt.grid()
            # plt.legend(legends[n:], loc=0)
            # plt.legend(legends[n:])
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        else:
            plt.plot(data[0], data[2*n+1], label=legends[2*n], color=color[2*n])
            plt.plot(data[0], data[2*n+2], label=legends[2*n+1], color=color[2*n+1])
            plt.grid()
            # plt.legend(legends[2*n:2*n+2], loc=0)
            # plt.legend(legends[2*n:2*n+2])
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        plt.savefig(name + '.png', bbox_inches='tight')


def get_score(workdir_ann, df):
    # Load trained model for further prediction and scalers to transform the data.
    ann = joblib.load(workdir_ann + 'mlmodel.pkl')
    scaler_x = joblib.load(workdir_ann + 'scaler_x.pkl')
    scaler_y = joblib.load(workdir_ann + 'scaler_y.pkl')

    # Choose features
    X = df.drop(["ET11", "ET22", "ET12", "dEi11", "dEi22", "dEi12", "Ee11",
                 "Ee22", "Ee12", "dX11", "dX12", "dX22", "dpStrain", "dR",
                 "Time"], axis=1)
    # Choose targets
    y = df.drop(["ET11", "ET22", "ET12", "Ei11", "Ei22", "Ei12", "Time",  "Ee11",
                 "Ee22",  "Ee12", "X11", "X22", "X12", "pStrain", "R", "S11",
                 "S22", "S12"], axis=1)

    X = scaler_x.transform(X)
    y = scaler_y.transform(y)
    print (ann.score(X, y))
