import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys


# Function to read simulation values and plot graphs
def get_data(jobname, workdir, strain):
    df_stat = pd.read_csv(workdir + 'state_plane_stress_'+ jobname + '_' + strain + '_hist.txt', header=None)
    df_der = pd.read_csv(workdir + 'deriv_plane_stress_'+ jobname +'_' + strain + '_hist.txt', header=None)
    return df_stat, df_der

def get_csv(workdir, name):
    df = pd.read_csv(workdir + name + '.csv')
    return df

def rename_headers(stat, deriv):
    stat = stat.rename(index=str, columns={0: "Ei11", 1: "Ei22", 2: "Ei12",
                        3: "R", 4: "S11", 5: "S22", 6: "S12", 7: "X11",
                        8: "X22", 9: "X12", 10: "p", 11: "ET11", 12: "ET22",
                        13: "ET12"})
    deriv = deriv.rename(index=str, columns={0: "dEi11", 1: "dEi22",
                          2: "dEi12", 3: "dR", 4: "dX11", 5: "dX22",
                          6: "dX12", 7: "dp"})
    return stat, deriv

def get_max_index(value, start, stop, num_el):
    index = int(np.floor((value-start)*(num_el-1)/(stop-start)+1))
    return index

def get_index(max_index, value, max_strain):
    index = np.floor((value * max_index) / max_strain)
    return index

# Chose indexs of 4th integration point
def get_indexs(stat):
    indexs = []
    for n in range(0, len(stat)):
        if 4*n-1 > len(stat):
            break
        if n==0:
            pass
        else:
            indexs.append(4*n-1)
    return indexs

# Driver program
if __name__ == "__main__":
    workdir = '/home/miguel/Documents/tese/ViscoPlastic-ML/abaqus_deploy/results/'
    pred_dir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/testmodel/results/'
    real_dir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2D/dataset/results/'
    graph_dir = '/home/miguel/Documents/tese/ViscoPlastic-ML/abaqus_deploy/graphs/'

    if len(sys.argv) > 1:
        trial = sys.argv[1]
        start = 0
        stop = 80
        num_el = 25000
        max_strain = 0.18
        max_strain_str = '018'
        max_strain_str_1 = '18'
        trial_num = '12'
        name = 'abaqus_EI_' + max_strain_str + '_' + trial + '_2d'

        stat, deriv = get_data(sys.argv[1], workdir, max_strain_str_1)
        stat, deriv = rename_headers(stat, deriv)

        pred = get_csv(pred_dir, 'predictions_' + str(max_strain) + '_' + trial + '_2d')
        real = get_csv(real_dir, 'data_' + str(max_strain) + '_' + trial)

        max_idx = get_max_index(5, start, stop, num_el)
        indexs = get_indexs(stat)
        stress = []
        strain = []
        visco = []
        elastic = []
        time = []
        dEi = []
        Ei = []
        dR = []
        R = []
        dp = []
        dstrain = []
        for idx in indexs:
            stress.append(stat['S' + trial_num][idx])
            strain.append(stat['ET' + trial_num][idx])
            visco.append(stat['Ei'+ trial_num][idx])
            elastic.append(stat['ET' + trial_num][idx] - stat['Ei' + trial_num][idx])
            time.append(stat[19][idx])
            dstrain.append(stat[20][idx])
            dEi.append(deriv['dEi' + trial_num][idx])
            Ei.append(stat['Ei' + trial_num][idx])
            R.append(stat['R'][idx])
            dR.append(deriv['dR'][idx])
            dp.append(deriv['dp'][idx])

        idxs = []
        pred_viscostrain = []
        real_viscostrain = []
        pred_elast = []
        real_elast = []
        S_real = []
        S_pred = []
        for value in strain:
            indexs.append(get_index(max_idx, value, max_strain))
            pred_viscostrain.append(pred['Ei' + trial_num][get_index(max_idx, value, max_strain)])
            real_viscostrain.append(real['Ei' + trial_num][get_index(max_idx, value, max_strain)])
            S_real.append(real['S' + trial_num][get_index(max_idx, value, max_strain)])
            S_pred.append(pred['S' + trial_num][get_index(max_idx, value, max_strain)])

        # visco[16:] = [0.00331, 0.01126, 0.01126, 0.02775, 0.02775, 0.055139999999999995, 0.055139999999999995]

        plt.plot(time, strain, label=r'Total Strain')
        plt.plot(time, visco, label=r'Viscoplastic Strain (ANN-FEA)')
        plt.plot(time, elastic, label=r'Elastic Strain (ANN-FEA)')
        plt.plot(time, pred_viscostrain, label=r'Viscoplastic Strain (ANN-model)')
        plt.plot(time, real_viscostrain, label=r'Viscoplastic Strain (Experimental)')
        plt.legend(loc=2, prop={'size': 10})
        plt.ylabel('Strain')
        plt.xlabel('Time [s]')
        plt.grid()
        plt.savefig(graph_dir + name + '.png', bbox_inches='tight')

    else:
        print('Not enough input arguments. You must specify the job name.')
        exit()
