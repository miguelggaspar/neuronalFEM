from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit
from sklearn.utils import shuffle
from utils import get_data

# For further use, use this line to import trained model
# gs = joblib.load('gs.pkl')
workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/train/'

# Load Dataset
X, y = get_data(workdir, 'training_data')

# Transform Dataset
scaler_x = preprocessing.StandardScaler()
scaler_y = preprocessing.StandardScaler()

scaler_x.fit(X)
scaler_y.fit(y)

X = scaler_x.transform(X)
y = scaler_y.transform(y)
X_shuf, y_shuf = shuffle(X, y)


estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(16),
                         activation='relu',
                         random_state=1, verbose=True)

train_sizes, train_scores, test_scores = learning_curve(estimator, X_shuf, y_shuf, cv=5)

plt.figure()
plt.xlabel("Training examples")
plt.ylabel(r'$R^2$')

train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

plt.grid()
plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                 train_scores_mean + train_scores_std, alpha=0.1,
                 color="r")
plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                 test_scores_mean + test_scores_std, alpha=0.1, color="g")
plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
         label="Training score")
plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
         label="Validation score")
plt.legend(loc=4)
plt.savefig('l_curve_2d.png', bbox_inches='tight')
plt.show()
