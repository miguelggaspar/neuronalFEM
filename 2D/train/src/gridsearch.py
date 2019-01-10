from sklearn.utils import shuffle
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV
import numpy as np
from utils import get_data


workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/train/'

X, y = get_data(workdir, 'training_data')
# Implements the Transformer API to compute the mean and standard deviation on a
# training set so as to be able to later reapply the same transformation on the
# testing set
scaler_x = preprocessing.StandardScaler()
scaler_y = preprocessing.StandardScaler()
# Don't cheat - fit only on training data

scaler_x.fit(X)
scaler_y.fit(y)

# Transform Dataset
X = scaler_x.transform(X)
y = scaler_y.transform(y)

# shuffle Dataset
X_shuf, y_shuf = shuffle(X, y)

hidden_nodes = [4, 10, 16, 22]
gs = GridSearchCV(MLPRegressor(), param_grid={
    'hidden_layer_sizes': hidden_nodes,
    'activation': ['logistic', 'tanh', 'relu'],
    'solver': ["lbfgs", "sgd", "adam"],
    'learning_rate': ['constant']}, cv=5)

gs.fit(X_shuf, y_shuf)

print("Best: %f using %s" % (gs.best_score_, gs.best_params_))
means = gs.cv_results_['mean_test_score']
stds = gs.cv_results_['std_test_score']
params = gs.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))

# Save gridsearch for further read
joblib.dump(gs, '../gridsearch_results/gs.pkl')
joblib.dump(scaler_x, '../gridsearch_results/scaler_x.pkl')
joblib.dump(scaler_y, '../gridsearch_results/scaler_y.pkl')
