# -*- coding: utf-8 -*-
import time
import numpy as np
from copy import deepcopy


class SimpleHeu:
    def __init__(self, prb, dict_data):
        self.prb = prb
        self.dict_data = dict_data
        self.costMax = sum(sum(prb.c))

    def defineProbabilities(self, prob_type):
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
        if prob_type == 1:
            probabilityCost = 1 - np.max(probabilityCost) + probabilityCost  # sum the difference to avoid 0 probability
            probabilityCostSquare = 1 - probabilityCostSquare / np.max(probabilityCostSquare)
            probabilityCostSquare = 1 - np.max(probabilityCostSquare) + probabilityCostSquare  # sum the difference to avoid 0 probability
            totalProbability = probabilityCostSquare * probabilityDemand * probabilityCost
            totalProbability = np.interp(totalProbability, [np.min(totalProbability), np.max(totalProbability)], [0.2, 0.8])
        elif prob_type == 2:
            totalProbability = probabilityDemand * probabilityCost
        else:
            totalProbability = 0
        return totalProbability

    def solveRandomPDF(self, N_iter, prob_type):
        cost = self.costMax
        start = time.time()
        sol_x = np.ones((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        sol_q = np.zeros((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        countFeasible = 0
        countUnfeasible = 0
        feasibleDaR = 0
        unfeasibleDaR = 0
        totalProbability = self.defineProbabilities(prob_type)  # generate probability for each antenna
        for sol_iter in range(N_iter):
            newSol = np.zeros((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
            for i in range(self.dict_data['antennaRow']):
                for j in range(self.dict_data['antennaColumn']):
                    newSol[i, j] = np.random.choice([0, 1], p=[1 - totalProbability[i, j], totalProbability[i, j]])
            feasible, sol_x, sol_q, cost, constraint = self.validateFeasibility(newSol, sol_x, sol_q, cost)
            if feasible:
                countFeasible += 1
            else:
                countUnfeasible += 1
                feasible, sol_x, sol_q, cost, constraint, nF, nU = self.destroyAndRebuild(newSol, sol_x, sol_q, cost, constraint)
                feasibleDaR += nF
                unfeasibleDaR += nU

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
        feasibleDaR = 0
        unfeasibleDaR = 0
        for sol_iter in range(N_iter):
            newSol = np.random.choice([0, 1], size=(self.dict_data['antennaRow'], self.dict_data['antennaColumn']), p=[1 / 3, 2 / 3])
            feasible, sol_x, sol_q, cost, constraint = self.validateFeasibility(newSol, sol_x, sol_q, cost)
            if feasible:
                countFeasible += 1
            else:
                countUnfeasible += 1
                feasible, sol_x, sol_q, cost, constraint, nF, nU = self.destroyAndRebuild(newSol, sol_x, sol_q, cost, constraint)
                feasibleDaR += nF
                unfeasibleDaR += nU
        end = time.time()
        comp_time = end - start
        # print(countFeasible, countUnfeasible)
        return cost, sol_x, sol_q, comp_time

    def solve_N21(self, N_iter=10):
        cost = self.costMax
        start = time.time()
        sol_x = np.ones((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        sol_q = np.zeros((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        max_ant_number = self.dict_data['antennaRow'] * self.dict_data['antennaColumn']
        countFeasible_N = np.zeros(max_ant_number)
        countUnfeasible_N = np.zeros(max_ant_number)
        for quantity_zeros in range(max_ant_number):
            sol_x_aux = np.ones(self.dict_data['antennaRow'] * self.dict_data[
                'antennaColumn'])  # Initialize here so that the zeros do not overwrite the ones
            sol_x_aux[:quantity_zeros] = 0
            newSol = sol_x_aux.reshape((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
            for sol_iter in range(N_iter):  # Try several times with the same number of zeros (The instance may repeat for small instances)
                np.random.shuffle(newSol)
                feasible, opt_sol_x, sol_q, cost, constraint = self.validateFeasibility(newSol, sol_x, sol_q, cost)
                if feasible:
                    countFeasible_N[quantity_zeros] += 1
                else:
                    countUnfeasible_N[quantity_zeros] += 1

            if countFeasible_N[quantity_zeros] == 0 and countUnfeasible_N[quantity_zeros] == N_iter:
                uninstalled_ant = quantity_zeros - 1
                # There are no more feasible solutions for lesser amount of installed antennas
                # (Valid only if the number of iterations N_iter is much bigger than the instance
                # this way we are checking every combination of non installed antennas (if instance not repeated))
                break
        end = time.time()
        comp_time = end - start
        # print(countFeasible_N, countUnfeasible_N)
        return cost, opt_sol_x, sol_q, comp_time, uninstalled_ant

    def solve_12N(self, N_iter):
        cost = self.costMax
        start = time.time()
        sol_x = np.ones((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        sol_q = np.zeros((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
        max_ant_number = self.dict_data['antennaRow'] * self.dict_data['antennaColumn']
        countFeasible_N = np.zeros(max_ant_number)
        countUnfeasible_N = np.zeros(max_ant_number)
        min_ant_number = 1
        for ant_number in range(1, max_ant_number):
            sol_x_aux = np.zeros(self.dict_data['antennaRow'] * self.dict_data['antennaColumn'])
            random_ant = np.random.randint(self.dict_data['antennaRow'] * self.dict_data['antennaColumn'], size=ant_number)
            sol_x_aux[random_ant] = 1
            newSol = sol_x_aux.reshape((self.dict_data['antennaRow'], self.dict_data['antennaColumn']))
            for sol_iter in range(N_iter):
                feasible, opt_sol_x, sol_q, cost, constraint = self.validateFeasibility(newSol, sol_x, sol_q, cost)
                np.random.shuffle(newSol)
                if feasible:
                    countFeasible_N[ant_number - 1] += 1
                else:
                    countUnfeasible_N[ant_number - 1] += 1
            if countFeasible_N[ant_number - 1] == 0 and countUnfeasible_N[ant_number - 1] == N_iter and not (countFeasible_N.any() == 1):
                min_ant_number = ant_number + 1
        end = time.time()
        comp_time = end - start
        return cost, sol_x, sol_q, comp_time, min_ant_number

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
                return feasible, sol_x, sol_q, cost, key

        if feasible:
            if cost > prob.objective.value():
                cost = prob.objective.value()
                for indX in x:
                    sol_x[indX[0], indX[1]] = x[indX[0], indX[1]].varValue
                for indQ in q:
                    sol_q[indQ[0], indQ[1]] = q[indQ[0], indQ[1]].varValue

            return feasible, sol_x, sol_q, cost, key

    def destroyAndRebuild(self, newSol, sol_x, sol_q, cost, constraint):
        nF = 0
        nU = 0

        if len(constraint.split('_')) == 3:
            nConst, nRow, nCol = [int(x) for x in constraint.split('_')]
        elif len(constraint.split('_')) == 4:
            nConst, nRow, nCol, k = [int(x) for x in constraint.split('_')]
        for i in range(5):
            if nConst == 8:  # constraint 8
                table = []
                for m in range(nRow, nRow + 2):
                    for n in range(nCol, nCol + 2):
                        if newSol[m, n] == 0:
                            table.append([m, n, self.prb.c[m, n], self.prb.Q[m, n] - sol_q[m, n]])
                table = np.array(table, dtype=int)
                if len(table) == 0:
                    feasible, opt_sol_x, sol_q, cost, constraint = self.validateFeasibility(newSol, sol_x, sol_q, cost)
                table = table[np.lexsort((table[:, 3], table[:, 2]))]
                newSol[table[0][0], table[0][1]] = 1  # add lowest cost antenna
            elif nConst == 10:
                # cellsR = np.zeros((2, 2))
                R0 = np.zeros((self.dict_data['antennaRow'] + 1, self.dict_data['antennaColumn'] + 1))  # Demand matrix, zeros in borders
                R0[1:self.dict_data['antennaRow'], 1:self.dict_data['antennaColumn']] = deepcopy(self.prb.R)  # R in the center
                cellsR = R0[nRow:nRow + 2, nCol:nCol + 2]
                notFull = 0
                while notFull < 4:
                    ind = np.unravel_index(np.argmax(cellsR, axis=None), cellsR.shape)
                    nRowAux = ind[0]-1+nRow
                    nColAux = ind[1]-1+nCol
                    if sum(sum(newSol[nRowAux:nRowAux+2, nColAux:nColAux+2])) == 4:
                        cellsR[ind[0], ind[1]] = 0
                        notFull += 1
                    else:
                        notFull = 4
                        nRow = nRowAux
                        nCol = nColAux
                table = []
                for m in range(nRow, nRow + 2):
                    for n in range(nCol, nCol + 2):
                        if newSol[m, n] == 0:
                            table.append([m, n, self.prb.c[m, n], self.prb.Q[m, n] - sol_q[m, n]])
                table = np.array(table, dtype=int)
                table = table[np.lexsort((table[:, 3], table[:, 2]))]
                newSol[table[0][0], table[0][1]] = 1  # add lowest cost antenna
            else:
                pass
            feasible, opt_sol_x, sol_q, cost, constraint = self.validateFeasibility(newSol, sol_x, sol_q, cost)
            if feasible:
                nF += 1
                break
            else:
                nU += 1

            if len(constraint.split('_')) == 3:
                nConst, nRow, nCol = [int(x) for x in constraint.split('_')]
            elif len(constraint.split('_')) == 4:
                nConst, nRow, nCol, k = [int(x) for x in constraint.split('_')]

        return feasible, sol_x, sol_q, cost, constraint, nF, nU
