import pandas as pd
import matplotlib.pyplot as plt
import sys


# Function to read simulation values and plot graphs
def get_data(jobname, workdir):
    df_stat = pd.read_csv(workdir + 'stat_' + jobname + '.txt', header=None)
    df_der = pd.read_csv(workdir + 'der_' + jobname + '.txt', header=None)
    return df_stat, df_der

def rename_headers(stat, deriv):
    stat = stat.rename(index=str, columns={0: "Ei11", 1: "Ei22", 2: "Ei12",
                        3: "R", 4: "S11", 5: "S22", 6: "S12", 7: "X11",
                        8: "X22", 9: "X12", 10: "p", 11: "ET11", 12: "ET22",
                        13: "ET12"})
    deriv = deriv.rename(index=str, columns={0: "dEi11", 1: "dEi22",
                          2: "dEi12", 3: "dR", 4: "dX11", 5: "dX22",
                          6: "dX12", 7: "dp"})
    return stat, deriv

def plot_results(stat,deriv):
    plt.subplot(2,3,1)
    plt.plot(stat['Ei11'])
    plt.subplot(2,3,2)
    plt.plot(stat['Ei22'])
    plt.subplot(2,3,3)
    plt.plot(stat['Ei12'])
    plt.subplot(2,3,4)
    plt.plot(deriv['dEi11'])
    plt.subplot(2,3,5)
    plt.plot(deriv['dEi22'])
    plt.subplot(2,3,6)
    plt.plot(deriv['dEi12'])
    
# Driver program
if __name__ == "__main__":
    workdir = '/home/miguel/UA/tese/ViscoPlastic-ML/abaqus_deploy/'
    if len(sys.argv) > 1:
        stat, deriv = get_data(sys.argv[1], workdir)
        stat, deriv = rename_headers(stat, deriv)
        plot_results(stat, deriv)
        plt.show()
    else:
        print('Not enough input arguments. You must specify the job name.')
        exit()
