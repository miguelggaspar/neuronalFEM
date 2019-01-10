from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import learning_curve
from sklearn.model_selection import validation_curve
from sklearn.utils import shuffle


def get_data(wokdir, name):
    # Load Dataset for trainig
    df = pd.read_csv("../dataset/data_036.csv")
    # Choose features
    X = df.drop(["dIStrain", "dX", "dR", "Time", "TStrain", "EStrain"], axis=1)
    # Choose targets
    y = df.drop(["IStrain", "TStrain", "X", "R", "Time", "Stress", "EStrain"], axis=1)
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
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
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
    plt.ylim([0,1.1])
    plt.legend(loc="best")
    plt.show()
    return plt, train_scores_mean, test_scores_mean, train_scores_std, test_scores_std

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

    # plt.title("Validation Curve")
    plt.xlabel("Number of Hidden Neurons")
    plt.ylabel(r"$R^2$")
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
    plt.legend(loc=2)

    return plt, train_scores_mean, valid_scores_mean

if __name__ == "__main__":
    "Starting Manual Search"
    workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/1 Dimension/train/graphs/'
    # Get features and targets
    X, y = get_data(workdir, '1000_3')
    solvers = ['lbfgs']
    activations = ['relu']
    l_rates = ['constant']

    nsample = 3000
    nsamples = nsample
    # Pre Process features and targets
    X_train, y_train = pre_process(X, y)
    # Shuffle the data
    X_shuf, y_shuf = shuffle(X_train, y_train)

    hidden_nodes = [1,2,3,4,5,9,13,18,20]
    ind = np.arange(len(hidden_nodes))

    for solver in solvers:
        n = 0
        for activation in activations:
            params = [solver, activations[0]]
            estimator = MLPRegressor(solver=solver, activation=activation,
                                     random_state=1, alpha=1, learning_rate='constant')
            plt, train_scores_mean, valid_scores_mean = plot_validation_curve(estimator, X_shuf, y_shuf, 5, hidden_nodes,
                                                                              n, params)

            # plt.show()
            #
            plt.xlim([0, 20])
            plt.legend(loc=4)
            plt.xticks(hidden_nodes)
            plt.grid()
            plt.savefig(workdir + solver + '_' + activation + '.png', bbox_inches='tight')


            # plt.show()
            plt.close()

    # estimator = MLPRegressor(solver='lbfgs', activation='relu',
    #                          hidden_layer_sizes=(3,), learning_rate='adaptive',
    #                          random_state=1, alpha=0.1)

    # learning_curve(estimator, X_shuf,y_shuf, 10)

    # plt, train_scores_mean, test_scores_mean, train_scores_std, test_scores_std = plot_learning_curve(estimator, X, y, 5)
