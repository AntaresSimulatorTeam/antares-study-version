Antares Study Version Changelog
===============================

v0.1.1 (2024-04-10)
-------------------

### Fixes

* **model:** avoid deprecation warning about usage of `NotImplemented` in boolean context

### Tests

* replace [pytest-freezegun](https://pypi.org/project/pytest-freezegun/) lib
  by [pytest-freezer](https://pypi.org/project/pytest-freezer/)

### Docs

* `README.md`: update doc, fix typo, add a link to the change log

### Build

* create [CHANGELOG.md](CHANGELOG.md) and update the release date
* add `scripts/update_version.py` script to create or update the changelog

### CI

* add missing dependency [pytest-freezer](https://pypi.org/project/pytest-freezer/) required for type checking
* create the `.github/workflows/python-package.yml` GitHub workflow for code style and typing check

v0.1.0 (2024-03-20)
-------------------

### Features

* First release of the project.

