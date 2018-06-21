from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
import pandas as pd

# Load Dataset for trainig
df = pd.read_csv("../dataset/data.csv")
# Choose features
X = df.drop(["ET11", "ET22", "ET12", "dEi11", "dEi22", "dEi12", "Ee11", "Ee22",
             "Ee12", "dX11", "dX12", "dX22", "dpStrain", "dR", "Time"], axis=1)
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

estimator = MLPRegressor(solver='lbfgs', hidden_layer_sizes=(4,4),
                         activation='relu', learning_rate='adaptive',
                         alpha=1, random_state=1)

estimator.fit(X_train, y_train)
# Save trained model to further use. Scalers are required too, to transform
# the new data
joblib.dump(estimator, 'model/mlmodel.pkl')
joblib.dump(scaler_x, 'model/scaler_x.pkl')
joblib.dump(scaler_y, 'model/scaler_y.pkl')
