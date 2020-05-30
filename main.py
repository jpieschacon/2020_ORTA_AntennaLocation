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

    
    of_exact, sol_exact, sol_q, comp_time_exact, flagSolver = prb.solve(
        dict_data,
        verbose=True
    )

    grid = Graph(inst, sol_exact, sol_q)
    grid.plot()
    print(of_exact, comp_time_exact)
   
    heu = SimpleHeu(prb, dict_data)
    of_heu, sol_heux, sol_heuq, comp_time_heu = heu.solveRandom(1000)

    grid = Graph(inst, sol_heux, sol_heuq)
    grid.plot()
    print(of_heu, comp_time_heu)

    of_heu, sol_heux, sol_heuq, comp_time_heu = heu.solveRandomPDF(1000)

    grid = Graph(inst, sol_heux, sol_heuq)
    grid.plot()
    print(of_heu, comp_time_heu)
    
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
