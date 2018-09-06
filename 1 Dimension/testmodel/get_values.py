import pandas as pd


df = pd.read_csv("../dataset/data.csv")
pred = pd.read_csv("predictions_1d.csv")

def get_values(idx, col, dataframe):
    print ( col, "  ->  ",dataframe.at[idx,col])


print ("Get values from a specific time")
print (" ")
print (" ")
print (" Real values")
get_values(188, 'X', df)
get_values(188, 'R', df)
get_values(188, 'Stress', df)
get_values(188, 'IStrain', df)
print (" ")
print (" ")
print (" Predicted values")
get_values(188, 'X', pred)
get_values(188, 'R', pred)
get_values(188, 'S', pred)
get_values(188, 'EI', pred)
