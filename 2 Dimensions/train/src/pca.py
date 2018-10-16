from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

# For further use, use this line to import trained model
# gs = joblib.load('gs.pkl')

df = pd.read_csv("../../dataset/results/data_16000_3.csv")

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
X = scaler_x.transform(X)
y = scaler_y.transform(y)

# Split Dataset into training and test sets

# Transform data to training and testing
X_train = scaler_x.transform(X_train)
X_test = scaler_x.transform(X_test)
y_train = scaler_y.transform(y_train)
y_test = scaler_y.transform(y_test)

# estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(15,15,15),
#                          alpha=0.01, random_state=1, learning_rate='constant')


# estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(5,4,5),
#                          alpha=0.01, random_state=1, learning_rate='constant',
#                          learning_rate_init=3e-5)

estimator = MLPRegressor(solver='adam', hidden_layer_sizes=(10,10),
                         activation='relu', learning_rate='constant',
                         alpha=0.01, random_state=1, verbose=True)
pca = PCA()
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)
estimator.fit(X_train, y_train)

# Predicting the Test set results
y_pred = estimator.predict(X_test)
X_train = pca.fit_transform(X_train)


print(cm)
print('Accuracy' + accuracy_score(y_test, y_pred))
