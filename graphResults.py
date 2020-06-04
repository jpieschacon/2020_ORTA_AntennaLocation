import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


df = pd.read_csv('results/exp_general_table_seed_0.csv')

methods = df['method'][1:].unique()

# 2D
df = df [df['rows'] == df['columns']]
fig = plt.figure()
for method in methods:
    df_aux = df[df['method'] == method]
    plt.semilogy(df_aux['rows'], df_aux['time'])
    # plt.plot(df_aux['rows'], df_aux['time'])

    # plt.hold(True)
plt.legend(methods)
plt.grid()
plt.title('Execution time')
plt.xlabel('Dimension (n x n)')
plt.ylabel('Time (s)')
plt.show()

# 3D
# df_solver = df[df['method'] == 'solver']
# for method in methods:
#     fig = plt.figure()
#     ax = Axes3D(fig)
#     df_aux = df[df['method'] == method]
#
#     top = np.divide(df_aux['of'].values, df_solver['of'].values)
#     # top = df_aux['of'].values - df_solver.values
#     bottom = np.zeros_like(top)
#     width = depth = 1
#     ax.bar3d(df_aux['rows'], df_aux['columns'], bottom, width, depth, top, shade=True)
#     # ax.scatter(df_aux['rows'], df_aux['columns'], df_aux['time'])
#     ax.set_title(method)
#     ax.set_xlim([3, 10])
#     ax.set_ylim([3, 10])
#     ax.set_xlabel('Rows')
#     ax.set_ylabel('Columns')
#     ax.set_zlabel('Zzzz')
#     plt.show()
#
#     fig = plt.figure()
#     ax = Axes3D(fig)
#     # top = df_aux['time']
#     top = np.divide(df_aux['time'].values, df_solver['time'].values)
#     # top = abs(df_solver['time'].values - df_aux['time'].values)
#     bottom = np.zeros_like(top)
#     width = depth = 1
#     ax.bar3d(df_aux['rows'], df_aux['columns'], bottom, width, depth, top, shade=True)
#     # ax.scatter(df_aux['rows'], df_aux['columns'], df_aux['time'])
#     ax.set_title(method)
#     ax.set_xlim([3, 10])
#     ax.set_ylim([3, 10])
#     ax.set_xlabel('Rows')
#     ax.set_ylabel('Columns')
#     ax.set_zlabel('Execution time')
#     plt.show()