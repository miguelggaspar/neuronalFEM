import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV
import numpy as np
import itertools

df = pd.read_csv("../dataset/data.csv")

# Choose features
X = df.drop(["dIStrain", "dX", "dR", "Time", "TStrain", "EStrain"], axis=1)
# Choose targets
y = df.drop(["IStrain", "TStrain", "X", "R", "Time", "Stress", "EStrain"], axis=1)

scaler_x = preprocessing.StandardScaler()
scaler_y = preprocessing.StandardScaler()

scaler_x.fit(X)
scaler_y.fit(y)

# Split Dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3,
                                                    random_state=42)
X_train = scaler_x.transform(X_train)
X_test = scaler_x.transform(X_test)
y_train = scaler_y.transform(y_train)
y_test = scaler_y.transform(y_test)

# Store hidden layer sizs and neurons for gridsearch
hidden_sizes = [x for x in itertools.product(np.linspace(1, 20, 5, dtype=int),
                                             repeat=2)]
hidden_sizes.extend(np.linspace(1, 20, 5, dtype=int))
hidden_size_2 = [x for x in itertools.product(np.linspace(1, 20, 5, dtype=int),
                                              repeat=3)]
hidden_sizes.extend(hidden_size_2)

gs = GridSearchCV(MLPRegressor(), param_grid={
    'hidden_layer_sizes': hidden_sizes,
    'activation': ['logistic', 'tanh', 'relu'],
    'solver': ["lbfgs", "sgd", "adam"],
    'learning_rate': ['constant', 'invscaling', 'adaptive'],
    'alpha': [np.logspace(-5, 3, 5).all()]})

gs.fit(X_train, y_train)
#
# print("Best: %f using %s" % (gs.best_score_, gs.best_params_))
# means = gs.cv_results_['mean_test_score']
# stds = gs.cv_results_['std_test_score']
# params = gs.cv_results_['params']
# for mean, stdev, param in zip(means, stds, params):
#     print("%f (%f) with: %r" % (mean, stdev, param))

# Save gridsearch for further read
joblib.dump(gs, 'gs.pkl')
joblib.dump(scaler_x, 'scaler_x.pkl')
joblib.dump(scaler_y, 'scaler_y.pkl')
