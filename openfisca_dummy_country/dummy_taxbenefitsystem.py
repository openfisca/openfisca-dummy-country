# -*- coding: utf-8 -*-

import pkg_resources
import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from entities import entities
from scenarios import Scenario

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
path_to_model_dir = os.path.join(COUNTRY_DIR, 'model')
path_to_root_params = os.path.join(COUNTRY_DIR, 'parameters', 'param_root.xml')
path_to_crds_params = os.path.join(COUNTRY_DIR, 'parameters', 'param_more.xml')


class DummyTaxBenefitSystem(TaxBenefitSystem):
    def __init__(self):
        TaxBenefitSystem.__init__(self, entities)
        self.Scenario = Scenario
        self.add_legislation_params(path_to_root_params)
        self.add_legislation_params(path_to_crds_params, 'csg.activite')
        self.add_variables_from_directory(path_to_model_dir)
