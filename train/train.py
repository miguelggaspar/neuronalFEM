import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier


import numpy as np
import hashlib

MODEL_PATH = "../viscoplasticModels/"


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
        scaler = preprocessing.StandardScaler().fit(X_train)
        X_train = scaler.transform(X_train)
        X_tests = scaler.transform(X_test)
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
y1 = y_train.as_matrix()


#
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 2), random_state=1)

clf.fit(X_train, y1)
