Changelog
=========

v1.0.12 (2025-03-12)
-------------------

## What's Changed
* fix(resources): remove usage of importlib.resources by @MartinBelthle in https://github.com/AntaresSimulatorTeam/antares-study-version/pull/27
* build: remove usage of hatch by @MartinBelthle in https://github.com/AntaresSimulatorTeam/antares-study-version/pull/28
* Fix pyproject.toml by @flomnes in https://github.com/AntaresSimulatorTeam/antares-study-version/pull/29
* Handle 9.2 version by @payetvin in https://github.com/AntaresSimulatorTeam/antares-study-version/pull/26
* chore(study_templates): update default values of study templates by @maugde in https://github.com/AntaresSimulatorTeam/antares-study-version/pull/30

## New Contributors
* @payetvin made their first contribution in https://github.com/AntaresSimulatorTeam/antares-study-version/pull/26
* @maugde made their first contribution in https://github.com/AntaresSimulatorTeam/antares-study-version/pull/30

**Full Changelog**: https://github.com/AntaresSimulatorTeam/antares-study-version/compare/v1.0.11...v1.0.12

v1.0.10 (2024-10-25)
-------------------

- migrate cluster group from "other" to "other 1" inside v8.1 upgrader

v1.0.9 (2024-10-16)
-------------------

- add a function identifying upgrade temporary directories for AntaresWeb

v1.0.8 (2024-10-15)
-------------------

- Implement upgrade for StudyVersion 9.2

v1.0.7 (2024-10-08)
-------------------

- introduce a new class `SolverMinorVersion` for antares-launcher.

v1.0.6 (2024-09-25)
-------------------

- revert change in release v1.0.5 as it was a mistake
- v8.6 update puts field `enable-first-step` at False instead of True

v1.0.5 (2024-09-25)
-------------------

- str(TripletVersion) now returns XYZ instead of X.Y.Z to make serialization work inside AntaresWeb


v1.0.4 (2024-09-24)
-------------------

- Add missing operators inside TripletVersion class
- Explicitly export StudyVersion and SolverVersion to avoid mypy issues
- Implement upgrade for StudyVersion 9.0


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

