from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import validation_curve
import pandas as pd
from matplotlib import pyplot as plt
import pickle
import json
import sys
import numpy as np
from sklearn.utils import shuffle

workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/train/'
# Load Dataset for trainig
df = pd.read_csv(workdir + "../dataset/results/data_1000_3.csv")

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

# Fit the scaler to transform features and targets
scaler_x.fit(X)
scaler_y.fit(y)


# Split Dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3,
                                                    random_state=42)

# Transform data to training and testing
X_train = scaler_x.transform(X_train)
X_test = scaler_x.transform(X_test)
y_train = scaler_y.transform(y_train)
y_test = scaler_y.transform(y_test)

X = scaler_x.transform(X)
y = scaler_y.transform(y)

X_shuf, y_shuf = shuffle(X, y)


# last:
# relu, adaptive, (7,7), lbfgs, alpha 1
# estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(5,4),
#                          activation='relu', learning_rate='adaptive',
#                          random_state=1)
# # #
# estimator = MLPRegressor(solver='adam', hidden_layer_sizes=(13),
#                          activation='relu', learning_rate='constant',
#                          random_state=1, verbose=True)


estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(15),
                         activation='relu',
                         random_state=1)

# estimator = MLPRegressor(solver='sgd', hidden_layer_sizes=(20, 20, 20),
#                          activation='relu', learning_rate='constant',
#                          alpha=1, random_state=1)

# estimator.fit(X, y)
train_scores, valid_scores = validation_curve(estimator, X_shuf, y_shuf, "alpha",
                                              np.logspace(-7, 3, 10),
                                              cv=5)
param_range = np.logspace(-7,3,10)
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
valid_scores_mean = np.mean(valid_scores, axis=1)
valid_scores_std = np.std(valid_scores, axis=1)

plt.title("Validation Curve with MLPRegressor")
plt.xlabel("$\gamma$")
plt.ylabel("Score")
# plt.ylim(0.0, 1.1)
lw = 2
plt.semilogx(param_range, train_scores_mean, label="Training score",
             color="darkorange", lw=lw)
plt.fill_between(param_range, train_scores_mean - train_scores_std,
                 train_scores_mean + train_scores_std, alpha=0.2,
                 color="darkorange", lw=lw)
plt.semilogx(param_range, valid_scores_mean, label="Cross-validation score",
             color="navy", lw=lw)
plt.fill_between(param_range, valid_scores_mean - valid_scores_std,
                 valid_scores_mean + valid_scores_std, alpha=0.2,
                 color="navy", lw=lw)
plt.grid()
plt.legend(loc="best")
plt.show()
#
