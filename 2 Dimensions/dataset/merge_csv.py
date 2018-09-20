import pandas as pd


# Function to merge csv files
def merge_csv_files(files, workdir):
    dataframes = [pd.read_csv(workdir + f + '.csv') for f in files ]
    merged = pd.concat(dataframes, axis=0, join='outer', join_axes=None,
                       ignore_index=False, keys=None, levels=None, names=None,
                       verify_integrity=False, copy=True)
    merged.to_csv(workdir + "data.csv", index=False)


# Driver program
if __name__ == "__main__":
    print ('Merge csv files for training')
    files = ['data_0.05_xx', 'data_0.05_yy', 'data_0.05_xy',
             'data_0.025_xx', 'data_0.025_yy', 'data_0.025_xy',
             'data_0.036_xx', 'data_0.036_yy', 'data_0.036_xy']
             
    workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/dataset/results/'
    merge_csv_files(files, workdir)
    print ('csv file ready for training')
