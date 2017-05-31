# -*- coding: utf-8 -*-

import datetime

import numpy as np
from numpy.core.defchararray import startswith

from openfisca_core.model_api import *

from openfisca_dummy_country.entities import Famille, Individu


class af(Variable):
    column = FloatCol
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period


class age_en_mois(Variable):
    column = IntCol
    entity = Individu
    label = u"Âge (en nombre de mois)"
    definition_period = MONTH


class birth(Variable):
    column = DateCol
    entity = Individu
    label = u"Date de naissance"
    definition_period = ETERNITY
    url = "https://fr.wikipedia.org/wiki/Date_de_naissance"


class city_code(Variable):
    column = FixedStrCol(max_length = 5)
    entity = Famille
    label = u"""Code INSEE de la commune de résidence de la famille"""
    definition_period = ETERNITY


class salaire_brut(Variable):
    column = FloatCol
    entity = Individu
    label = "Salaire brut"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class a_charge_fiscale(Variable):
    column = BoolCol
    entity = Individu
    label = u"La personne n'est pas fiscalement indépendante"
    definition_period = MONTH


# Calculated variables

class age(Variable):
    column = IntCol
    entity = Individu
    label = u"Âge (en nombre d'années)"
    definition_period = MONTH

    def formula(self, simulation, period):
        birth = simulation.get_array('birth', period)
        if birth is None:
            age_en_mois = simulation.get_array('age_en_mois', period)
            if age_en_mois is not None:
                return age_en_mois // 12
            birth = simulation.calculate('birth', period)
        return (np.datetime64(period.date) - birth).astype('timedelta64[Y]')


class dom_tom(Variable):
    column = BoolCol
    entity = Famille
    label = u"La famille habite-t-elle les DOM-TOM ?"
    definition_period = YEAR

    def formula(famille, period):
        city_code = famille('city_code', period)

        return np.logical_or(startswith(city_code, '97'), startswith(city_code, '98'))


class revenu_disponible(Variable):
    column = FloatCol
    entity = Individu
    label = u"Revenu disponible de l'individu"
    definition_period = YEAR

    def formula(individu, period, legislation):
        rsa = individu('rsa', period, options = [ADD])
        salaire_imposable = individu('salaire_imposable', period)
        taux = legislation(period).impot.taux

        return rsa + salaire_imposable * (1 - taux)


class revenu_disponible_famille(Variable):
    column = FloatCol
    entity = Famille
    label = u"Revenu disponible de la famille"
    definition_period = YEAR

    def formula(famille, period):
        revenu_disponible = famille.members('revenu_disponible', period)
        return famille.sum(revenu_disponible)


class rsa(Variable):
    column = FloatCol
    entity = Individu
    label = u"RSA"
    definition_period = MONTH

    def formula_2010_01_01(individu, period):
        salaire_imposable = individu('salaire_imposable', period, options = [DIVIDE])

        return (salaire_imposable < 500) * 100.0

    def formula_2011_01_01(individu, period):
        salaire_imposable = individu('salaire_imposable', period, options = [DIVIDE])

        return (salaire_imposable < 500) * 200.0

    def formula_2013_01_01(individu, period):
        salaire_imposable = individu('salaire_imposable', period, options = [DIVIDE])

        return (salaire_imposable < 500) * 300.0


class rmi(Variable):
    column = FloatCol
    entity = Individu
    label = u"RMI (remplacé par le RSA en 2010)"
    definition_period = MONTH
    end = '2009-12-31'

    def formula_2000_01_01(individu, period):
        salaire_imposable = individu('salaire_imposable', period, options = [DIVIDE])

        return (salaire_imposable == 0) * 400


class salaire_imposable(Variable):
    column = FloatCol
    entity = Individu
    label = u"Salaire imposable"
    definition_period = YEAR

    def formula(individu, period):
        dom_tom = individu.famille('dom_tom', period)

        salaire_net = individu('salaire_net', period, options=[ADD])

        return salaire_net * 0.9 - 100 * dom_tom


class salaire_net(Variable):
    column = FloatCol
    entity = Individu
    label = u"Salaire net"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula(individu, period):
        salaire_brut = individu('salaire_brut', period)

        return salaire_brut * 0.8


class contribution_sociale(Variable):
    column = FloatCol
    entity = Individu
    label = u"Contribution payée sur le salaire"
    definition_period = YEAR

    def formula_1880_01_01(individu, period, legislation):
        salaire_brut = individu('salaire_brut', period, options=[ADD])
        bareme = legislation(period).contribution_sociale.salaire.bareme

        return bareme.calc(salaire_brut)

    def formula(individu, period, legislation):  # function_avant_1880
        salaire_brut = individu('salaire_brut', period, options=[ADD])

        return salaire_brut * 0.05


# start_date is deprecated, we now prefer functions start.
# However it needs to be tested
class fixed_tax(Variable):
    column = FloatCol
    entity = Individu
    label = u"Former tax used to be paid by every adult"
    definition_period = YEAR
    # start_date = date(1980, 1, 1)
    end = '1989-12-31'

    def formula_1980(individu, period, legislation):
        return individu('age') >= 18 * 400


class api(Variable):
    column = FloatCol
    entity = Famille
    label = u"Allocation pour Parent Isolé"
    definition_period = MONTH
    # start_date = date(2000, 1, 1)
    end = '2009-12-31'

    def formula_2005_01_01(famille, period):
        nb_parents = famille.nb_persons(role = famille.PARENT)
        nb_enfants = famille.nb_persons(role = famille.ENFANT)
        condition = (nb_parents == 1) * (nb_enfants > 0)

        return condition * 200

    def formula_2000_01_01(famille, period):
        nb_parents = famille.nb_persons(role = famille.PARENT)
        nb_enfants = famille.nb_persons(role = famille.ENFANT)
        condition = (nb_parents == 1) * (nb_enfants > 0)

        return condition * 100
