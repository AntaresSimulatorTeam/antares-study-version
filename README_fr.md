# Study Version Manager

[![PyPI - Version](https://img.shields.io/pypi/v/antares-study-version.svg)](https://pypi.org/project/antares-study-version)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/antares-study-version.svg)](https://pypi.org/project/antares-study-version)

![antares-study-version-title](docs/assets/antares-study-version-title.jpeg)

English version: [README.md](README.md)

Le package `antares-study-version` est à la fois une bibliothèque et une application en ligne de commande
pour gérer les versions des études brutes d’Antares (études sur disque).

La bibliothèque dispose de deux classes, `StudyVersion` et `SolverVersion`, qui sont utilisées
pour gérer les numéros de version des études (et du solveur).
Elle fournit une API pour créer de nouvelles études dans une version donnée et pour mettre à jour
les versions des études existantes.

L’application CLI `antares-study-version` vous permet de créer et de mettre à jour des études sur disque.
Il s’agit d’un utilitaire pratique pour les utilisateurs qui souhaitent maintenir leurs études Antares à jour
et profiter des dernières fonctionnalités du solveur Antares.
Cet utilitaire est également utile pour les développeurs qui souhaitent mettre à jour les études de test.

-----

**Table of Contents**

- [overview](docs/overview.md)
- [installation](docs/installation.md)
- [usage](docs/usage.md)
- [development](docs/development.md)
- [Changelog](docs/CHANGELOG.md)
- [LICENSE](LICENSE.md)
