import pandas as pd
from sklearn.externals import joblib

def get_data(workdir, name):
    #Load whole dataset
    df = pd.read_csv(workdir + "../dataset/results/data_" + name + ".csv")
    # Chose features
    X = df.drop(["ET11", "ET22", "ET12", "dEi11", "dEi22", "dEi12", "Ee11", "Ee22",
                 "Ee12", "dX11", "dX12", "dX22", "dpStrain", "dR",
                 "Time"], axis=1)
    # Chose targets
    y = df.drop(["ET11", "ET22", "ET12", "Ei11", "Ei22", "Ei12", "Time",  "Ee11",
                 "Ee22",  "Ee12", "X11", "X22", "X12", "pStrain", "R", "S11",
                 "S22", "S12"], axis=1)
    return X, y

def get_trained_model():
    model_dir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/train/model/'
    ann = joblib.load(model_dir + 'mlmodel.pkl')
    scaler_x = joblib.load(model_dir + 'scaler_x.pkl')
    scaler_y = joblib.load(model_dir + 'scaler_y.pkl')
    return ann, scaler_x, scaler_y


def pre_process(X, y):
    scaler_x = preprocessing.StandardScaler()
    scaler_y = preprocessing.StandardScaler()
    scaler_x.fit(X)
    scaler_y.fit(y)
    X = scaler_x.transform(X)
    y = scaler_y.transform(y)
    return X, y
