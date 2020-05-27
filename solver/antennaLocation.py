# -*- coding: utf-8 -*-
import time
import logging
import numpy as np
from pulp import *
import re


class AntennaLocation():
    def __init__(self):
        pass

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
        logging.info("#########")
        # items = range(dict_data['n_items'])

        x = LpVariable.dicts(
            "x", ((i, j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat="Binary"
        )

        q = LpVariable.dicts(
            "q", ((i, j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )

        q_NW = LpVariable.dicts(
            "q_NW", ((i, j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )
        q_NE = LpVariable.dicts(
            "q_NE", ((i, j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )

        q_SW = LpVariable.dicts(
            "q_SW", ((i, j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )

        q_SE = LpVariable.dicts(
            "q_SE", ((i, j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )

        z = LpVariable.dicts(
            "z", ((m, n, k) for m in range(dict_data['antennaRow'] - 1) for n in range(dict_data['antennaColumn'] - 1) for k in range(5)),
            lowBound=0,
            cat="Binary"
        )
        # LpContinuous
        R = dict_data['demand']
        c = dict_data['cost']
        Q = dict_data['capacity']

        problem_name = "antennalocation"

        prob = LpProblem(problem_name, LpMinimize)
        prob += lpSum([c[i, j] * x[i, j] for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])]), "obj_func"
        for m in range(dict_data['antennaRow'] - 1):
            for n in range(dict_data['antennaColumn'] - 1):
                prob += lpSum(z[m, n, k] for k in range(5)) == 1, f"2_{m}_{n}"
                prob += 4 - lpSum([x[i, j]] for i in [m, m + 1] for j in [n, n + 1]) == lpSum([(4 - k) * z[m, n, k] for k in range(5)]), f"3_{m}_{n}"
                for k in range(5):
                    prob += q_SE[m, n] * k - R[m, n] * x[m, n] <= (1 - z[m, n, k]) * Q[m, n], f"4_{m}_{n}_{k}"
                    prob += q_SW[m, n + 1] * k - R[m, n] * x[m, n + 1] <= (1 - z[m, n, k]) * Q[m, n + 1], f"5_{m}_{n}_{k}"
                    prob += q_NE[m + 1, n] * k - R[m, n] * x[m + 1, n] <= (1 - z[m, n, k]) * Q[m + 1, n], f"6_{m}_{n}_{k}"
                    prob += q_NW[m + 1, n + 1] * k - R[m, n] * x[m + 1, n + 1] <= (1 - z[m, n, k]) * Q[m + 1, n + 1], f"7_{m}_{n}_{k}"
                prob += q_SE[m, n] + q_SW[m, n + 1] + q_NE[m + 1, n] + q_NW[m + 1, n + 1] == R[m, n], f"lina_{m}_{n}"
        for i in range(dict_data['antennaRow']):
            for j in range(dict_data['antennaColumn']):
                prob += q[i, j] == q_NW[i, j] + q_NE[i, j] + q_SW[i, j] + q_SE[i, j], f"8_{i}_{j}"
                prob += q[i, j] <= Q[i, j] * x[i, j], f"9_{i}_{j}"

        prob.writeLP("./logs/{}.lp".format(problem_name))

        msg_val = 1 if verbose else 0
        start = time.time()
        solver = COIN_CMD(
            msg=msg_val,
            maxSeconds=time_limit,
            fracGap=gap
        )
        solver.solve(prob)
        end = time.time()
        logging.info("\t Status: {}".format(LpStatus[prob.status]))

        sol = prob.variables()
        of = value(prob.objective)
        comp_time = end - start

        sol_x = np.zeros((dict_data['antennaRow'], dict_data['antennaColumn']))
        sol_q = np.zeros((dict_data['antennaRow'], dict_data['antennaColumn']))

        for var in sol:
            logging.info("{} {}".format(var.name, var.varValue))
            if var.varValue != 0:
                print(var.name, "\t", var.varValue)
            if "x_" in var.name:
                index = re.findall(r'\d+', var.name.replace('x_', ''))
                sol_x[int(index[0]), int(index[1])] = var.varValue
            elif "q_(" in var.name:
                index = re.findall(r'\d+', var.name.replace('q_', ''))
                sol_q[int(index[0]), int(index[1])] = var.varValue
        # logging.info("\n\tof: {}\n\tsol:\n{} \n\ttime:{}".format(of, sol_x, comp_time))
        logging.info("#########")
        return of, sol_x, sol_q, comp_time
