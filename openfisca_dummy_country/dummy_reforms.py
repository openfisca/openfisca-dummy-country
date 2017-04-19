# -*- coding: utf-8 -*-

from openfisca_core.model_api import *


class neutralization_rsa(Reform):
    def apply(self):
        self.neutralize_variable('rsa')



class salaire_net(Variable):
    definition_period = MONTH

    def function(individu, period):
        salaire_brut = individu('salaire_brut', period)

        return salaire_brut


class remove_social_cotisations(Reform):
    def apply(self):
        self.update_variable(salaire_net)
