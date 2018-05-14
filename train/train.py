import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
# from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV

MODEL_PATH = "../dataset/"


def load_model_data(model_path=MODEL_PATH):
    csv_path = os.path.join(model_path, "data.csv")
    return pd.read_csv(csv_path)


rawData = load_model_data()

X = rawData.drop(["dIStrain", "dX", "dR", "Time"], axis=1)
y = rawData.drop(["IStrain", "TStrain", "X", "R", "Time", "Stress"], axis=1)

# Implements the Transformer API to compute the mean and standard deviation on a
# training set so as to be able to later reapply the same transformation on the
# testing set

# Split dataset with sklearn function
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.4)
if len(sys.argv) >= 2:
    if sys.argv[1] == "1":
        scaler = preprocessing.StandardScaler()
        # Don't cheat - fit only on training data
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        # apply same transformation to test data
        X_test = scaler.transform(X_test)

    elif sys.argv[1] == "2":    # Scaling features to a range
        min_max_scaler = preprocessing.MinMaxScaler()
        X_train_minmax = min_max_scaler.fit_transform(X_train)
        X_test_minmax = min_max_scaler.transform(X_test)
    elif sys.argv[1] == "3":
        X_normalized = preprocessing.normalize(X, norm='l2')
        X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=.4)
else:
    print ("Choose Pre-processing method")
    quit()


# This section is used for imputation of missing values TODO
# imputer = preprocessing.Imputer(missing_values='NaN', strategy='mean', axis=0)

# Simple neural_network definition
#
# clf = MLPRegressor(solver='lbfgs', alpha=1.0,
#                    hidden_layer_sizes=(5, 2), random_state=1)
#
# final_model = clf.fit(X_train, y_train)


# Grid Search Parameter Tuning
#
# prepare a range of alpha values to test
# alphas = np.array([1,0.1,0.01,0.001,0.0001,0])
# # create and fit a neural_network regression model, testing each alpha
# model = MLPRegressor()
# grid = GridSearchCV(estimator=model, param_grid=dict(alpha=alphas))
# grid.fit(X_train, y_train)
#
# print(grid)
# # summarize the results of the grid search
# print(grid.best_score_)
# print(grid.best_estimator_.alpha)

# Randomized Search for Algorithm Tuning
from scipy.stats import uniform as sp_rand
# prepare a uniform distribution to sample for the alpha parameter
param_grid = {'alpha': sp_rand()}
# create and fit a ridge regression model, testing random alpha values
model = MLPRegressor()
rsearch = RandomizedSearchCV(estimator=model, param_distributions=param_grid, n_iter=100)
rsearch.fit(X_train, y_train)
print(rsearch)
# summarize the results of the random parameter search
print(rsearch.best_score_)
print(rsearch.best_estimator_.alpha)

# Some input values to test
# p = scaler.transform([[0.00016, 0.04893, 3.78436, 0.01909, 0.80891]])
# a = final_model.predict(p)
# # a = final_model.predict([[0.00016, 0.04893, 3.78436, 0.01909, 0.80891]])
# print (a[0][0])
# print (a[0][1])
# print (a[0][2])

# Save final model to deploy
# joblib.dump(final_model, 'mlmodel.pkl')
joblib.dump(rsearch, 'mlmodel.pkl')
joblib.dump(scaler, 'scaler.pkl')

# For further use, use this line to import trained model
# clf = joblib.load('mlmodel.pkl')
