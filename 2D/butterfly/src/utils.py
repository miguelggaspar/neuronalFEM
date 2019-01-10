import numpy as np
import pandas as pd


def get_data(dir):
    abaqus = pd.read_csv(dir[0], header=None)
    chaboche = pd.read_csv(dir[1])
    # deriv = pd.read_csv(dir[2], header=None)
    return abaqus, chaboche


def rename_headers(stat):
    stat = stat.rename(index=str, columns={0: "Ei11", 1: "Ei22", 2: "Ei12",
                        3: "R", 4: "S11", 5: "S22", 6: "S12", 7: "X11",
                        8: "X22", 9: "X12", 10: "p", 11: "ET11", 12: "ET22",
                        13: "ET12", 16:'EL', 17:'IP', 19: "t"})
    return stat

def rename_header_deriv(stat):
    stat = stat.rename(index=str, columns={0: "dEi11", 1: "dEi22", 2: "dEi12",
                        3: "dR", 4: "dX11", 5: "dX22", 6: "dX12", 7: "dp"})
    return stat

def get_max_index(value, start, stop, num_el):
    index = int(np.floor((value-start)*(num_el-1)/(stop-start)+1))
    return index


def get_index(max_index, value, max_strain):
    index = np.floor((value * max_index) / max_strain)
    return index

def get_dataframe(df, el_num, int_point):
    df_el = df[df['EL'] == el_num]
    df_int_p = df_el[df_el['IP'] == int_point]
    df_int_p.index = range(len(df_int_p))
    df_int_p = df_int_p.iloc[::2]
    df_int_p.index = range(len(df_int_p))
    # df_int_p = df_int_p.append(pd.DataFrame(index=['24'], data=df_int_p.tail(1).values, columns=df_int_p.columns))
    # df_int_p[19].iloc[-1] = 5
    return df_int_p
