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
                top = np.divide(df_aux[var].values, self.df_solver[var].values)
                # top = abs(self.df_solver[var].values - df_aux[var].values)
            elif variable in 'Objective Function Ratio':
                var = 'of'
                top = np.divide(df_aux[var].values, self.df_solver[var].values)
            else:
                top = 0
            bottom = np.zeros_like(top)
            width = depth = 1
            cmap = cm.get_cmap('hot')
            max_height = np.max(top)  # get range of colorbars
            min_height = np.min(top)
            norm = plt.Normalize(min_height, max_height)
            if method not in 'solver':
                rgba = [cmap((k - min_height) / (max_height - min_height)) for k in top]
            else:
                rgba = [cmap(k) for k in top]
            m = cm.ScalarMappable(norm=norm, cmap=cmap)
            fig.colorbar(m, ax=ax, shrink=0.8)
            ax.bar3d(df_aux['rows'], df_aux['columns'], bottom, width, depth, top, color=rgba, shade=True)
            ax.set_title(method)
            ax.set_xlim([3, 10])
            ax.set_ylim([3, 10])
            ax.set_xlabel('Rows')
            ax.set_ylabel('Columns')
            ax.set_zlabel(variable)
            plt.show()

    def plot2D(self):
        df = self.df[self.df['rows'] == self.df['columns']]
        fig = plt.figure()
        for method in self.methods:
            df_aux = df[df['method'] == method]
            plt.semilogy(df_aux['rows'], df_aux['time'])
            # plt.plot(df_aux['rows'], df_aux['time'])
        plt.legend(self.methods)
        plt.grid()
        plt.title('Execution time')
        plt.xlabel('Dimension (n x n)')
        plt.ylabel('Time (s)')
        plt.show()


if __name__ == '__main__':
    plot3D = Plot('results/exp_general_table_seed_0.csv')
    plot3D.plot3Dbar('Objective Function Ratio')
    plot3D.plot3Dbar('Execution Time')
    plot2D = Plot('results/exp_general_table_seed_0.csv')
    plot2D.plot2D()
