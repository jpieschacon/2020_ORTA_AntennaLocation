#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import numpy as np
from simulator.instance import Instance
from solver.antennaLocation import AntennaLocation
from heuristic.simpleHeu import SimpleHeu
from tqdm import tqdm
from graph.graph import Graph


if __name__ == '__main__':
    # Parameters
    time_limit = 60 * 60  # maximum execution time in seconds
    output_file = "./results/exp_general_table_iter_same_solver6_v5.csv"  # output file
    seeds_number = 30  # Number of seeds
    iterNumber = 100

    log_name = "./logs/main.log"
    logging.basicConfig(filename=log_name, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt="%H:%M:%S", filemode='w')

    fp = open("./etc/config.json", 'r')
    sim_setting = json.load(fp)
    fp.close()
    
    for itervalue in tqdm(range(iterNumber)):
        for seed in tqdm(range(seeds_number)):
            np.random.seed(seed)
    
            inst = Instance(sim_setting)
            dict_data = inst.get_data()
        
            prb = AntennaLocation(dict_data)
        
            # Solver
            of_exact, sol_exact, sol_q, comp_time_exact, flagSolver = prb.solve(dict_data, verbose=False, time_limit=time_limit)

            # # printing results of a file
            file_output = open(output_file, "a")
            file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'solver'},{itervalue},{comp_time_exact},{of_exact},{flagSolver}\n")
            file_output.close()
