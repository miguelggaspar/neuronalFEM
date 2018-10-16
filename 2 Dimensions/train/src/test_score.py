from utils import get_data, get_trained_model
import matplotlib.pyplot as plt

if __name__ == "__main__":
    workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/train/'
    "Calculate test score"
    # # Get features and targets
    # X, y = get_data(workdir, 'test')
    ann, scaler_x, scaler_y = get_trained_model()
    X = scaler_x.transform(X)
    y = scaler_y.transform(y)
    score = ann.score(X,y)
    print(score)
