# -*- coding: utf-8 -*-
import time
import math
import logging
import numpy as np
from pulp import *

class SimpleHeu():
    def __init__(self, n):
        self.n = n

    def solve(
        self, dict_data , problem_instances, N_iter=10
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
        
        c=problem_instances['c']
        Q=problem_instances['Q']
        R=problem_instances['R']
        cost=sum(sum(c))
        sol_x = np.zeros((dict_data['antennaRow'], dict_data['antennaColumn']))
        sol_q = np.zeros((dict_data['antennaRow'], dict_data['antennaColumn']))
        start = time.time()    
        for sol_iter in range(N_iter):
            x=problem_instances['x']
            z=problem_instances['z']
            q=problem_instances['q']
            q_NW=problem_instances['q_NW']
            q_NE=problem_instances['q_NE']
            q_SW=problem_instances['q_SW']
            q_SE=problem_instances['q_SE']
            prob=problem_instances['prob']
            x_sol=np.random.choice([0,1],size=(dict_data['antennaRow'],dict_data['antennaColumn']),p=[1/3,2/3])
            
            for i in range(dict_data['antennaRow']):
                for j in range(dict_data['antennaColumn']):
                    x[i,j].varValue=x_sol[i,j]
                  
            for m in range(dict_data['antennaRow']-1):
                for n in range(dict_data['antennaColumn']-1):
                    ant_N=x[m,n].varValue+x[m+1,n].varValue+x[m,n+1].varValue+x[m+1,n+1].varValue
                    q_SE[m,n].varValue=0
                    q_SW[m,n+1].varValue=0
                    q_NE[m+1,n].varValue=0
                    q_NW[m+1,n+1].varValue=0
                    for k in range(5):
                        z[m,n,k].varValue=0
                        if k==ant_N:
                            z[m,n,k].varValue=1
                            if k!=0:
                                q_SE[m,n].varValue=(R[m,n]*x[m,n].varValue)/k
                                q_SW[m,n+1].varValue=(R[m,n]*x[m,n+1].varValue)/k
                                q_NE[m+1,n].varValue=(R[m,n]*x[m+1,n].varValue)/k
                                q_NW[m+1,n+1].varValue=(R[m,n]*x[m+1,n+1].varValue)/k
                                
            for i in range(dict_data['antennaRow']):
                for j in range(dict_data['antennaColumn']):
                    q[i,j].varValue=q_SE[i,j].varValue+q_SW[i,j].varValue+q_NE[i,j].varValue+q_NW[i,j].varValue
            # Validate constraints
            feasible=True
            prob.constraints.update()
            for key in prob.constraints.keys():
                if not(prob.constraints[key].valid(eps=1e-8)):
                    print(prob.constraints[key])
                    feasible=False
                    print('Unfeasible solution')
                    break
            if feasible:
                if cost>prob.objective.value():
                    cost=prob.objective.value()
                    for indx in x:
                        sol_x[indx[0],indx[1]]=x[indx[0],indx[1]].varValue
                    for indq in q:
                        sol_q[indq[0],indq[1]]=q[indq[0],indq[1]].varValue
                    
                
        
        end = time.time()
        
        
        comp_time = end - start
        
        return cost, sol_x, sol_q, comp_time
