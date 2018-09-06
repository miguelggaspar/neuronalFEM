import numpy as np
import pandas as pd
from sklearn.externals import joblib
from matplotlib import pyplot as plt
from sklearn.neural_network import MLPClassifier


# Load loss function values thought training
data = pd.read_csv('loss_values.txt', sep=" ", header=None)
# Give labels
data.columns = ["iter", "loss"]

# Plot Loss function values
fig, ax = plt.subplots()
ax.plot(data['loss'], 'r', label='Training set')
# plt.style.use('ggplot')
legend = ax.legend(loc=0)
plt.xlabel("Iteration")
plt.ylabel("Mean square error")
plt.grid()
plt.xlim(xmax=105)
plt.title('Loss Function')

plt.savefig('graphs/loss_curve_1d', bbox_inches='tight')