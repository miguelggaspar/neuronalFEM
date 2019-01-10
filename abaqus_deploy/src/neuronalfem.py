#!/usr/bin/env python3
import numpy as np
from sklearn.externals import joblib

class NeuronalFem:
    """


    Args:
        param1 (str): Local path directory to machine learning model and scalers.

    Attributes:
        esimator (pickle obj): Estimator ready for prediction using the
                               multi-layer perceptron model.
        scaler_x (pickle obj): Contains the binary file, which has the methods
                               to be used for scaling features.
        scaler_y (pickle obj): Contains the binary file, which has the methods
                               to be used for scaling predictions.

    """

    def __init__(self, modeldir):

        self.estimator = joblib.load(modeldir + 'mlmodel.pkl')
        self.scaler_x = joblib.load(modeldir + 'scaler_x.pkl')
        self.scaler_y = joblib.load(modeldir + 'scaler_y.pkl')


    def get_features(self, filepath):
        """

        Args:
            param1 (str): Local path directory to the file containing
                          features

        """
        file = open(filepath, 'r')
        for line in file.readlines():
            features = line.rstrip().split(',')       # using rstrip to remove the \n
        features = [float(i) for i in features]
        file.close()
        return [features]


    def save_predictions(self, output, filepath):
        """

        Args:
            param1 (np.array): Local path directory to the file containing
                          features
            param2 (str): Local path directory to the file to save the output
        """

        file = open(filepath, 'wb')
        predictions = np.arange(8, dtype=float)     # Initialize predictions vector
        for i in range(0,8):
            predictions[i] = output[0][i]
        np.savetxt(file, [predictions], fmt='%0.6f', delimiter=',')
        file.close()
        return None

# Main program
if __name__ == "__main__":
    # Machine learning model directory
    modeldir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/train/model/'
    # Initialize neuronalfem class with trained model for further prediction
    # and scalers to transform the data.
    neuronalfem = NeuronalFem(modeldir)
    # Load features from features.txt file
    features = neuronalfem.get_features('/home/miguel/features.txt')
    # Transform features values to make predictions
    input = neuronalfem.scaler_x.transform(features)
    # Make predictions and transform the output
    output = neuronalfem.scaler_y.inverse_transform((neuronalfem.estimator.predict(input)))
    # Save predictions
    neuronalfem.save_predictions(output,'/home/miguel/predictions.txt')
