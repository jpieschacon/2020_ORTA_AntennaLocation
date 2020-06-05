import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm  # import colormap stuff
from mpl_toolkits.mplot3d import Axes3D


df = pd.read_csv('results/exp_general_table_seed_0.csv')

methods = df['method'][1:].unique()

# 2D
# df = df[df['rows'] == df['columns']]
# fig = plt.figure()
# for method in methods:
#     df_aux = df[df['method'] == method]
#     plt.semilogy(df_aux['rows'], df_aux['time'])
#     # plt.plot(df_aux['rows'], df_aux['time'])
#
#     # plt.hold(True)
# plt.legend(methods)
# plt.grid()
# plt.title('Execution time')
# plt.xlabel('Dimension (n x n)')
# plt.ylabel('Time (s)')
# plt.show()

# 3D
df_solver = df[df['method'] == 'solver']
for method in methods:
    # fig = plt.figure()
    # ax = Axes3D(fig)
    df_aux = df[df['method'] == method]
    # top = np.divide(df_aux['of'].values, df_solver['of'].values)
    # # top = df_aux['of'].values - df_solver.values
    # bottom = np.zeros_like(top)
    # width = depth = 1
    # cmap = cm.get_cmap('hot')
    # max_height = np.max(top)  # get range of colorbars
    # min_height = np.min(top)
    # norm = plt.Normalize(min_height, max_height)
    # if method != 'solver':
    #     rgba = [cmap((k - min_height) / (max_height-min_height)) for k in top]
    # else:
    #     rgba = [cmap((k - min_height) / max_height) for k in top]
    # m = cm.ScalarMappable(norm=norm, cmap=cmap)
    # fig.colorbar(m, ax=ax, shrink=0.8)
    # ax.bar3d(df_aux['rows'], df_aux['columns'], bottom, width, depth, top, color=rgba, shade=True, zsort='average')
    # # ax.scatter(df_aux['rows'], df_aux['columns'], df_aux['time'])
    # ax.set_title(method)
    # ax.set_xlim([3, 10])
    # ax.set_ylim([3, 10])
    # ax.set_xlabel('Rows')
    # ax.set_ylabel('Columns')
    # ax.set_zlabel('Objective Function Ratio')
    # plt.show()
#
    fig = plt.figure()
    ax = Axes3D(fig)
    # top = df_aux['time']
    top = np.divide(df_aux['time'].values, df_solver['time'].values)
    # top = abs(df_solver['time'].values - df_aux['time'].values)
    bottom = np.zeros_like(top)
    width = depth = 1
    cmap = cm.get_cmap('hot')
    max_height = np.max(top)  # get range of colorbars
    min_height = np.min(top)
    norm = plt.Normalize(min_height, max_height)
    if method not in 'solver':
        rgba = [cmap((k - min_height) / (max_height-min_height)) for k in top]
    else:
        rgba = [cmap(k) for k in top]
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    fig.colorbar(m, ax=ax, shrink=0.8)
    ax.bar3d(df_aux['rows'], df_aux['columns'], bottom, width, depth, top, color=rgba, shade=True)
    # ax.scatter(df_aux['rows'], df_aux['columns'], df_aux['time'])
    ax.set_title(method)
    ax.set_xlim([3, 10])
    ax.set_ylim([3, 10])
    ax.set_xlabel('Rows')
    ax.set_ylabel('Columns')
    ax.set_zlabel('Execution time')
    plt.show()