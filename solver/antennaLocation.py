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
        
        q_NW= LpVariable('q_NW',lowBound = 0, cat='Continuous')
        q_NE= LpVariable('q_NE',lowBound = 0, cat='Continuous')
        q_SW= LpVariable('q_SW',lowBound = 0, cat='Continuous')
        q_SE= LpVariable('q_SE',lowBound = 0, cat='Continuous')
        
        z = LpVariable.dicts(
            "z", ((m,n,k) for m in range(dict_data['antennaRow']) for n in range(dict_data['antennaColumn']) for k in range(5)),
            lowBound=0,
            cat="Binary"
        )
        # LpContinuous

        problem_name = "antennalocation"

        prob = LpProblem(problem_name, LpMinimize)
        prob += lpSum([dict_data['cost'][i,j] * x[i,j] for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])]) , "obj_func"
        prob += [q[i,j] for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])] == q_NW+q_NE+q_SW+q_SE,"max_vol"
        prob += [q[i,j] for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])] <= [dict_data['capacity'][i,j] * x[i,j] for i in range(dict_data['antennaRow']) for j in range(dict_data['antennaColumn'])]
        # prob += lpSum([dict_data['sizes'][i] * x[i] for i in items]) <= dict_data['max_size'], "max_vol"
        # prob += lpSum([dict_data['sizes'][i] * x[i] for i in items]) <= dict_data['max_size'], "max_vol"

        # prob.writeLP("./logs/{}.lp".format(problem_name))

        # msg_val = 1 if verbose else 0
        # start = time.time()
        # solver = COIN_CMD(
        #     msg=msg_val,
        #     maxSeconds=time_limit,
        #     fracGap=gap
        # )
        # solver.solve(prob)
        # end = time.time()
        # logging.info("\t Status: {}".format(LpStatus[prob.status]))

        # sol = prob.variables()
        # of = value(prob.objective)
        # comp_time = end - start

        # sol_x = [0] * dict_data['n_items']
        # for var in sol:
        #     logging.info("{} {}".format(var.name, var.varValue))
        #     if "X_" in var.name:
        #         sol_x[int(var.name.replace("X_", ""))] = abs(var.varValue)
        # logging.info("\n\tof: {}\n\tsol:\n{} \n\ttime:{}".format(
        #     of, sol_x, comp_time)
        # )
        logging.info("#########")
        # return of, sol_x, comp_time
