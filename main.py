#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import numpy as np
from simulator.instance import Instance
from solver.antennaLocation import AntennaLocation
from heuristic.simpleHeu import SimpleHeu
from graph.graph import Graph

seed = 1
np.random.seed(seed)

if __name__ == '__main__':
    # Parameters
    time_limit = 60*60  # maximum execution time in seconds
    iter_number = 1000  # Max number of iteration for each heuristic algorithm
    output_file = "./results/exp_general_table.csv"  # output file

    log_name = "./logs/main.log"
    logging.basicConfig(filename=log_name, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt="%H:%M:%S", filemode='w')
    fp = open("./etc/config.json", 'r')
    sim_setting = json.load(fp)
    fp.close()

    inst = Instance(sim_setting)
    dict_data = inst.get_data()

    prb = AntennaLocation(dict_data)

    # Solver
    of_exact, sol_exact, sol_q, comp_time_exact, flagSolver = prb.solve(dict_data, verbose=True, time_limit=time_limit)

    grid = Graph(inst, sol_exact, sol_q)
    grid.plot('Solver')
    print(of_exact, comp_time_exact)

    heu = SimpleHeu(prb, dict_data)

    # Random
    of_heu_random, sol_x_random, sol_q_random, comp_time_heu_random = heu.solveRandom(iter_number)

    grid = Graph(inst, sol_x_random, sol_q_random)
    grid.plot('Random heuristic')
    print(of_heu_random, comp_time_heu_random)

    # PDFT1
    of_heu_pdf, sol_x_PDFT1, sol_q_PDFT1, comp_time_heu_pdf = heu.solveRandomPDF(iter_number, 1)

    grid = Graph(inst, sol_x_PDFT1, sol_q_PDFT1)
    grid.plot('PDFT1 heuristic')
    print(of_heu_pdf, comp_time_heu_pdf)

    # PDFT2
    of_heu_bic, sol_x_PDFT2, sol_q_PDFT2, comp_time_heu_bic = heu.solveRandomPDF(iter_number, 2)

    grid = Graph(inst, sol_x_PDFT2, sol_q_PDFT2)
    grid.plot('PDFT2 heuristic')
    print(of_heu_bic, comp_time_heu_bic)

    # From max number of antennas to 1 antenna heuristic
    of_heu_N21, sol_x_N21, sol_q_N21, comp_time_heu_N21, uninstalled_ant = heu.solve_N21(iter_number)

    grid = Graph(inst, sol_x_N21, sol_q_N21)
    grid.plot('Random N-to-1 heuristic')
    print(of_heu_N21, comp_time_heu_N21, uninstalled_ant)

    # From 1 antenna  to max number of antennas
    of_heu_12N, sol_x_12N, sol_q_12N, comp_time_heu_12N, min_ant_num = heu.solve_12N(iter_number)

    grid = Graph(inst, sol_x_12N, sol_q_12N)
    grid.plot('Random 1-to-N heuristic')
    print(of_heu_12N, comp_time_heu_12N, min_ant_num)

    # printing results of a file
    file_output = open(output_file, "a")
    file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'solver'},{-1},{comp_time_exact},{of_exact}\n")
    file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'random'},{iter_number},{comp_time_heu_random},{of_heu_random}\n")
    file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'PDF'},{iter_number},{comp_time_heu_pdf},{of_heu_pdf}\n")
    file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'BIC'},{iter_number},{comp_time_heu_bic},{of_heu_bic}\n")
    file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'N21'},{iter_number},{comp_time_heu_N21},{of_heu_N21}\n")
    file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'12N'},{iter_number},{comp_time_heu_12N},{of_heu_12N}\n")
    file_output.close()
