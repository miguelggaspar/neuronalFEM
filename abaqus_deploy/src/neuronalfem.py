#!/usr/bin/env python3
import numpy as np
from sklearn.externals import joblib
workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/abaqus_deploy/'
# Load trained model for further prediction and scalers to transform the data.
ann = joblib.load('/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/train/model/mlmodel.pkl')
scaler_x = joblib.load('/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/train/model/scaler_x.pkl')
scaler_y = joblib.load('/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/train/model/scaler_y.pkl')

#   print ('Python program running')
file_1 = open('/home/miguel/state.txt', 'r')
for line in file_1.readlines():
    values = line.rstrip().split(',')       # using rstrip to remove the \n

Ei11 = float(values[0])
Ei22 = float(values[1])
Ei12 = float(values[2])
R = float(values[3])
S11 = float(values[4])
S22 = float(values[5])
S12 = float(values[6])
X11 = float(values[7])
X22 = float(values[8])
X12 = float(values[9])
p = float(values[10])
ET11 = float(values[11])
ET22 = float(values[12])
ET12 = float(values[13])
kinc = float(values[14])
kstep = float(values[15])
noel = float(values[16])
npt = float(values[17])
kspt = float(values[18])

state = np.arange(19, dtype=float)     # Initialize derivatives vector

for i in range(0, 19):
    # print ('inside python')
    state[i] = float(values[i])
    # print (state[i])

file_1.close()
# print('Python: loading state from txt file')
# print('Python: Ei11 ', Ei11, ' Ei22 ', Ei22, ' R ', R, ' S ', ' X11 ', X11, ' X11 ', X22, ' p ', p)

input = scaler_x.transform([[Ei11, Ei12, Ei22, R, S11, S12, S22,
                             X11, X12, X22, p]])
output = scaler_y.inverse_transform((ann.predict(input)))

dEi11 = output[0][0]
dEi12 = output[0][1]
dEi22 = output[0][2]
dR = output[0][3]
dX11 = output[0][4]
dX12 = output[0][5]
dX22 = output[0][6]
dp = output[0][7]

# dEIdt = np.array([[output[0][0]], [output[0][1]], [0]])
# dRdt = output[0][2]
# dXdt = np.array([[output[0][3]], [output[0][4]], [0]])
# dpdt = output[0][5]

file = open('/home/miguel/derivatives.txt', 'wb')
file_hist_state = open(workdir + 'state.txt', 'ab+')
file_hist_deriv = open(workdir + 'derivatives.txt', 'ab+')

# file = open('/home/miguel/derivatives.txt', 'a')
derivatives = np.arange(8, dtype=float)     # Initialize derivatives vector
derivatives[0] = output[0][0]               # Inelastic Strain rate x
derivatives[1] = output[0][2]               # Inelastic Strain rate y
derivatives[2] = output[0][1]               # Inelastic Strain rate xy
derivatives[3] = output[0][3]               # Drag Stress rate
derivatives[4] = output[0][4]               # Back Stress rate x
derivatives[5] = output[0][6]               # Back Stress rate y
derivatives[6] = output[0][5]               # Back Stress rate xy
derivatives[7] = output[0][7]               # Plastic Strain rate

# print('Python: saving derivatives to txt file')
np.savetxt(file, [derivatives], fmt='%0.6f', delimiter=',')
np.savetxt(file_hist_state, [state], fmt='%0.20f', delimiter=',')
np.savetxt(file_hist_deriv, [derivatives], fmt='%0.6f', delimiter=',')

# Close files
file.close()
file_hist_state.close()
file_hist_deriv.close()
# print('Python program ended')
