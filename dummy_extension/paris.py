# -*- coding: utf-8 -*-

from openfisca_core.model_api import *

from openfisca_dummy_country.entities import Famille


class paris_logement_familles(Variable):
    column = FloatCol
    label = u"Allocation Paris Logement Famille"
    entity = Famille
    definition_period = MONTH

    def function(famille, period):
        condition = round_(famille('city_code', period).astype(int) / 1000) == 75
        return condition * 100
