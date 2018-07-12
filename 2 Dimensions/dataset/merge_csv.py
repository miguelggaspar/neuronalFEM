import pandas as pd


# Function to merge csv files
def merge_csv_files(files):
    dataframes = [ pd.read_csv( f + '.csv' ) for f in files ]
    merged = pd.concat( dataframes, axis=0, join='outer', join_axes=None,
                    ignore_index=False, keys=None, levels=None, names=None,
                    verify_integrity=False, copy=True)
    merged.to_csv("data.csv", index=False)


# Driver program
if __name__ == "__main__":
    print ('Merge csv files for training')
    files = ['data_xx', 'data_yy', 'data_xy']
    merge_csv_files(files)
