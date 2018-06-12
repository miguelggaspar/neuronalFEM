import numpy as np
import copy
import math
import pandas as pd
# Material parameters for steel 316 20C
E = 200000.0
v = 0.3
R1 = 436.0
k = 80.0
K = 85.2
a = 93.57
b = 21.3
c = 843.0
n = 4.55

t = np.linspace(0,80,1000)
Ei12 = np.zeros(1000)
asd = np.empty_like(t)
n = 1000
lists = [[np.ones(n)] for _ in range(3)]

z0 = np.array([3,4,5,6])
print z0

count = 0
# for i in range(3):
#     lists[i][0][0] = copy.deepcopy(z0[count])
#     count += 1

lists[0][0][0] = 0
lists[1][0][0] = 3
lists[2][0][0] = 2


# Save Results to csv file
df = pd.DataFrame({"IStrain": lists[0][0],"asdsatrain": lists[1][0]})
df.to_csv("data.csv", float_format='%.5f', index=False)

test = [lists[i] for i in range(3)]

print test

# lists[0]=1
#
# print lists[0][0][0] # value
# print lists[0][0] # each vector
# print lists[0][0][]

# Matriz de rigidez
stiff = E/(1-v**2) * np.array([[1, v, 0], [v, 1 , 0], [0, 0, (1-v)/2]])

# Alguns valores de deformacao para teste
ET = np.array([[0.01],[0.2],[0]])
EI = np.array([[0.005],[0.09],[0]])

stress = np.matmul(stiff,ET-EI)

print 'stress'+"\n", stress, "\n-------------------\n"

# Calculate deviatoric Stress
S_hyd = (1./3.)*(stress[0]+stress[1])
S_dev = copy.deepcopy(stress)
S_dev[0][0] -= S_hyd
S_dev[1][0] -= S_hyd
print 'deviatoric stress'+"\n", S_dev, "\n-------------------\n"

#Calculate deviatoric back stress
X = np.array([[1],[2],[3]])
X_hyd = (1./3.)*(X[0] + X[1])
X_dev = copy.deepcopy(X)
X_dev[0][0] -= X_hyd
X_dev[1][0] -= X_hyd
print 'deviatoric back stress'+"\n", X_dev.transpose(), "\n-------------------\n"

#Drag stress
R = 0

#Calculate invariant
J = math.sqrt((3./2.)*np.matmul((S_dev-X_dev).transpose(),S_dev-X_dev))
print 'J'+"\n", J, "\n-------------------\n"
# Calculate plastic strain rate
aux = (J - R - k) / K
print 'aux'+"\n", aux, "\n-------------------\n"
if aux < 0:
    dpdt = ((1./2.) * (aux + abs(aux)))**n
else:
    dpdt = 0
print 'Plastic Strain rate'+"\n", dpdt, "\n-------------------\n"

dEIdt = (3./2.) * dpdt * (S_dev-X_dev)/J
print 'Inelastic Strain rate'+"\n", dEIdt, "\n-------------------\n"

# Calculate Back stress rate
dXdt = (3./2.) * a * dEIdt - c * X * dpdt
print 'Back stress rate'+"\n", dXdt, "\n-------------------\n"
# Calculate Drag stress rate
dRdt = b * (R1 - R) * dpdt
print 'Drag stress rate'+"\n", dRdt, "\n-------------------\n"

print dEIdt.reshape(1,3)
print dEIdt[2][0]
lol = [dEIdt.reshape(1,3), dXdt.reshape(1,3) , dRdt, dpdt]
# lol2 = [dEIdt[i][0] for i in range(0,2), dXdt.reshape(1,3) , dRdt, dpdt]
dEIdt[:, 0]
lol2 = [dEIdt[:,0] , dXdt[:,0] , dRdt, dpdt]

a = np.array([[1],[2],[3],[4],[5],[6],[7],[8]])

A = a[3:6]

print A
print a[6]
print a[7]

asd = np.zeros((20, 3))
print asd


print dEIdt[2,0]
