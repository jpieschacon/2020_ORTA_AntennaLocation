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

    def plot2DIter(self):
        df = self.df[self.df['rows'] == self.df['columns']]

        solver_time = df[df['method'] == 'solver'].iloc[0, 5]
        solver_of = df[df['method'] == 'solver'].iloc[0, 6]
        min_iter = df[df['iter'] != -1]['iter'].min()
        max_iter = df[df['iter'] != -1]['iter'].max()

        plt.hlines(solver_time, min_iter, max_iter, linestyles='dashdot', label='solver')
        for method in self.methods:
            if method != 'solver':
                df_aux = df[df['method'] == method]
                y_time = df_aux.groupby(['iter']).mean()['time']
                x_time = df_aux.groupby(['iter']).mean().index
                plt.plot(x_time, y_time, label=method)

                # y = df_aux.groupby(['rows']).mean()['time']
                # x = df_aux.groupby(['rows']).mean()['columns']
                # sy = df_aux.groupby(['rows']).std()['time']
                # plt.errorbar(x,y,yerr=sy,marker='_')
        plt.legend()
        plt.grid()
        plt.title('Execution time')
        plt.xlabel('Number of iterations')
        plt.ylabel('Time (s)')
        plt.yscale('log')
        plt.savefig(f'results/Figures/time_iter_comparison_{df.iloc[0,2]}x{df.iloc[0,2]}.pdf')
        plt.show()

        plt.hlines(100, min_iter, max_iter, linestyles='dashdot', label='solver')
        # plt.show()

        for method in self.methods:
            if method != 'solver':
                df_aux = df[df['method'] == method]
                y_time = df_aux.groupby(['iter']).mean()['of']
                x_time = df_aux.groupby(['iter']).mean().index
                plt.plot(x_time, 100*y_time/solver_of, label=method)

                # y = df_aux.groupby(['rows']).mean()['time']
                # x = df_aux.groupby(['rows']).mean()['columns']
                # sy = df_aux.groupby(['rows']).std()['time']
                # plt.errorbar(x,y,yerr=sy,marker='_')
        plt.legend()
        plt.grid()
        plt.title('Objective function')
        plt.xlabel('Number of iterations')
        plt.ylabel('Total cost ratio (%)')
        # plt.yscale('log')
        plt.savefig(f'results/Figures/cost_iter_comparison_{df.iloc[0,2]}x{df.iloc[0,2]}.pdf')
        plt.show()

    def plot2Ddistros(self):
        df = self.df[self.df['rows'] == self.df['columns']]
        distros = df['distro'][1:].unique()
        for distro in distros:
            df_aux = df[(df['distro'] == distro) & (df['flagSolver'] == 1)]
            y = df_aux.groupby(['rows']).mean()['time']
            sy = df_aux.groupby(['rows']).std()['time']
            x = df_aux.groupby(['rows']).mean()['columns']
            # plt.plot(x, y, label=distro)
            plt.errorbar(x, y, yerr=sy, marker='.', label=distro)
        plt.legend()
        plt.grid()
        plt.title('Execution time')
        plt.xlabel('Dimension (n x n)')
        plt.ylabel('Time (s)')
        plt.yscale('log')
        plt.savefig('results/Figures/execution_time_mean_distros.pdf')
        plt.show()

    def plot2DRatio(self):
        df = self.df
        for dimension in df['rows'].unique():
            df_aux = df[(df['flagSolver'] == 1) & (df['rows'] == dimension)]
            y = df_aux.groupby(['max_demand']).mean()['time']
            x = df_aux.groupby(['max_demand']).mean()['ratio']
            plt.plot(x, y, label=f"{dimension}x{dimension}")
        plt.xlim([0, 1])
        plt.grid()
        plt.legend()
        plt.title('Execution time')
        plt.xlabel('Ratio (Rmn/Qij)')
        plt.ylabel('Time (s)')
        plt.yscale('log')
        plt.savefig('results/Figures/execution_time_mean_ratio_Rmn_Qij.pdf')
        plt.show()

    def plotBox(self):
            df = self.df
            distan = df['seed'].unique()
            d = []
            c = "red"
            for i in distan:
                d.append(np.array(df['time'][(df['seed'] == i).values], dtype=float))
            plt.figure()
            plt.boxplot(d, labels=distan, patch_artist=True, boxprops=dict(facecolor=c, color=c))
            plt.grid()
            plt.xlabel('seed')
            plt.ylabel('time')
            plt.title('solver')
            plt.savefig('solver')
            plt.show()


if __name__ == '__main__':
    plot3D = Plot('results/exp_general_table_seed_0_9_3D.csv')
    plot3D.plot3Dbar('Objective Function Ratio')
    plot3D.plot3Dbar('Execution Time')
    plot2D = Plot('results/exp_general_table0_9_v2.csv')
    plot2D.plot2D()
    plot2DIter = Plot('results/exp_general_table_iter_4_2.csv')
    plot2DIter.plot2DIter()
    plot2DIter = Plot('results/exp_general_table_iter_8.csv')
    plot2DIter.plot2DIter()
    plot2Ddistros = Plot('results/exp_general_table_distros.csv')
    plot2Ddistros.plot2Ddistros()
    plot2DRatio = Plot('results/exp_general_table_ratio_NxN.csv')
    plot2DRatio.plot2DRatio()
    plotbox = Plot('results/exp_general_table_iter_same_solver6_v5.csv')
    plotbox.plotBox()
