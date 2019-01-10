import numpy as np
import pandas as pd
from sklearn.externals import joblib
from matplotlib import pyplot as plt
from sklearn.neural_network import MLPClassifier


# Load loss function values thought training
# Load neural network
ann = joblib.load('../model/mlmodel.pkl')
# Plot Loss function values
fig, ax = plt.subplots()
ax.plot(ann.loss_curve_, 'r', label='Training set')
# plt.style.use('ggplot')
legend = ax.legend(loc=0)
plt.xlabel("Iteration")
plt.ylabel("Mean square error")
plt.grid()
# plt.xlim()
plt.title('Loss Function')
plt.savefig('../graphs/loss_curve_2d', bbox_inches='tight')
