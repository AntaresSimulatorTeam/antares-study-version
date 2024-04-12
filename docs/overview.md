# Overview

The `antares-study-version` package defines `StudyVersion` and `SolverVersion` classes to manage version numbers.
It can be used to manage the version of a study, but also the version
of [Antares Solver](https://github.com/AntaresSimulatorTeam/Antares_Simulator).
It supports the [semver](https://semver.org/) format ("major.minor.patch") and the integer format
(major×100 + minor×10 + patch), which is specific to Antares.

This module harmonizes the management of versions in Antares:

- at the level of Antares studies (configuration files, database, etc.)
- at the level of Antares applications, in particular [AntaREST](https://github.com/AntaresSimulatorTeam/AntaREST/).

In the data of a study and in the programs, we encounter several version formats:

- dotted string (ex. `"8.7"` or `"8.7.2"`),
- compact string (ex. `"870"`),
- integer (ex. `870`).
- tuples or lists (ex. `(8, 7)` or `[8, 7, 2]`).
- dictionaries (ex. `{"major": 8, "minor": 7, "patch": 2}`).

For instance, since
[version 9.0](https://antares-simulator.readthedocs.io/en/latest/reference-guide/13-file-format/#v900)
of Antares Solver, versions are stored as dotted strings;
the compact format is now obsolete (backward compatibility is ensured for versions prior to 9.0);

For instance, the `study.antares` configuration file now uses the "X.Y" format for the study version instead
of the "XYZ" format.

```ini
[antares]
version = 9.1
caption = My Study
created = 1618413128
lastsave = 1625583204
author = John DOE
```

This module allows to convert these formats to each other, and to compare versions.
