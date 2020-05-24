# -*- coding: utf-8 -*-
import time
import logging
from pulp import *


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
            "x", ((i,j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat="Binary"
        )
        
        q = LpVariable.dicts(
            "q", ((i,j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )
        
        q_NW = LpVariable.dicts(
            "q", ((i,j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )
        q_NE = LpVariable.dicts(
            "q", ((i,j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )
        
        q_SW = LpVariable.dicts(
            "q", ((i,j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )
        
        q_SE = LpVariable.dicts(
            "q", ((i,j) for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])),
            lowBound=0,
            cat=LpContinuous
        )
        
 
        
        z = LpVariable.dicts(
            "z", ((m,n,k) for m in range(dict_data['antennaRow']) for n in range(dict_data['antennaColumn']) for k in range(5)),
            lowBound=0,
            cat="Binary"
        )
        # LpContinuous
        R = dict_data['demand']
        c = dict_data['cost']
        Q = dict_data['capacity']

        problem_name = "antennalocation"

        prob = LpProblem(problem_name, LpMinimize)
        prob += lpSum([c[i,j] * x[i,j] for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])]) , "obj_func"
        prob += lpSum([z[m,n,k] for m in range(dict_data['antennaRow']-1) for n in range(dict_data['antennaColumn']-1) for k in range(5)]) == 1 , "2"
        prob += [4 - lpSum([x[i, j]] for i in [m, m+1] for j in [n, n+1]) for m in range(dict_data['antennaRow']-1) for n in range(dict_data['antennaColumn']-1)] == [lpSum([(4-k)*z[m,n,k] for k in range(5)])for m in range(dict_data['antennaRow']-1) for n in range(dict_data['antennaColumn']-1)], "3"
        prob += [q_NE[m,n]*k-R[m,n]*x[m,n] for m in range(dict_data['antennaRow']-1) for n in range(dict_data['antennaColumn']-1) for k in range(5)] <= [(1-z[m,n,k])*Q[m,n] for m in range(dict_data['antennaRow']-1) for n in range(dict_data['antennaColumn']-1) for k in range(5)],"4"
        prob += [q_NW[m,n+1]*k-R[m,n]*x[m,n+1] for m in range(dict_data['antennaRow']-1) for n in range(dict_data['antennaColumn']-1) for k in range(5)] <= [(1-z[m,n,k])*Q[m,n+1] for m in range(dict_data['antennaRow']-1) for n in range(dict_data['antennaColumn']-1) for k in range(5)],"5"
        prob += [q_SE[m+1,n]*k-R[m,n]*x[m+1,n] for m in range(dict_data['antennaRow']-1) for n in range(dict_data['antennaColumn']-1) for k in range(5)] <= [(1-z[m,n,k])*Q[m+1,n] for m in range(dict_data['antennaRow']-1) for n in range(dict_data['antennaColumn']-1) for k in range(5)],"6"
        prob += [q_SW[m+1,n+1]*k-R[m,n]*x[m+1,n+1] for m in range(dict_data['antennaRow']-1) for n in range(dict_data['antennaColumn']-1) for k in range(5)] <= [(1-z[m,n,k])*Q[m+1,n+1] for m in range(dict_data['antennaRow']-1) for n in range(dict_data['antennaColumn']-1) for k in range(5)],"7"
        prob += [q[i,j] for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])] == [q_NW[i,j]+q_NE[i,j]+q_SW[i,j]+q_SE[i,j] for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])],"8"
        prob += [q[i,j] for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])] <= [Q[i,j] * x[i,j] for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])],"9"
        # prob += lpSum([dict_data['sizes'][i] * x[i] for i in items]) <= dict_data['max_size'], "max_vol"
        # prob += lpSum([dict_data['sizes'][i] * x[i] for i in items]) <= dict_data['max_size'], "max_vol"

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

        # sol_x = [0] * dict_data['n_items']
        # for var in sol:
        #     logging.info("{} {}".format(var.name, var.varValue))
        #     if "X_" in var.name:
        #         sol_x[int(var.name.replace("X_", ""))] = abs(var.varValue)
        # logging.info("\n\tof: {}\n\tsol:\n{} \n\ttime:{}".format(
        #     of, sol_x, comp_time)
        # )
        logging.info("#########")
        return of, sol, comp_time
