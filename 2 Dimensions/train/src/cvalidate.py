from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import r2_score
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
import pandas as pd
from matplotlib import pyplot as plt
import pickle
import json
import sys

workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/train/'

# Load Dataset for trainig
df = pd.read_csv(workdir + "../dataset/results/data.csv")
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

# last:
# relu, adaptive, (7,7), lbfgs, alpha 1
# estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(4, 4, 12),
#                          activation='relu', learning_rate='adaptive',
#                          alpha=1, random_state=1)
#
estimator = MLPRegressor(solver='adam', hidden_layer_sizes=(30, 20, 30, 30),
                         activation='relu', learning_rate='constant',
                         alpha=1, random_state=1, verbose=True)

# estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(20, 12, 20),
#                          activation='tanh', learning_rate='constant',
#                          alpha=1, random_state=1)

# estimator = MLPRegressor(solver='sgd', hidden_layer_sizes=(20, 20, 20),
#                          activation='relu', learning_rate='constant',
#                          alpha=1, random_state=1)

# estimator.fit(X, y)
# predicted = cross_val_predict(estimator, X_train, y_train, cv=5)
# fig, ax = plt.subplots()
# ax.scatter(y_train, predicted, edgecolors=(0, 0, 0))
# ax.set_xlabel('Measured')
# ax.set_ylabel('Predicted')
# plt.show()
# ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
scores = cross_val_score(estimator, X, y, cv=5)
