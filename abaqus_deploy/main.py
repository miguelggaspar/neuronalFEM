#!/usr/bin/env python3
import numpy as np
from sklearn.externals import joblib

# Load trained model for further prediction and scalers to transform the data.
ann = joblib.load('/home/miguel/UA/tese/ViscoPlastic-ML/2 Dimensions/train/model/mlmodel.pkl')
scaler_x = joblib.load('/home/miguel/UA/tese/ViscoPlastic-ML/2 Dimensions/train/model/scaler_x.pkl')
scaler_y = joblib.load('/home/miguel/UA/tese/ViscoPlastic-ML/2 Dimensions/train/model/scaler_y.pkl')

# print ('Python program running')
file_1 = open('/home/miguel/state.txt', 'r')
for line in file_1.readlines():
    values = line.rstrip().split(',')       # using rstrip to remove the \n

Ei11 = float(values[0])
Ei22 = float(values[1])
Ei12 = float(values[2])
R = float(values[3])
S = float(values[4])
X11 = float(values[5])
X22 = float(values[6])
X12 = float(values[7])
p = float(values[8])

file_1.close()
# print('Python: loading state from txt file')
# print('Python: Ei11 ', Ei11, ' Ei22 ', Ei22, ' R ', R, ' S ', ' X11 ', X11, ' X11 ', X22, ' p ', p)

input = scaler_x.transform([[Ei11, Ei22, R, S, X11, X22, p]])
output = scaler_y.inverse_transform((ann.predict(input)))

dEi11 = output[0][0]
dEi22 = output[0][1]
dEi12 = 0
dR = output[0][2]
dX11 = output[0][3]
dX22 = output[0][4]
dX12 = 0
dp = output[0][5]

# dEIdt = np.array([[output[0][0]], [output[0][1]], [0]])
# dRdt = output[0][2]
# dXdt = np.array([[output[0][3]], [output[0][4]], [0]])
# dpdt = output[0][5]

file = open('/home/miguel/derivatives.txt', 'w')
# file = open('/home/miguel/derivatives.txt', 'a')
derivatives = np.arange(8, dtype=float)     # Initialize derivatives vector
derivatives[0] = output[0][0]               # Inelastic Strain rate x
derivatives[1] = output[0][1]               # Inelastic Strain rate y
derivatives[2] = 0                          # Inelastic Strain rate xy
derivatives[3] = output[0][2]               # Drag Stress rate
derivatives[4] = output[0][3]               # Back Stress rate x
derivatives[5] = output[0][4]               # Back Stress rate y
derivatives[6] = 0                          # Back Stress rate xy
derivatives[7] = output[0][5]               # Plastic Strain rate

# print('Python: saving derivatives to txt file')
np.savetxt(file, [derivatives], fmt='%0.000005f', delimiter=',')
file.close()
# print('Python program ended')
