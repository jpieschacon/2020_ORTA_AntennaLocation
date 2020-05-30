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

    def solve(self, N_iter, method='random'):
        cost = self.costMax
        start = time.time()
        sol_x = np.ones((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        sol_q = np.zeros((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        param1 = None
        if method == 'PDF':
            totalProbability = self.defineProbabilities()  # generate probability for each antenna
            param1 = totalProbability
        countFeasible = 0
        countUnfeasible = 0
        for sol_iter in range(N_iter):
            newSol = self.newSol(method, param1)
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

    def newSol(self, method, param1):
        if method == 'random':
            newSol = np.random.choice([0, 1], size=(self.dict_data['antennaRow'], self.dict_data['antennaColumn']), p=[1 / 3, 2 / 3])
        elif method == 'PDF':
            newSol = np.zeros((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
            for i in range(self.dict_data['antennaRow']):
                for j in range(self.dict_data['antennaColumn']):
                    newSol[i, j] = np.random.choice([0, 1], p=[1-param1[i, j], param1[i, j]])
        elif method == '12N':
            pass
        else:
            newSol = np.ones((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        return newSol


    def defineProbabilities(self):
        R0 = np.zeros((self.dict_data['antennaRow'] + 1, self.dict_data['antennaColumn'] + 1))  # Demand matrix, zeros in borders
        R0[1:self.dict_data['antennaRow'], 1:self.dict_data['antennaColumn']] = self.prb.R  # R in the center

        cost0 = np.zeros((self.dict_data['antennaRow'] + 2, self.dict_data['antennaColumn'] + 2))  # Cost matrix, zeros in borders
        cost0[1:self.dict_data['antennaRow'] + 1, 1:self.dict_data['antennaColumn'] + 1] = self.prb.c

        probabilityDemand = np.zeros((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        probabilityCostSquare = np.zeros((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        for i in range(self.dict_data['antennaRow']):
            for j in range(self.dict_data['antennaColumn']):
                probabilityDemand[i, j] = sum(sum(R0[i:i + 2, j:j + 2]))  # sum 4 nearest demands
                probabilityCostSquare[i, j] = sum(sum(cost0[i:i + 3, j:j + 3])) - self.prb.c[i, j]  # sum costs for antennas around antenna i,j
        probabilityDemand = probabilityDemand / np.max(probabilityDemand)  # normalize probabilities
        probabilityCost = 1 - self.prb.c / np.max(self.prb.c)  # assign probability 0 to most expensive antenna
        probabilityCost = 1 - np.max(probabilityCost) + probabilityCost  # sum the difference to avoid 0 probability
        probabilityCostSquare = 1 - probabilityCostSquare / np.max(probabilityCostSquare)
        probabilityCostSquare = 1 - np.max(probabilityCostSquare) + probabilityCostSquare  # sum the difference to avoid 0 probability
        totalProbability = probabilityCostSquare * probabilityDemand * probabilityCost
        totalProbability = np.interp(totalProbability, [np.min(totalProbability), np.max(totalProbability)], [0.2, 0.8])
        return totalProbability

    def solveRandomPDF(self, N_iter):
        cost = self.costMax
        start = time.time()
        sol_x = np.ones((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        sol_q = np.zeros((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        countFeasible = 0
        countUnfeasible = 0
        totalProbability = self.defineProbabilities()  # generate probability for each antenna
        for sol_iter in range(N_iter):
            newSol = np.zeros((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
            for i in range(self.dict_data['antennaRow']):
                for j in range(self.dict_data['antennaColumn']):
                    newSol[i, j] = np.random.choice([0, 1], p=[1-totalProbability[i, j], totalProbability[i, j]])
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




    def solveRandom(self, N_iter):
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
