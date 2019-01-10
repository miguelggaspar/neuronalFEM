from sklearn.externals import joblib
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import validation_curve
from matplotlib import pyplot as plt
import pickle
import sys
import numpy as np
from sklearn.utils import shuffle
from utils import get_data

workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/train/'

# Load Dataset
X, y = get_data(workdir, 'training_data')

scaler_x = preprocessing.StandardScaler()
scaler_y = preprocessing.StandardScaler()

# Fit the scaler to transform features and targets
scaler_x.fit(X)
scaler_y.fit(y)


# Split Dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3,
                                                    random_state=42)

# Transform data to training and testing
X = scaler_x.transform(X)
y = scaler_y.transform(y)

X_shuf, y_shuf = shuffle(X, y)

estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(16),
                         activation='relu',
                         random_state=1)

train_scores, valid_scores = validation_curve(estimator, X_shuf, y_shuf, "alpha",
                                              np.logspace(-7, 3, 10),
                                              cv=5)
param_range = np.logspace(-7,3,10)
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
valid_scores_mean = np.mean(valid_scores, axis=1)
valid_scores_std = np.std(valid_scores, axis=1)

# plt.title("Validation Curve")
plt.xlabel(r"$\lambda$")
plt.ylabel(r"$R^2$")
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
plt.savefig('v_curve_y_2d.png', bbox_inches='tight')
plt.show()
#
