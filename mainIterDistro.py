#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import numpy as np
from simulator.instance import Instance
from solver.antennaLocation import AntennaLocation
from tqdm import tqdm

if __name__ == '__main__':
    # Parameters
    time_limit = 2*60*60  # maximum execution time in seconds
    output_file = "./results/exp_general_table_distros.csv"  # output file
    distros = ['uniform', 'normal', 'realistic']
    seeds_number = 10  # Number of seeds
    row_min = 3  # Minimum number of rows
    row_max = 10  # Maximum number of rows

    log_name = "./logs/main.log"
    logging.basicConfig(filename=log_name, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt="%H:%M:%S", filemode='w')
    fp = open("./etc/config.json", 'r')
    sim_setting = json.load(fp)
    fp.close()

    for seed in tqdm(range(seeds_number)):
        for row in tqdm(range(row_min, row_max)):
            for distro in distros:
                np.random.seed(seed)
                sim_setting['antenna_row'] = row
                sim_setting['antenna_column'] = row
                sim_setting['distribution'] = distro

                inst = Instance(sim_setting)
                dict_data = inst.get_data()

                prb = AntennaLocation(dict_data)

                # Solver
                of_exact, sol_exact, sol_q, comp_time_exact, flagSolver = prb.solve(dict_data, verbose=False, time_limit=time_limit)

                file_output = open(output_file, "a")
                file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']}, {sim_setting['max_capacity']}, {sim_setting['min_capacity']}, {sim_setting['max_demand']}, {sim_setting['min_demand']}, {sim_setting['max_cost']}, {sim_setting['min_cost']},{'solver'},{distro},{comp_time_exact},{of_exact},{flagSolver}\n")
                file_output.close()