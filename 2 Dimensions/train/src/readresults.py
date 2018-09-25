from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import pandas as pd

# For further use, use this line to import trained model
gs = joblib.load('../grid_results_1/gs.pkl')

# df = pd.read_csv("../../dataset/results/data.csv")
#
# # Choose features
# X = df.drop(["ET11", "ET22", "ET12", "dEi11", "dEi22", "dEi12", "Ee11", "Ee22",
#              "Ee12", "dX11", "dX12", "dX22", "dpStrain", "dR",
#              "Time"], axis=1)
# # Choose targets
# y = df.drop(["ET11", "ET22", "ET12", "Ei11", "Ei22", "Ei12", "Time",  "Ee11",
#              "Ee22",  "Ee12", "X11", "X22", "X12", "pStrain", "R", "S11",
#              "S22", "S12"], axis=1)
#
# scaler_x = preprocessing.StandardScaler()
# scaler_y = preprocessing.StandardScaler()
#
# scaler_x.fit(X)
# scaler_y.fit(y)
#
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3,
#                                                     random_state=42)
#
# X_train = scaler_x.transform(X_train)
# X_test = scaler_x.transform(X_test)
# y_train = scaler_y.transform(y_train)
# y_test = scaler_y.transform(y_test)


print("Best: %f using %s" % (gs.best_score_, gs.best_params_))
means = gs.cv_results_['mean_test_score']
stds = gs.cv_results_['std_test_score']
params = gs.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    if mean > 0.90:
         if param['solver'] == 'sgd':
            print("%f (%f) with: %r" % (mean, stdev, param))
