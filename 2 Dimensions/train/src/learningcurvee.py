from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit
from sklearn.utils import shuffle

# For further use, use this line to import trained model
# gs = joblib.load('gs.pkl')
workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/train/'
data = 'data_800_3'
df = pd.read_csv("../../dataset/results/" + data + ".csv")

# Choose features
X = df.drop(["ET11", "ET22", "ET12", "dEi11", "dEi22", "dEi12", "Ee11", "Ee22",
             "Ee12", "dX11", "dX12", "dX22", "dpStrain", "dR",
             "Time"], axis=1)

# Choose targets
y = df.drop(["ET11", "ET22", "ET12", "Ei11", "Ei22", "Ei12", "Time",  "Ee11",
             "Ee22",  "Ee12", "X11", "X22", "X12", "pStrain", "R", "S11",
             "S22", "S12"], axis=1)

scaler_x = preprocessing.StandardScaler()
scaler_y = preprocessing.StandardScaler()

scaler_x.fit(X)
scaler_y.fit(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3,
                                                    random_state=42)

X_train = scaler_x.transform(X_train)
X_test = scaler_x.transform(X_test)
y_train = scaler_y.transform(y_train)
y_test = scaler_y.transform(y_test)

X = scaler_x.transform(X)
y = scaler_y.transform(y)
X_shuf, y_shuf = shuffle(X, y)


#
# estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(15,15,15),
#                          alpha=0.01, random_state=1, learning_rate='constant')


# estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(5,4,5),
#                          alpha=0.01, random_state=1, learning_rate='constant',
#                          learning_rate_init=3e-5)

estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(14),
                         activation='relu',max_iter=400,
                         random_state=1, verbose=True)
# estimator = MLPRegressor(solver='adam', hidden_layer_sizes=(30, 20, 30),
#                          activation='relu', learning_rate='constant',
#                          alpha=1, random_state=1)
# Cross validation with 100 iterations to get smoother mean test and train
# score curves, each time with 20% data randomly selected as a validation set.

train_sizes, train_scores, test_scores = learning_curve(estimator, X_shuf, y_shuf, cv=5)

plt.figure()
title = "Learning Curve"
plt.title(title)

plt.xlabel("Training examples")
plt.ylabel("Score")
# train_sizes, train_scores, test_scores = learning_curve(estimator, X, y, cv=5, scoring='neg_median_absolute_error')
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

plt.savefig(workdir + 'graphs/'+ estimator.solver +'/LC' + data + '.png', bbox_inches='tight')
plt.show()
# plt.savefig('learning_curve_2d', bbox_inches='tight')
