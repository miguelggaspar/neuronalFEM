from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import numpy as np

def plot(data, name, legend):
    plt.plot(data)
    plt.xlabel('Training examples')
    plt.grid()
    plt.xlim([0,3000])
    # plt.legend(legend, fancybox=True, framealpha=0.5)
    plt.legend(legend,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig(name, bbox_inches='tight')
    plt.close()


# Load Dataset for trainig
df = pd.read_csv("../dataset/data.csv")
# Choose features
X = df.drop(["dIStrain", "dX", "dR", "Time", "TStrain", "EStrain"], axis=1)
# Choose targets
y = df.drop(["IStrain", "TStrain", "X", "R", "Time", "Stress", "EStrain"], axis=1)
# name
name = '/home/miguel/Documents/tese/ViscoPlastic-ML/1 Dimension/train/graphs/'

X_1 = X
y_1 = y
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

#Plot Features before StandardScaler
legend_X=[r'$\varepsilon^{vp}$', r'$R$', r'$\sigma$', r'$\chi$']
legend_y=[r'$\dot \varepsilon^{vp}$', r'$\dot R$', r'$\dot \chi$']

plot(X_1, name + 'X_before_1d', legend_X)
plot(y_1, name + 'y_before_1d', legend_y)
plot(X, name + 'X_after_1d', legend_X)
plot(y, name + 'y_after_1d', legend_y)
# plot(X_shuf, name + 'X_shuf_1d')
# plot(y_shuf, name + 'y_shuf_1d')
