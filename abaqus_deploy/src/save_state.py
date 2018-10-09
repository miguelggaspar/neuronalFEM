#!/usr/bin/env python3
import numpy as np
workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/abaqus_deploy/'
# Load trained model for further prediction and scalers to transform the data.

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#   print ('Python program running')
file_1 = open('/home/miguel/state_debug.txt', 'r')
for line in file_1.readlines():
    values = line.rstrip().split(',')       # using rstrip to remove the \n

state = np.arange(len(values), dtype=float)     # Initialize derivatives vector

for i in range(0, len(values)):
    state[i] = float(values[i])

file_1.close()

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
file_2 = open('/home/miguel/derivatives.txt', 'r')
for line in file_2.readlines():
    valuess = line.rstrip().split(',')       # using rstrip to remove the \n

derivatives = np.arange(len(valuess), dtype=float)     # Initialize derivatives vector

for i in range(0, len(valuess)):
    derivatives[i] = float(valuess[i])

file_2.close()
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------


file_hist_state = open(workdir + 'state_debug.txt', 'ab+')
file_hist_deriv = open(workdir + 'derivatives_debug.txt', 'ab+')

# file = open('/home/miguel/derivatives.txt', 'a')
np.savetxt(file_hist_state, [state], fmt='%0.20f', delimiter=',')
np.savetxt(file_hist_deriv, [derivatives], fmt='%0.20f', delimiter=',')

file_hist_state.close()
file_hist_deriv.close()
# print('Python program ended')
