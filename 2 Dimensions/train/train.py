from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
import pandas as pd
from matplotlib import pyplot as plt
import pickle
import json


def savePerformance(params, X_train, y_train, filename):
    # file = open(filename, 'a+')
    # file.write(params)

    with open(filename, 'a+') as file:
        file.write(json.dumps(params)) # use `json.loads` to do the reverse
        file.write("\n")
    # pickle.dump(params['alpha'], file)
    file.close()


print('Training Neural network')
workdir = '/home/miguel/UA/tese/ViscoPlastic-ML/2 Dimensions/train/'
# Load Dataset for trainig
df = pd.read_csv(workdir + "../dataset/results/data.csv")
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

# last:
# relu, adaptive, (7,7), lbfgs, alpha 1
# estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(4, 4, 12),
#                          activation='relu', learning_rate='adaptive',
#                          alpha=1, random_state=1)
#
estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(20, 12, 20),
                         activation='tanh', learning_rate='constant',
                         alpha=1, random_state=1)

# estimator = MLPRegressor(solver='sgd', hidden_layer_sizes=(20, 20, 20),
#                          activation='relu', learning_rate='constant',
#                          alpha=1, random_state=1)

estimator.fit(X_train, y_train)

# Save hyperparameters and network performance
size = X.size / 11 / 3      # Size of training set for each trial

params = {'activation': estimator.activation, 'solver': estimator.solver,
          'learning_rate': estimator.learning_rate,
          'hidden_layer_sizes': estimator.hidden_layer_sizes,
          'alpha': estimator.alpha,
          'score': estimator.score(X_train, y_train),
          'loss': estimator.loss_, 'size': size}

dfs = pd.DataFrame({'activation': estimator.activation, 'solver': estimator.solver,
                    'learning_rate': estimator.learning_rate,
                #    'hidden_layer_sizes': estimator.hidden_layer_sizes,
                    'alpha': estimator.alpha,
                    'score': estimator.score(X_train, y_train),
                    'loss': estimator.loss_, 'size': [size]})

count = 0
for nodes in estimator.hidden_layer_sizes:
    layer_number = 'hidden_layer_'
    layer_number += str(count)
    df1 = pd.DataFrame({layer_number: [nodes]})
    dfs = pd.concat([dfs, df1], axis=1)
    count += 1

dfs.to_csv(workdir + "teste.csv",
           float_format='%.5f', index=False, mode='a', header=False)

savePerformance(params, X_train, y_train, 'teste.txt')
# Plot and save loss curve
# plt.plot(estimator.loss_curve_)
# plt.savefig('graphs/loss_curve_2d', bbox_inches='tight')

# Save trained model to further use. Scalers are required too, to transform
# the new data
joblib.dump(estimator, workdir + 'model/mlmodel.pkl')
joblib.dump(scaler_x, workdir + 'model/scaler_x.pkl')
joblib.dump(scaler_y, workdir + 'model/scaler_y.pkl')
print('Fnish Training Neural network')
