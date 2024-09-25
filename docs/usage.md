# Usage

This package provides a `StudyVersion` class to manage study version numbers,
and a `SolverVersion` class to manage Antares Solver version numbers.

The difference between `StudyVersion` and `SolverVersion` is that Solver versions are generally on 3 digits
(with the `major`, `minor` and `patch` components), while study versions are on 2 digits
(with the `major` and `minor` components only), and the `patch` component is not used (always 0).

## StudyVersion

Using the `antares-study-version` module is straightforward:

```python
from antares.study.version import StudyVersion

version = StudyVersion(8, 7, 2)  # patch component is not used
print(version)  # 870
```

You can also create a version object from a dotted string:

```python
from antares.study.version import StudyVersion

version = StudyVersion.parse("8.7")
print(version)  # 870
```

You can create a version object from a compact string:

```python
from antares.study.version import StudyVersion

version = StudyVersion.parse("870")
print(version)  # 870
```

You can create a version object from an integer:

```python
from antares.study.version import StudyVersion

version = StudyVersion.parse(870)
print(version)  # 870
```

You can compare versions:

```python
from antares.study.version import StudyVersion

version1 = StudyVersion(8, 6)
version2 = StudyVersion(8, 7)
print(version1 < version2)  # True
```

You can convert a version to string using format specifiers:

```python
from antares.study.version import StudyVersion

version = StudyVersion(8, 7)
print(f"{version}d.d.d")  # 8.7
print(f"{version:02d}")  # 08.07
print(f"{version:03d}")  # 08.07.00
print(version)  # 870
```

You can convert a version to an integer:

```python
from antares.study.version import StudyVersion

version = StudyVersion(8, 7)
print(int(version))  # 870
```

## SolverVersion

Of course, the same operations can be done with `SolverVersion` objects, but with 3 digits:

```python
from antares.study.version import SolverVersion

version = SolverVersion(8, 7, 2)
print(version)  # 872
```

Objects of the `StudyVersion` and `SolverVersion` classes can be compared to each other:

```python
from antares.study.version import StudyVersion, SolverVersion

study_version = StudyVersion(8, 7)
solver_version = SolverVersion(8, 7, 2)
print(study_version <= solver_version)  # True
```

## Pydantic model

You can even use the `StudyVersion` or `SolverVersion` classes in a Pydantic model:

```python
import datetime
import typing as t
import uuid

from pydantic import BaseModel, Field, validator

from antares.study.version import StudyVersion


class StudyDTO(BaseModel):
    id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
    name: str
    version: StudyVersion
    created: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc))

    @validator("version", pre=True)
    def _validate_version(cls, v: t.Any) -> StudyVersion:
        return StudyVersion.parse(v)


study = StudyDTO(name="foo", version=StudyVersion(4, 5))
obj = study.json()
print(obj)
# {
#     "created": "2024-12-31T12:30:00+00:00",
#     "id": "4930a577-63d2-4ea9-b0b9-581110d97475",
#     "name": "foo",
#     "version": {"major": 4, "minor": 5, "patch": 0}
# }
```
