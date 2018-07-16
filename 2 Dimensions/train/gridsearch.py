import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV
import numpy as np
import itertools
df = pd.read_csv("../dataset/results/data.csv")

# Choose features
X = df.drop(["ET11", "ET22", "ET12", "dEi11", "dEi22", "dEi12", "Ee11", "Ee22",
             "Ee12", "dX11", "dX12", "dX22", "dpStrain", "dR",
             "Time"], axis=1)
# Choose targets
y = df.drop(["ET11", "ET22", "ET12", "Ei11", "Ei22", "Ei12", "Time",  "Ee11",
             "Ee22",  "Ee12", "X11", "X22", "X12", "pStrain", "R", "S11",
             "S22", "S12"], axis=1)

# Implements the Transformer API to compute the mean and standard deviation on a
# training set so as to be able to later reapply the same transformation on the
# testing set
scaler_x = preprocessing.StandardScaler()
scaler_y = preprocessing.StandardScaler()
# Don't cheat - fit only on training data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3,
                                                    random_state=42)
scaler_x.fit(X)
scaler_y.fit(y)

X_train = scaler_x.transform(X_train)
X_test = scaler_x.transform(X_test)
y_train = scaler_y.transform(y_train)
y_test = scaler_y.transform(y_test)

# Store hidden layer sizs and neurons for gridsearch
hidden_sizes = [x for x in itertools.product(np.linspace(4, 20, 5, dtype=int),
                                             repeat=2)]
hidden_sizes.extend(np.linspace(4, 20, 5, dtype=int))
hidden_size_2 = [x for x in itertools.product(np.linspace(4, 20, 5, dtype=int),
                                              repeat=3)]
hidden_sizes.extend(hidden_size_2)

gs = GridSearchCV(MLPRegressor(), param_grid={
    'hidden_layer_sizes': hidden_sizes,
    'activation': ['logistic', 'tanh', 'relu'],
    'solver': ["lbfgs", "sgd", "adam"],
    'learning_rate': ['constant', 'invscaling', 'adaptive'],
    'alpha': [np.logspace(-5, 3, 5).all()]})
gs.fit(X_train, y_train)

print("Best: %f using %s" % (gs.best_score_, gs.best_params_))
means = gs.cv_results_['mean_test_score']
stds = gs.cv_results_['std_test_score']
params = gs.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))

# Save gridsearch for further read
joblib.dump(gs, 'gs.pkl')
joblib.dump(scaler_x, 'scaler_x.pkl')
joblib.dump(scaler_y, 'scaler_y.pkl')
