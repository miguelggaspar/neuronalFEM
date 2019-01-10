#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_data(workdir, name, flag):
    if flag == 1:
        df = pd.read_csv(workdir + name + '.csv', sep='\t' ,header=None)
    else:
        df = pd.read_csv(workdir + name + '.csv')
    return df

def rename_headers(df):
    df = df.rename(index=str, columns={0: 'ET', 1: 'S'})
    return df

def get_max_index(value, start, stop, num_el):
    index = int(np.floor((value-start)*(num_el-1)/(stop-start)+1))
    return index

def get_index(max_index, value, max_strain):
    index = np.floor((value * max_index) / max_strain)
    return index



# Driver program
if __name__ == "__main__":
    abaqus_dir = '/home/miguel/Documents/tese/ViscoPlastic-ML/abaqus_deploy/results/'
    pred_dir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/testmodel/results/'
    real_dir = '/home/miguel/Documents/tese/ViscoPlastic-ML/2 Dimensions/dataset/results/'
    graph_dir = '/home/miguel/Documents/tese/ViscoPlastic-ML/abaqus_deploy/graphs/'
    start = 0
    stop = 80
    num_el = 25000
    max_strain = 0.11
    max_strain_str = '011'
    trial = 'xy'
    trial_num = '12'


    name = 'abaqus_ET_S_' + max_strain_str + '_' + trial + '_2d'
    title = 'Trial ' + trial + ' with a maximum strain of '+ str(max_strain)
    #Get values from abaqus simulation
    abaqus = get_data(abaqus_dir, 'abaqus_' + max_strain_str + '_' + trial, 1)
    abaqus = rename_headers(abaqus)
    pred = get_data(pred_dir, 'predictions_' + str(max_strain) + '_' + trial + '_2d', 0)
    real = get_data(real_dir, 'data_' + str(max_strain) + '_' + trial, 0)
    max_idx = get_max_index(5, start, stop, num_el)

    indexs = []
    pred_stress = []
    real_stress = []
    p = []
    for value in abaqus['ET']:
        indexs.append(get_index(max_idx, value, max_strain))
        pred_stress.append(pred['S' + trial_num][get_index(max_idx, value, max_strain)])
        real_stress.append(real['S' + trial_num][get_index(max_idx, value, max_strain)])
        p.append(real['pStrain'][get_index(max_idx, value, max_strain)])

    plt.plot(abaqus['ET'], abaqus['S'], label='Stress (ANN-FEA)')
    plt.plot(pred['ET'+ trial_num][:max_idx], pred['S' + trial_num][:max_idx], label='Stress (ANN-model')
    plt.plot(pred['ET'+ trial_num][:max_idx], real['S' + trial_num][:max_idx], label='Stress (Experimental)')
    
    plt.xlabel('Strain')
    plt.ylabel('Stress [MPa]')
    plt.legend(loc=0, prop={'size': 10})
    plt.grid()

    plt.savefig(graph_dir + name + '.png', bbox_inches='tight')
