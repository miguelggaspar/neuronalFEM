from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import learning_curve
from sklearn.model_selection import validation_curve
from sklearn.utils import shuffle

def get_data(wokdir, name):
    #Load whole dataset
    df = pd.read_csv(workdir + "../dataset/results/data_" + name + ".csv")
    # Chose features
    X = df.drop(["ET11", "ET22", "ET12", "dEi11", "dEi22", "dEi12", "Ee11", "Ee22",
                 "Ee12", "dX11", "dX12", "dX22", "dpStrain", "dR",
                 "Time"], axis=1)
    # Chose targets
    y = df.drop(["ET11", "ET22", "ET12", "Ei11", "Ei22", "Ei12", "Time",  "Ee11",
                 "Ee22",  "Ee12", "X11", "X22", "X12", "pStrain", "R", "S11",
                 "S22", "S12"], axis=1)
    return X, y


def pre_process(X, y):
    scaler_x = preprocessing.StandardScaler()
    scaler_y = preprocessing.StandardScaler()
    scaler_x.fit(X)
    scaler_y.fit(y)
    X = scaler_x.transform(X)
    y = scaler_y.transform(y)
    return X, y

def get_hidden_nodes(nsamples, Ni, No):
    alphas = [2,4,6,8,10]
    hidden_nodes = []
    for alpha in alphas:
        hidden_nodes.append(int(np.floor(nsamples/(alpha*(Ni+No)))))
    return hidden_nodes

def plot_learning_curve(estimator, X, y, cv):
    train_sizes, train_scores, test_scores = learning_curve(estimator,
                                                            X, y, cv=cv)
    plt.figure()
    title = "Learning Curve"
    plt.title(title)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_scores_mean = 1 - np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = 1 - np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Validation score")
    plt.legend(loc="best")
    plt.show()

def plot_validation_curve(estimator, X, y, cv, hidden_sizes, n, params):
    train_color = ['darkorange', 'k', 'salmon', 'palegreen']
    valid_color = ['navy', 'y', 'orange', 'orchid']

    train_scores, valid_scores = validation_curve(estimator, X, y,
                                                  "hidden_layer_sizes",
                                                  hidden_sizes, cv=cv)
    # param_range = np.linspace(1,len(hidden_sizes), len(hidden_sizes))
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    valid_scores_mean = np.mean(valid_scores, axis=1)
    valid_scores_std = np.std(valid_scores, axis=1)

    plt.title("Validation Curve with MLPRegressor \n Solver = " + params[0] + "\nActivation = " + params[1])
    plt.xlabel("Number of Hidden Neurons")
    plt.ylabel("Score")
    lw = 2
    # plt.ylim(0.7, 1)
    plt.plot(hidden_sizes, train_scores_mean,
                label="Training score" ,
                color=train_color[n], lw=lw)
    plt.fill_between(hidden_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.2,
                     color=train_color[n], lw=lw)

    plt.plot(hidden_sizes, valid_scores_mean,
                label="Cross-validation score",
                color=valid_color[n], lw=lw)
    plt.fill_between(hidden_sizes, valid_scores_mean - valid_scores_std,
                     valid_scores_mean + valid_scores_std, alpha=0.2,
                     color=valid_color[n], lw=lw)
    # plt.grid()
    plt.legend(loc=4)

    return plt

if __name__ == "__main__":
    "Starting Manual Search"
    workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/train/'
    # Get features and targets
    X, y = get_data(workdir, '1000_3')
    # solvers = ['lbfgs', 'adam']
    # activations = ['tanh', 'relu', 'logistic']
    solvers = ['lbfgs']
    activations = ['relu']

    nsample = 1000
    nsamples = nsample * 3 * 3
    # nsamples = 42007s
    # Pre Process features and targets
    X_train, y_train = pre_process(X, y)
    # Shuffle the data
    X_shuf, y_shuf = shuffle(X_train, y_train)

    # hidden_nodes = [1,2,3,4,5,9]#,10,11,12,13,14,15,16,17,18,22,47,59,78]
    # hidden_nodes.extend(list(reversed(get_hidden_nodes(nsamples, 11, 8))))
    # # hidden_nodes.extend([80, 250, 300])
    # list.sort(hidden_nodes)
    # hidden_nodess = [(31,42,9), (31,42,25), (31,42,31) , (31,42,42), (3142,63), (31,42,126)]
    # hidden_nodess = [(15,1), (15,2), (15,3) , (15,4), (15,5), (15,9), (15,22)]
    # exit()
    # hidden_nodes = [1,2,3,4,5,9,] #,10,11,12,13,14,15,16,17,18,22,47,59,78]
    hidden_nodes = list(np.linspace(9,20,12, dtype=int))

    for solver in solvers:
        n = 0
        for activation in activations:
            params = [solver, activation]
            estimator = MLPRegressor(solver=solver, activation=activation,
                                     random_state=1, verbose=True)
            plt = plot_validation_curve(estimator, X_shuf, y_shuf, 5, hidden_nodes,
                                        n, params)

            plt.grid()
            # plt.show()
            #
            plt.savefig(workdir + 'graphs/' + solver + '/' + str(nsample) + '_' + activation + '.png',
                           bbox_inches='tight')
            plt.show()
            plt.close()
    # estimator = MLPRegressor(solver='lbfgs', activation='relu',
    #                                  learning_rate='constant',
    #                                  random_state=1, verbose=True)

    # learning_curve(estimator, X_shuf,y_shuf, 10)

    # plot_learning_curve(estimator, X, y, 5)
