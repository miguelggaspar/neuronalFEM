import pandas as pd
import matplotlib.pyplot as plt

n = 2300

df = pd.read_csv('data.csv')
plt.subplot(1,3,1)
plt.plot(df['Time'][:n], df['S11'][:n])

plt.subplot(1,3,2)
plt.plot(df['Time'][n:2*n], df['S22'][n:2*n])

plt.subplot(1,3,3)
plt.plot(df['Time'][2*n:], df['S12'][2*n:])

plt.show()
