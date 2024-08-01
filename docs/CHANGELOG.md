Changelog
=========

v1.0.3 (2024-07-31)
-------------------

- Minor code improvements
- Allow upgrade with empty fields inside `study.antares` file.
- Add `py.typed` file to avoid mypy issue in projects importing the code


v1.0.0 (2024-07-06)
-------------------

### Features

This version allows to manage the versions of Antares raw studies (studies on disk).

It contains a command line application to create a new raw study in the version of your choice,
and to update an existing raw study to a newer version.

The new CLI also allows to display the details of a raw study and to list the available versions.
Run the following command to get more information:

```bash
antares-study-version --help
```


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

