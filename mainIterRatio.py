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
    log_name = "./logs/main.log"
    logging.basicConfig(
        filename=log_name,
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO, datefmt="%H:%M:%S",
        filemode='w'
    )
    distros = ['uniform', 'normal', 'realistic']
    fp = open("./etc/config.json", 'r')
    sim_setting = json.load(fp)
    fp.close()

    for row in tqdm(range(6, 7)):
        print(f"####{row}#############")
        for seed in range(2, 10):
            for demand in range(int(1.5*sim_setting['max_capacity'])):

                np.random.seed(seed)
                sim_setting['max_demand'] = demand+1
                sim_setting['min_demand'] = demand+1
                sim_setting['antenna_row'] = row
                sim_setting['antenna_column'] = row

                inst = Instance(
                    sim_setting, 'uniform'
                )
                dict_data = inst.get_data()

                prb = AntennaLocation(dict_data)

                # Solver
                of_exact, sol_exact, sol_q, comp_time_exact, flagSolver = prb.solve(dict_data, verbose=False)

                file_output = open(f"./results/exp_general_table_ratio_NxN.csv", "a")
                file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{sim_setting['max_capacity']},{sim_setting['min_capacity']},{sim_setting['max_demand']},{sim_setting['min_demand']},{sim_setting['max_cost']},{sim_setting['min_cost']},{'solver'},{sim_setting['max_demand']/sim_setting['max_capacity']},{comp_time_exact},{of_exact},{flagSolver}\n")
                file_output.close()