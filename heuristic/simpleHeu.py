# -*- coding: utf-8 -*-
import time
import math
import logging
import numpy as np
from pulp import *


class SimpleHeu():
    def __init__(self, prb, dict_data):
        self.prb = prb
        self.dict_data = dict_data
        self.costMax = sum(sum(prb.c))

    def solveRandom(self, N_iter=10):
        cost = self.costMax
        start = time.time()
        sol_x = np.ones((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        sol_q = np.zeros((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        countFeasible = 0
        countUnfeasible = 0
        for sol_iter in range(N_iter):
            newSol = np.random.choice([0, 1], size=(self.dict_data['antennaRow'], self.dict_data['antennaColumn']), p=[1 / 3, 2 / 3])
            feasible, sol_x, sol_q, cost = self.validateFeasibility(newSol, sol_x, sol_q, cost)
            if feasible:
                countFeasible += 1
            else:
                countUnfeasible += 1
                # TODO implement destroy and rebuild
        end = time.time()
        comp_time = end - start
        # print(countFeasible, countUnfeasible)
        return cost, sol_x, sol_q, comp_time

    def solve_N21(self, N_iter=10):
        cost = self.costMax
        start = time.time()
        sol_x = np.ones((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        sol_q = np.zeros((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        max_ant_number = self.dict_data['antennaRow']*self.dict_data['antennaColumn']
        countFeasible_N = np.zeros(max_ant_number)
        countUnfeasible_N = np.zeros(max_ant_number)
        for quantity_zeros in range(max_ant_number):
            sol_x_aux = np.ones(self.dict_data['antennaRow'] * self.dict_data[
                'antennaColumn'])  # Initialize here so that the zeros do not overwrite the ones
            sol_x_aux[:quantity_zeros] = 0
            newSol = sol_x_aux.reshape((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
            for sol_iter in range(N_iter): # Try several times with the same number of zeros (The instance may repeat for small instances)
                np.random.shuffle(newSol)
                feasible, opt_sol_x, sol_q, cost = self.validateFeasibility(newSol, sol_x, sol_q, cost)
                if feasible:
                    countFeasible_N[quantity_zeros] += 1
                else:
                    countUnfeasible_N[quantity_zeros] += 1
        end = time.time()
        comp_time = end - start
        print(countFeasible_N, countUnfeasible_N)
        return cost, opt_sol_x, sol_q, comp_time

    def validateFeasibility(self, newSol, sol_x, sol_q, cost):
        c = self.prb.c
        Q = self.prb.Q
        R = self.prb.R
        x = self.prb.x
        z = self.prb.z
        q = self.prb.q
        q_NW = self.prb.q_NW
        q_NE = self.prb.q_NE
        q_SW = self.prb.q_SW
        q_SE = self.prb.q_SE
        prob = self.prb.prob

        for i in range(self.dict_data['antennaRow']):
            for j in range(self.dict_data['antennaColumn']):
                x[i, j].varValue = newSol[i, j]
                q_SE[i, j].varValue = 0
                q_SW[i, j].varValue = 0
                q_NE[i, j].varValue = 0
                q_NW[i, j].varValue = 0

        for m in range(self.dict_data['antennaRow'] - 1):
            for n in range(self.dict_data['antennaColumn'] - 1):
                ant_N = x[m, n].varValue + x[m + 1, n].varValue + x[m, n + 1].varValue + x[m + 1, n + 1].varValue
                for k in range(5):
                    z[m, n, k].varValue = 0
                    if k == ant_N:
                        z[m, n, k].varValue = 1
                        if k != 0:
                            q_SE[m, n].varValue = (R[m, n] * x[m, n].varValue) / k
                            q_SW[m, n + 1].varValue = (R[m, n] * x[m, n + 1].varValue) / k
                            q_NE[m + 1, n].varValue = (R[m, n] * x[m + 1, n].varValue) / k
                            q_NW[m + 1, n + 1].varValue = (R[m, n] * x[m + 1, n + 1].varValue) / k

        for i in range(self.dict_data['antennaRow']):
            for j in range(self.dict_data['antennaColumn']):
                q[i, j].varValue = q_SE[i, j].varValue + q_SW[i, j].varValue + q_NE[i, j].varValue + q_NW[i, j].varValue
        # Validate constraints
        feasible = True
        prob.constraints.update()
        for key in prob.constraints.keys():
            if not (prob.constraints[key].valid(eps=1e-8)):
                # print(prob.constraints[key])
                feasible = False
                # print('Unfeasible solution')
                break

        if feasible:
            if cost > prob.objective.value():
                cost = prob.objective.value()
                for indX in x:
                    sol_x[indX[0], indX[1]] = x[indX[0], indX[1]].varValue
                for indQ in q:
                    sol_q[indQ[0], indQ[1]] = q[indQ[0], indQ[1]].varValue

        return feasible, sol_x, sol_q, cost
