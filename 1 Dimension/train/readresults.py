from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import pandas as pd

# For further use, use this line to import trained model
gs = joblib.load('gs.pkl')

df = pd.read_csv("../../dataset/data.csv")

X = df.drop(["dIStrain", "dX", "dR", "Time"], axis=1)
y = df.drop(["IStrain", "TStrain", "X", "R", "Time", "Stress"], axis=1)

Xtime = df.drop(["dIStrain", "dX", "dR", "IStrain", "TStrain",
                 "X", "R", "Stress"], axis=1)

scaler_x = preprocessing.StandardScaler()
scaler_y = preprocessing.StandardScaler()

scaler_x.fit(X)
scaler_y.fit(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)
Xtime_train, Xtime_test, ytime_train, ytime_test = train_test_split(Xtime, y, test_size=.3, random_state=42)

X_train = scaler_x.transform(X_train)
X_test = scaler_x.transform(X_test)
y_train = scaler_y.transform(y_train)
y_test = scaler_y.transform(y_test)


print("Best: %f using %s" % (gs.best_score_, gs.best_params_))
means = gs.cv_results_['mean_test_score']
stds = gs.cv_results_['std_test_score']
params = gs.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))
