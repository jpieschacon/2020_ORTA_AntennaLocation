# -*- coding: utf-8 -*-
import time
import numpy as np
from pulp import *
import re


class AntennaLocation:
    def __init__(self, dict_data):
        logging.info("#########")
        # items = range(dict_data['n_items'])

        self.x = LpVariable.dicts(
            "x", ((i, j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat="Binary"
        )

        self.q = LpVariable.dicts(
            "q", ((i, j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )

        self.q_NW = LpVariable.dicts(
            "q_NW", ((i, j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )
        self.q_NE = LpVariable.dicts(
            "q_NE", ((i, j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )

        self.q_SW = LpVariable.dicts(
            "q_SW", ((i, j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )

        self.q_SE = LpVariable.dicts(
            "q_SE", ((i, j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )

        self.z = LpVariable.dicts(
            "z", ((m, n, k) for m in range(dict_data['antennaRow'] - 1) for n in range(dict_data['antennaColumn'] - 1) for k in range(5)),
            lowBound=0,
            cat="Binary"
        )
        # LpContinuous
        self.R = dict_data['demand']
        self.c = dict_data['cost']
        self.Q = dict_data['capacity']

        self.problem_name = "antennalocation"

        self.prob = LpProblem(self.problem_name, LpMinimize)
        self.prob += lpSum([self.c[i, j] * self.x[i, j] for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])]), "obj_func"
        for m in range(dict_data['antennaRow'] - 1):
            for n in range(dict_data['antennaColumn'] - 1):
                self.prob += lpSum(self.z[m, n, k] for k in range(5)) == 1, f"2_{m}_{n}"
                self.prob += 4 - lpSum([self.x[i, j]] for i in [m, m + 1] for j in [n, n + 1]) == lpSum([(4 - k) * self.z[m, n, k] for k in range(5)]), f"3_{m}_{n}"
                for k in range(5):
                    self.prob += self.q_SE[m, n] * k - self.R[m, n] * self.x[m, n] <= (1 - self.z[m, n, k]) * self.Q[m, n] * 100, f"4_{m}_{n}_{k}"
                    self.prob += self.q_SW[m, n + 1] * k - self.R[m, n] * self.x[m, n + 1] <= (1 - self.z[m, n, k]) * self.Q[m, n + 1] * 100, f"5_{m}_{n}_{k}"
                    self.prob += self.q_NE[m + 1, n] * k - self.R[m, n] * self.x[m + 1, n] <= (1 - self.z[m, n, k]) * self.Q[m + 1, n] * 100, f"6_{m}_{n}_{k}"
                    self.prob += self.q_NW[m + 1, n + 1] * k - self.R[m, n] * self.x[m + 1, n + 1] <= (1 - self.z[m, n, k]) * self.Q[m + 1, n + 1] * 100, f"7_{m}_{n}_{k}"
                self.prob += self.q_SE[m, n] + self.q_SW[m, n + 1] + self.q_NE[m + 1, n] + self.q_NW[m + 1, n + 1] == self.R[m, n], f"8_{m}_{n}"  # lina
        for i in range(dict_data['antennaRow']):
            for j in range(dict_data['antennaColumn']):
                self.prob += self.q[i, j] == self.q_NW[i, j] + self.q_NE[i, j] + self.q_SW[i, j] + self.q_SE[i, j], f"9_{i}_{j}"
                self.prob += self.q[i, j] <= self.Q[i, j] * self.x[i, j], f"10_{i}_{j}"

        self.prob.writeLP("./logs/{}.lp".format(self.problem_name))

    def solve(
            self, dict_data, time_limit=None,
            gap=None, verbose=False
    ):
        """[summary]
        
        Arguments:
            dict_data {[type]} -- [description]
        
        Keyword Arguments:
            time_limit {[type]} -- [description] (default: {None})
            gap {[type]} -- [description] (default: {None})
            verbose {bool} -- [description] (default: {False})
        
        Returns:
            [type] -- [description]
        """

        msg_val = 1 if verbose else 0
        start = time.time()
        solver = COIN_CMD(
            msg=msg_val,
            maxSeconds=time_limit,
            fracGap=gap
        )

        flagSolver = solver.solve(self.prob)

        end = time.time()
        logging.info("\t Status: {}".format(LpStatus[self.prob.status]))

        sol = self.prob.variables()
        of = value(self.prob.objective)
        comp_time = end - start

        sol_x = np.zeros((dict_data['antennaRow'], dict_data['antennaColumn']))
        sol_q = np.zeros((dict_data['antennaRow'], dict_data['antennaColumn']))

        if flagSolver != -1:
            for var in sol:
                logging.info("{} {}".format(var.name, var.varValue))
                # if var.varValue != 0:
                # print(var.name, "\t", var.varValue)
                if "x_" in var.name:
                    index = re.findall(r'\d+', var.name.replace('x_', ''))
                    sol_x[int(index[0]), int(index[1])] = var.varValue
                elif "q_(" in var.name:
                    index = re.findall(r'\d+', var.name.replace('q_', ''))
                    sol_q[int(index[0]), int(index[1])] = var.varValue
            # logging.info("\n\tof: {}\n\tsol:\n{} \n\ttime:{}".format(of, sol_x, comp_time))
            logging.info("#########")
        else:
            print("Unfeasible solution")
        return of, sol_x, sol_q, comp_time, flagSolver
