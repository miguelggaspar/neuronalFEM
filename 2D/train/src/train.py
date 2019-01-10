from sklearn.externals import joblib
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.utils import shuffle
import pickle
import sys
from utils import get_data


print('Training Neural network')
workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/train/'

X, y = get_data(workdir, 'training_data')

scaler_x = preprocessing.StandardScaler()
scaler_y = preprocessing.StandardScaler()

# Fit the scaler to transform features and targets
scaler_x.fit(X)
scaler_y.fit(y)

X = scaler_x.transform(X)
y = scaler_y.transform(y)

estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(16),
                         activation='relu', verbose=True,
                         random_state=1)

X_shuf, y_shuf = shuffle(X, y)
exit()

# Train the model
estimator.fit(X_shuf, y_shuf)

print (estimator.score(X_shuf, y_shuf))
print (estimator.loss_)

# Save trained model to further use. Scalers are required too, to transform
# the new data
joblib.dump(estimator, workdir + 'model/mlmodel.pkl')
joblib.dump(scaler_x, workdir + 'model/scaler_x.pkl')
joblib.dump(scaler_y, workdir + 'model/scaler_y.pkl')
print('Fnish Training Neural network')
