#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import numpy as np
from simulator.instance import Instance
from solver.antennaLocation import AntennaLocation
from heuristic.simpleHeu import SimpleHeu
from tqdm import tqdm

if __name__ == '__main__':
    # Parameters
    iter_number = 1000  # Max number of iteration for each heuristic algorithm
    output_file = "./results/exp_general_table_iter_8.csv"  # output file
    seeds_number = 10  # Number of seeds
    iterations = [5, 10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]  # Number of iterations

    log_name = "./logs/main.log"
    logging.basicConfig(filename=log_name, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt="%H:%M:%S", filemode='w')

    fp = open("./etc/config.json", 'r')
    sim_setting = json.load(fp)
    fp.close()
    
    np.random.seed(0)
    
    inst = Instance(sim_setting)
    dict_data = inst.get_data()

    prb = AntennaLocation(dict_data)

    # Solver
    of_exact, sol_exact, sol_q, comp_time_exact, flagSolver = prb.solve(dict_data, verbose=False)

    for seed in tqdm(range(seeds_number)):
        np.random.seed(seed)
        for itervalue in iterations:
            
            heu = SimpleHeu(prb, dict_data)
            iter_number = itervalue

            # Ramdom
            of_heu_random, sol_x_random, sol_q_random, comp_time_heu_random = heu.solveRandom(iter_number)

            # PDFT1
            of_heu_pdf, sol_x_PDFT1, sol_q_PDFT1, comp_time_heu_pdf = heu.solveRandomPDF(iter_number, 1)

            # PDFT2
            of_heu_bic, sol_x_PDFT2, sol_q_PDFT2, comp_time_heu_bic = heu.solveRandomPDF(iter_number, 2)

            # # From max number of antennas to 1 antenna heuristic
            of_heu_N21, sol_x_N21, sol_q_N21, comp_time_heu_N21, uninstalled_ant = heu.solve_N21(iter_number)

            # From 1 antenna  to max number of antennas
            of_heu_12N, sol_x_12N, sol_q_12N, comp_time_heu_12N, min_ant_num = heu.solve_12N(iter_number)

            # printing results of a file
            file_output = open(output_file, "a")
            file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'solver'},{-1},{comp_time_exact},{of_exact}\n")
            file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'random'},{iter_number},{comp_time_heu_random},{of_heu_random}\n")
            file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'PDF'},{iter_number},{comp_time_heu_pdf},{of_heu_pdf}\n")
            file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'BIC'},{iter_number},{comp_time_heu_bic},{of_heu_bic}\n")
            file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'N21'},{iter_number},{comp_time_heu_N21},{of_heu_N21}\n")
            file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'12N'},{iter_number},{comp_time_heu_12N},{of_heu_12N}\n")
            file_output.close()