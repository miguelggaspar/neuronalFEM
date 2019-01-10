import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV
import numpy as np
import itertools

df = pd.read_csv("../dataset/data_036.csv")

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

X = scaler_x.transform(X)
y = scaler_y.transform(y)


# Store hidden layer sizs and neurons for gridsearch
# hidden_sizes = [x for x in itertools.product(np.linspace(1, 20, 5, dtype=int),
#                                              repeat=2)]
# hidden_sizes.extend(np.linspace(1, 20, 5, dtype=int))
# hidden_size_2 = [x for x in itertools.product(np.linspace(1, 20, 5, dtype=int),
#                                               repeat=3)]
# hidden_sizes.extend(hidden_size_2)

X_shuf, y_shuf = shuffle(X, y)



# relu lbfgs (invscaling, constant, adaptive) [(2), (3), (4)]
# hidden_nodes = [1,2,3,4,5,9,13,18,20]#,10,11,12,13,14,15,16,17,18,22,47,59,78]
# hidden_nodes = [2,4,7,10]#,10,11,12,13,14,15,16,17,18,22,47,59,78]
hidden_nodes = [4]#,10,11,12,13,14,15,16,17,18,22,47,59,78]



gs = GridSearchCV(MLPRegressor(max_iter=400), param_grid={
    'hidden_layer_sizes': hidden_nodes,
    'activation': ['relu'],
    'solver': ["lbfgs"],
    'learning_rate': ['constant','invscaling','adaptive'],
    'alpha': [1]}, cv=5)

gs.fit(X_shuf, y_shuf)
#
# print("Best: %f using %s" % (gs.best_score_, gs.best_params_))
# means = gs.cv_results_['mean_test_score']
# stds = gs.cv_results_['std_test_score']
# params = gs.cv_results_['params']
# for mean, stdev, param in zip(means, stds, params):
#     print("%f (%f) with: %r" % (mean, stdev, param))

# Save gridsearch for further read
joblib.dump(gs, 'gridsearch/gs.pkl')
joblib.dump(scaler_x, 'gridsearch/scaler_x.pkl')
joblib.dump(scaler_y, 'gridsearch/scaler_y.pkl')
