import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm  # import colormap stuff
from mpl_toolkits.mplot3d import Axes3D


class Plot:
    def __init__(self, file):
        self.df = pd.read_csv(file)
        self.methods = self.df['method'][1:].unique()
        self.df_solver = self.df[self.df['method'] == 'solver']

    def plot3Dbar(self, variable):
        for method in self.methods:
            fig = plt.figure()
            ax = Axes3D(fig)
            df_aux = self.df[self.df['method'] == method]
            if variable in 'Execution Time':
                var = 'time'
                df_aux_mean = pd.DataFrame({'rows': [], 'columns': [], 'time': []})
                df_solver_mean = pd.DataFrame({'rows': [], 'columns': [], 'time': []})
                n = 0
                for i in df_aux['rows'].unique():
                    for j in df_aux['columns'].unique():
                        df_aux_mean = df_aux_mean.append(df_aux[(df_aux['rows'] == i) & (df_aux['columns'] == j)].agg({'time': ['mean']}))
                        df_solver_mean = df_solver_mean.append(self.df_solver[(self.df_solver['rows'] == i) & (self.df_solver['columns'] == j)].agg({'time': ['mean']}))
                        df_aux_mean['rows'][n] = i
                        df_solver_mean['rows'][n] = i
                        df_aux_mean['columns'][n] = j
                        df_solver_mean['columns'][n] = j
                        n += 1
                top = np.divide(df_aux_mean[var].values, df_solver_mean[var].values)
                # top = abs(self.df_solver[var].values - df_aux[var].values)
            elif variable in 'Objective Function Ratio':
                var = 'of'
                top = np.divide(df_aux[var][df_aux['seed'] == 0].values, self.df_solver[var][self.df_solver['seed'] == 0].values)
            else:
                top = 0
            bottom = np.zeros_like(top)
            width = depth = 1
            cmap = cm.get_cmap('jet')
            max_height = np.max(top)  # get range of colorbars
            min_height = np.min(top)
            norm = plt.Normalize(min_height, max_height)
            if method not in 'solver':
                rgba = [cmap((k - min_height) / (max_height - min_height)) for k in top]
            else:
                rgba = [cmap(k) for k in top]
            m = cm.ScalarMappable(norm=norm, cmap=cmap)
            fig.colorbar(m, ax=ax, shrink=0.8)
            ax.bar3d(df_aux['rows'][df_aux['seed'] == 0], df_aux['columns'][df_aux['seed'] == 0], bottom, width, depth, top, color=rgba, shade=True)
            ax.set_title(method)
            ax.set_xlim([3, 10])
            ax.set_ylim([3, 10])
            ax.set_xlabel('Rows')
            ax.set_ylabel('Columns')
            ax.set_zlabel(variable)
            plt.savefig(f'results/Figures/3D_{variable}_{method}.pdf')
            plt.show()

    def plot2D(self):
        df = self.df[self.df['rows'] == self.df['columns']]
        plt.figure()
        for method in self.methods:
            if method != 'solver':
                df_aux = df[df['method'] == method]
                y = df_aux.groupby(['rows']).mean()['time']
                x = df_aux.groupby(['rows']).mean()['columns']
                sy = df_aux.groupby(['rows']).std()['time']
                plt.errorbar(x, y, yerr=sy, marker='.')
        plt.legend(self.methods)
        plt.grid()
        plt.title('Execution time')
        plt.xlabel('Dimension (n x n)')
        plt.ylabel('Time (s)')
        plt.yscale('log')
        plt.savefig('results/Figures/execution_time_mean.pdf')
        plt.show()
        plt.figure()
        for method in self.methods:
            df_aux = df[df['method'] == method]
            y = df_aux.groupby(['rows']).mean()['time']
            x = df_aux.groupby(['rows']).mean()['columns']
            sy = df_aux.groupby(['rows']).std()['time']
            plt.errorbar(x, y, yerr=sy, marker='.')
        plt.legend(self.methods)
        plt.grid()
        plt.title('Execution time')
        plt.xlabel('Dimension (n x n)')
        plt.ylabel('Time (s)')
        plt.yscale('log')
        plt.savefig('results/Figures/execution_time_mean_sol.pdf')
        plt.show()

if __name__ == '__main__':
    plot3D = Plot('results/exp_general_table_seed_0_9_3D.csv')
    plot3D.plot3Dbar('Objective Function Ratio')
    plot3D.plot3Dbar('Execution Time')
    plot2D = Plot('results/exp_general_table_seed_0_9.csv')
    plot2D.plot2D()
