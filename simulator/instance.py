# -*- coding: utf-8 -*-
import logging
import numpy as np


class Instance:
    def __init__(self, sim_setting):
        """[summary]
        
        Arguments:
            sim_setting {[type]} -- [description]
        """
        logging.info("starting simulation...")
        distribution = sim_setting['distribution']
        self.ar = sim_setting['antenna_row']
        self.ac = sim_setting['antenna_column']
        self.Q = None
        self.R = None
        self.C = None
        self.min_cap = sim_setting['min_capacity']
        self.max_cap = sim_setting['max_capacity']
        self.min_demand = sim_setting['min_demand']
        self.max_demand = sim_setting['max_demand']
        self.max_cost = sim_setting['max_cost']
        self.min_cost = sim_setting['min_cost']
        if distribution in 'uniform':
            self.distribution_uniform()
        elif distribution in 'normal':
            self.distribution_gauss()
        elif distribution in 'realistic':
            self.realistic()
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

    def distribution_uniform(self):
        self.Q = np.around(np.random.uniform(
            self.min_cap,
            self.max_cap,
            (self.ar, self.ac)
        ))
        self.R = np.around(np.random.uniform(
            self.min_demand,
            self.max_demand,
            ((self.ar - 1), (self.ac - 1))
        ))
        self.C = np.around(np.random.uniform(
            self.min_cost,
            self.max_cost,
            (self.ar, self.ac)
        ))

    def distribution_gauss(self):
        self.Q = abs(np.around(np.random.normal(
            (self.max_cap+self.min_cap)/2,
            self.max_cap-self.min_cap,
            (self.ar, self.ac)
        )))
        self.R = abs(np.around(np.random.normal(
            (self.max_demand+self.min_demand)/2,
            self.max_demand-self.min_demand,
            ((self.ar - 1), (self.ac - 1))
        )))
        self.C = abs(np.around(np.random.normal(
            (self.max_cost+self.min_cost)/2,
            self.max_cost-self.min_cost,
            (self.ar, self.ac)
        )))

    def realistic(self):
        self.Q = abs(np.around(np.random.normal(
            (self.max_cap + self.min_cap) / 2,
            self.max_cap - self.min_cap,
            (self.ar, self.ac)
        )))

        self.C = np.interp(self.Q, [np.min(self.Q), np.max(self.Q)], [self.min_cost, self.max_cost])

        self.R = np.around(np.random.exponential(
            (2*self.max_demand)/3,
            ((self.ar - 1), (self.ac - 1))
        ))
