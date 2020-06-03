#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import numpy as np
from simulator.instance import Instance
from solver.antennaLocation import AntennaLocation
from heuristic.simpleHeu import SimpleHeu
from graph.graph import Graph

np.random.seed(0)

if __name__ == '__main__':
    log_name = "./logs/main.log"
    logging.basicConfig(
        filename=log_name,
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO, datefmt="%H:%M:%S",
        filemode='w'
    )

    fp = open("./etc/config.json", 'r')
    sim_setting = json.load(fp)
    fp.close()

    inst = Instance(
        sim_setting
    )
    dict_data = inst.get_data()

    prb = AntennaLocation(dict_data)

    # Solver
    of_exact, sol_exact, sol_q, comp_time_exact, flagSolver = prb.solve(
        dict_data,
        verbose=True
    )

    grid = Graph(inst, sol_exact, sol_q)
    grid.plot('Solver')
    print(of_exact, comp_time_exact)
   
    heu = SimpleHeu(prb, dict_data)
    
    # Ramdom
    of_heu, sol_heux, sol_heuq, comp_time_heu = heu.solveRandom(1000)

    grid = Graph(inst, sol_heux, sol_heuq)
    grid.plot('Random heuristic')
    print(of_heu, comp_time_heu)

    # PDF
    of_heu, sol_heux, sol_heuq, comp_time_heu = heu.solveRandomPDF(3000,1)

    grid = Graph(inst, sol_heux, sol_heuq)
    grid.plot('Random PDF heuristic')
    print(of_heu, comp_time_heu)
    
    # Beginning in the center
    of_heu, sol_heux, sol_heuq, comp_time_heu = heu.solveRandomPDF(3000,2)

    grid = Graph(inst, sol_heux, sol_heuq)
    grid.plot('Random BIC heuristic')
    print(of_heu, comp_time_heu)
    
    # From max number of antennas to 1 antenna heuristic
    of_heu1, sol_heux1, sol_heuq1, comp_time_heu1, uninstalled_ant = heu.solve_N21(1000)

    grid = Graph(inst, sol_heux1, sol_heuq1)
    grid.plot('Random N-to-1 heuristic')
    print(of_heu1, comp_time_heu1, uninstalled_ant)
    
    # From 1 antenna  to max number of antennas
    of_heu2, sol_heux2, sol_heuq2, comp_time_heu2 = heu.solve_12N(1000)

    grid = Graph(inst, sol_heux2, sol_heuq2)
    grid.plot('Random 1-to-N heuristic')
    print(of_heu2, comp_time_heu2)
    
    # print(of_heu, sol_heu, comp_time_heu)

    # # printing results of a file
    # file_output = open(
    #     "./results/exp_general_table.csv",
    #     "w"
    # )
    # file_output.write("method, of, sol, time\n")
    # file_output.write("{}, {}, {}, {}\n".format(
    #     "heu", of_heu, sol_heu, comp_time_heu
    # ))
    # file_output.write("{}, {}, {}, {}\n".format(
    #     "exact", of_exact, sol_exact, comp_time_exact
    # ))
    # file_output.close()
