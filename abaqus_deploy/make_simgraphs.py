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


def plot_results(stat, deriv):
    plt.figure(figsize=(8, 5), dpi=80)
    props = ['Ei11', 'Ei22', 'Ei12', 'dEi11', 'dEi22', 'dEi12']
    count = 1
    for prop in props:
        plt.subplot(2, 3, count)
        if count < 4:
            plt.plot(stat[prop])
        else:
            plt.plot(deriv[prop])
        count += 1
    plt.figure(figsize=(8, 5), dpi=80)
    props = ['X11', 'X22', 'X12', 'dX11', 'dX22', 'dX12']
    count = 1
    for prop in props:
        plt.subplot(2, 3, count)
        if count < 4:
            plt.plot(stat[prop])
        else:
            plt.plot(deriv[prop])
        count += 1
    plt.figure(figsize=(8, 5), dpi=80)
    plt.subplot(1, 2, 1)
    plt.plot(stat['R'])
    plt.subplot(1, 2, 2)
    plt.plot(deriv['dR'])
    plt.figure(figsize=(8, 5), dpi=80)
    plt.subplot(1, 2, 1)
    plt.plot(stat['p'])
    plt.subplot(1, 2, 2)
    plt.plot(deriv['dp'])
    plt.figure(figsize=(8, 5), dpi=80)
    props = ['S11', 'S22', 'S12']
    count = 1
    for prop in props:
        plt.subplot(1, 3, count)
        plt.plot(stat[prop])
        count += 1
    plt.figure(figsize=(8, 5), dpi=80)
    props = ['ET11', 'S11', 'ET22', 'S22', 'ET12', 'S12']
    count = 1
    n = 0
    # for :
    #     plt.subplot(1, 3, count)
    #     plt.plot(stat[props[2*n]], stat[props[2*n+1]])
    #     n += 1
    #     print (n)
    #     count += 1


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
