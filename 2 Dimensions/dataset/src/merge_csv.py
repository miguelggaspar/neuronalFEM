import pandas as pd
import sys

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

    files = []
    for k in range(len(sys.argv)):
        if (len(sys.argv) - k) == 1:
            break
        files.append('data_' + sys.argv[k+1] + '_xx')
        files.append('data_' + sys.argv[k+1] + '_yy')
        files.append('data_' + sys.argv[k+1] + '_xy')


    workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/dataset/results/'
    merge_csv_files(files, workdir)
    print ('csv file ready for training')
