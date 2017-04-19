#! /usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name = 'OpenFisca-Dummy-Country',
    version = '0.2.0',
    author = 'OpenFisca Team',
    author_email = 'contact@openfisca.fr',
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Information Analysis",
        ],
    description = u'Dummy tax and benefit system used for tests',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url = 'https://github.com/openfisca/openfisca-dummy-country',
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'OpenFisca-Core >= 10.0, < 11.0',
        ],
    packages = find_packages(),
    test_suite = 'nose.collector',
    dependency_links = ['git+https://github.com/openfisca/openfisca-core.git@remove-fuzzy#egg=OpenFisca-Core-10'],
    )
