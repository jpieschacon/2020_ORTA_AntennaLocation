# -*- coding: utf-8 -*-
import logging
import numpy as np


class Instance():
    def __init__(self, sim_setting):
        """[summary]
        
        Arguments:
            sim_setting {[type]} -- [description]
        """
        logging.info("starting simulation...")
        self.ar = sim_setting['antenna_row']
        self.ac = sim_setting['antenna_column']
        self.Q = sim_setting['max_capacity'] * np.ones((sim_setting['antenna_row'], sim_setting['antenna_column']))
        self.R = np.around(np.random.uniform(
            sim_setting['min_demand'],
            sim_setting['max_demand'],
            (sim_setting['antenna_row'] - 1) * (sim_setting['antenna_column'] - 1)
        ))
        self.R = np.reshape(self.R, [(sim_setting['antenna_row'] - 1), (sim_setting['antenna_column'] - 1)])
        self.C = np.around(np.random.uniform(
            sim_setting['min_cost'],
            sim_setting['max_cost'],
            sim_setting['antenna_row'] * sim_setting['antenna_column']
        ))
        self.C = np.reshape(self.C, [(sim_setting['antenna_row']), (sim_setting['antenna_column'])])
        # self.profits = np.around(np.random.uniform(
        #     sim_setting['low_profit'],
        #     sim_setting['high_profit'],
        #     sim_setting['n_items']
        # ))
        # self.n_items = sim_setting['n_items']
        logging.info("simulation end")

    def get_data(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """
        logging.info("getting data from instance...")
        return {
            "demand": self.R,
            "capacity": self.Q,
            "cost": self.C,
            "antennaRow": self.ar,
            "antennaColumn": self.ac
        }
