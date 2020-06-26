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
    time_limit = 60 * 60  # maximum execution time in seconds
    iter_number = 1000  # Max number of iteration for each heuristic algorithm
    output_file = "./results/exp_general_table.csv"  # output file
    seeds_number = 10  # Number of seeds
    row_min = 3  # Minimum number of rows
    row_max = 10  # Maximum number of rows
    column_min = 3  # Minimum number of columns
    column_max = 10  # Maximum number of columns

    log_name = "./logs/main.log"
    logging.basicConfig(filename=log_name, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt="%H:%M:%S", filemode='w')

    fp = open("./etc/config.json", 'r')
    sim_setting = json.load(fp)
    fp.close()

    for seed in tqdm(range(seeds_number)):
        for row in tqdm(range(row_min, row_max)):
            for column in tqdm(range(column_min, column_max)):
                np.random.seed(seed)
                sim_setting['antenna_row'] = row
                sim_setting['antenna_column'] = column

                inst = Instance(sim_setting)
                dict_data = inst.get_data()

                prb = AntennaLocation(dict_data)

                # Solver
                of_exact, sol_exact, sol_q, comp_time_exact, flagSolver = prb.solve(dict_data, verbose=False, time_limit=time_limit)

                heu = SimpleHeu(prb, dict_data)

                # Random
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
                file_output = open("./results/exp_general_table.csv", "a")
                file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'solver'},{-1},{comp_time_exact},{of_exact}\n")
                file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'random'},{iter_number},{comp_time_heu_random},{of_heu_random}\n")
                file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'PDF'},{iter_number},{comp_time_heu_pdf},{of_heu_pdf}\n")
                file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'BIC'},{iter_number},{comp_time_heu_bic},{of_heu_bic}\n")
                file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'N21'},{iter_number},{comp_time_heu_N21},{of_heu_N21}\n")
                file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'12N'},{iter_number},{comp_time_heu_12N},{of_heu_12N}\n")
                file_output.close()