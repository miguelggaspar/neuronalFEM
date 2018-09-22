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

    if len(sys.argv) == 2:
        files = ['data_' + sys.argv[1] + '_xx', 'data_' + sys.argv[1] + '_yy',
                 'data_' + sys.argv[1] + '_xy']
    elif len(sys.argv) == 3:
        files = ['data_' + sys.argv[1] + '_xx', 'data_' + sys.argv[1] + '_yy',
                 'data_' + sys.argv[1] + '_xy', 'data_' + sys.argv[2] + '_xx',
                 'data_' + sys.argv[2] + '_yy', 'data_' + sys.argv[2] + '_xy']
    elif len(sys.argv) == 4:
        files = ['data_' + sys.argv[1] + '_xx', 'data_' + sys.argv[1] + '_yy',
                 'data_' + sys.argv[1] + '_xy', 'data_' + sys.argv[2] + '_xx',
                 'data_' + sys.argv[2] + '_yy', 'data_' + sys.argv[2] + '_xy',
                 'data_' + sys.argv[3] + '_xx', 'data_' + sys.argv[3] + '_yy',
                 'data_' + sys.argv[3] + '_xy']
    elif len(sys.argv) == 5:
        files = ['data_' + sys.argv[1] + '_xx', 'data_' + sys.argv[1] + '_yy',
                 'data_' + sys.argv[1] + '_xy', 'data_' + sys.argv[2] + '_xx',
                 'data_' + sys.argv[2] + '_yy', 'data_' + sys.argv[2] + '_xy',
                 'data_' + sys.argv[3] + '_xx', 'data_' + sys.argv[3] + '_yy',
                 'data_' + sys.argv[3] + '_xy', 'data_' + sys.argv[4] + '_xx',
                 'data_' + sys.argv[4] + '_yy', 'data_' + sys.argv[4] + '_xy']
    elif len(sys.argv) == 6:
        files = ['data_' + sys.argv[1] + '_xx', 'data_' + sys.argv[1] + '_yy',
                 'data_' + sys.argv[1] + '_xy', 'data_' + sys.argv[2] + '_xx',
                 'data_' + sys.argv[2] + '_yy', 'data_' + sys.argv[2] + '_xy',
                 'data_' + sys.argv[3] + '_xx', 'data_' + sys.argv[3] + '_yy',
                 'data_' + sys.argv[3] + '_xy', 'data_' + sys.argv[4] + '_xx',
                 'data_' + sys.argv[4] + '_yy', 'data_' + sys.argv[4] + '_xy',
                 'data_' + sys.argv[5] + '_xx', 'data_' + sys.argv[5] + '_yy',
                 'data_' + sys.argv[5] + '_xy']


    workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/dataset/results/'
    merge_csv_files(files, workdir)
    print ('csv file ready for training')
