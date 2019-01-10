from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def get_dataframe(df, spec, value):
    df_el = df[df[spec] == value]
    df_el.index = range(len(df_el))
    return df_el


# For further use, use this line to import trained model
# gs = joblib.load('results/gs.pkl')
gs = joblib.load('gridsearch/gs.pkl')

print("Best: %f using %s" % (gs.best_score_, gs.best_params_))


df = pd.DataFrame.from_dict(gs.cv_results_)
inv = get_dataframe(df, 'param_learning_rate', 'invscaling')
const = get_dataframe(df, 'param_learning_rate', 'constant')
adapt = get_dataframe(df, 'param_learning_rate', 'adaptive')
# node_2 = get_dataframe(df, 'param_hidden_layer_sizes', 2)
# node_4 = get_dataframe(df, 'param_hidden_layer_sizes', 4)
# node_7 = get_dataframe(df, 'param_hidden_layer_sizes', 7)
# node_10 = get_dataframe(df, 'param_hidden_layer_sizes', 10)

test_means = gs.cv_results_['mean_test_score']
test_stds = gs.cv_results_['std_test_score']
train_means = gs.cv_results_['mean_train_score']
train_stds = gs.cv_results_['std_train_score']

params = gs.cv_results_['params']
# count = 0
# for mean, stdev, param in zip(test_means, test_stds, params):
#     print("%f (%f) with: %r" % (mean, stdev, param))
#     # if (mean > 0.10 and mean <0.2 ):
#     count += 1
# print (count)
# nodes = [node_2, node_4, node_7, node_10]

l_rates = [inv, const, adapt]
l_rates_str = ['invscaling','constant','adaptive']

N = len(df)
# a = node_2['param_solver'].values + '\n' + node_2['param_activation'].values
# a = inv['param_solver'].values + '\n' + node_2['param_activation'].values
a = df['param_learning_rate'].values


node_str = ['node_2','node_4','node_7','node_10']
count = 0

# for node in nodes:
    # test = node['mean_test_score']
    # # train = node['mean_train_score']
    # test_std = node['std_test_score']
    # # train_std = node['std_train_score']
    # ind = np.arange(N)    # the x locations for the groups
    # width = 0.8       # the width of the bars: can also be len(x) sequence
    # p1 = plt.bar(ind, test, width, yerr=test_std)
    # # p2 = plt.bar(ind, train, width,
    # #              bottom=test, yerr=train_std)
    #
    # plt.ylabel('Scores')
    # plt.title('Scores by group and gender')
    # plt.xticks(ind, a)
    #
    # # plt.yticks(np.arange(0, 81, 10))
    # # plt.legend((p1[0], p2[0]), ('Test', 'Train'))
    # plt.legend((p1[0],), ('Test'))
    #
    # plt.show()

    #
########################################################
#     test = node['mean_test_score']
#     train = node['mean_train_score']
#     test_std = node['std_test_score']
#     train_std = node['std_train_score']
#
#     ind = np.arange(N)  # the x locations for the groups
#     width = 0.35       # the width of the bars
#
#     fig, ax = plt.subplots()
#     rects1 = ax.bar(ind, test, width, color='tab:orange', yerr=test_std)
#
#     rects2 = ax.bar(ind + width, train, width, color='tab:blue', yerr=train_std)
#
#     # add some text for labels, title and axes ticks
#     ax.set_ylabel(r'$R^2$')
#     ax.set_xticks(ind + width / 2)
#     ax.set_xticklabels(a)
#     ax.set_ylim(0,1)
#     ax.legend((rects1[0], rects2[0]), ('Cross-validation', 'Train'))
#     fig.savefig(node_str[count], bbox_inches='tight')
# ##################################################
#     count+=1

test = df['mean_test_score']
train = df['mean_train_score']
test_std = df['std_test_score']
train_std = df['std_train_score']

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, test, width, color='tab:orange', yerr=test_std)

rects2 = ax.bar(ind + width, train, width, color='tab:blue', yerr=train_std)

# add some text for labels, title and axes ticks
ax.set_ylabel(r'$R^2$')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(a)
ax.set_ylim(0,1)
ax.legend((rects1[0], rects2[0]), ('Cross-validation', 'Train'))
fig.savefig('l_rate', bbox_inches='tight')




    # autolabel(rects1,ax)
    # autolabel(rects2,ax)

    # plt.show()
