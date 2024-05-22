# Study Version Manager

[![PyPI - Version](https://img.shields.io/pypi/v/antares-study-version.svg)](https://pypi.org/project/antares-study-version)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/antares-study-version.svg)](https://pypi.org/project/antares-study-version)

![antares-study-version-title](docs/assets/antares-study-version-title.jpeg)

Version française : [README_fr.md](README_fr.md)

The `antares-study-version` package is both a library and a command line application
for managing versions of raw Antares studies (on disk studies).

The library has two classes, `StudyVersion` and `SolverVersion`, which are used to manage
the study (and solver) version numbers.
It provides an API for creating new studies in a given version and for upgrading versions of existing studies.

The `antares-study-version` command line application allows you to create and upgrade study versions on disk.
This is a handy utility for users who wish to keep their Antares studies up-to-date and to take advantage
of the latest Antares Solver features.
This utility is also useful for developers who wish to update test studies.

-----

**Table of Contents**

- [overview](docs/overview.md)
- [installation](docs/installation.md)
- [usage](docs/usage.md)
- [development](docs/development.md)
- [Changelog](docs/CHANGELOG.md)
- [LICENSE](LICENSE.md)
