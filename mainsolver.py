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

    fp = open("./etc/config.json", 'r')
    sim_setting = json.load(fp)
    fp.close()

    for cost in tqdm(range(0, 1000000,1000)):
        for demand in tqdm(range(0, 100)):
            for seed in tqdm(range(0, 10)):
                np.random.seed(seed)
                sim_setting['max_demand'] = demand
                sim_setting['max_demand'] = demand
                sim_setting['max_cost'] = cost
                sim_setting['min_cost'] = cost

                inst = Instance(
                    sim_setting, 'realistic'
                )
                dict_data = inst.get_data()

                prb = AntennaLocation(dict_data)

                # Solver
                of_exact, sol_exact, sol_q, comp_time_exact, flagSolver = prb.solve(dict_data, verbose=False)

                # grid = Graph(inst, sol_exact, sol_q)
                # grid.plot('Solver')
                # print(of_exact, comp_time_exact)

                # heu = SimpleHeu(prb, dict_data)
                # iter_number = 1000

                # # Ramdom
                # of_heu_random, sol_heux, sol_heuq, comp_time_heu_random = heu.solveRandom(iter_number)

                # grid = Graph(inst, sol_heux, sol_heuq)
                # grid.plot('Random heuristic')
                # print(of_heu_random, comp_time_heu_random)

                # # PDF
                # of_heu_pdf, sol_heux, sol_heuq, comp_time_heu_pdf = heu.solveRandomPDF(iter_number, 1)

                # grid = Graph(inst, sol_heux, sol_heuq)
                # grid.plot('Random PDF heuristic')
                # print(of_heu_pdf, comp_time_heu_pdf)

                # # Beginning in the center
                # of_heu_bic, sol_heux, sol_heuq, comp_time_heu_bic = heu.solveRandomPDF(iter_number, 2)

                # grid = Graph(inst, sol_heux, sol_heuq)
                # grid.plot('Random BIC heuristic')
                # print(of_heu_bic, comp_time_heu_bic)

                # # # From max number of antennas to 1 antenna heuristic
                # of_heu_N21, sol_heux1, sol_heuq1, comp_time_heu_N21, uninstalled_ant = heu.solve_N21(iter_number)
                #
                # grid = Graph(inst, sol_heux1, sol_heuq1)
                # grid.plot('Random N-to-1 heuristic')
                # print(of_heu_N21, comp_time_heu_N21, uninstalled_ant)

                # # From 1 antenna  to max number of antennas
                # of_heu_12N, sol_heux2, sol_heuq2, comp_time_heu_12N, min_ant_num = heu.solve_12N(iter_number)

                # grid = Graph(inst, sol_heux2, sol_heuq2)
                # grid.plot('Random 1-to-N heuristic')
                # print(of_heu_12N, comp_time_heu_12N, min_ant_num)

                # printing results of a file
                
                file_output = open("./results/exp_general_table_solver_std.csv", "a")
                file_output.write(f"{seed},{sim_setting['max_demand']},{sim_setting['max_cost']},{'solver'},{-1},{comp_time_exact},{of_exact},{flagSolver}\n")
                # file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'random'},{iter_number},{comp_time_heu_random},{of_heu_random}\n")
                # file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'PDF'},{iter_number},{comp_time_heu_pdf},{of_heu_pdf}\n")
                # file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'BIC'},{iter_number},{comp_time_heu_bic},{of_heu_bic}\n")
                # file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'N21'},{iter_number},{comp_time_heu_N21},{of_heu_N21}\n")
                # file_output.write(f"{seed},{sim_setting['antenna_row']},{sim_setting['antenna_column']},{'12N'},{iter_number},{comp_time_heu_12N},{of_heu_12N}\n")
                file_output.close()