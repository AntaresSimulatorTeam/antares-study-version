"""
Antares Study (and Solver) version models.
"""

import typing as t

AnyVersionType = t.Union[int, str, t.Sequence[t.Union[int, str]], t.Mapping[str, t.Union[int, str]]]


def version_int_to_triplet(version: int) -> tuple[int, int, int]:
    if 0 <= version < 100:
        # Consider a major version
        return version, 0, 0
    elif version >= 100:
        # Consider a major.minor.patch version
        major, minor = divmod(version, 100)
        minor, patch = divmod(minor, 10)
        return major, minor, patch
    else:
        raise ValueError("unsupported integer value")


def version_str_to_triplet(version: str) -> tuple[int, int, int]:
    try:
        if version.count(".") == 0:
            return version_int_to_triplet(int(version))
        elif version.count(".") == 1:
            major, minor = version.split(".")
            return int(major), int(minor), 0
        elif version.count(".") == 2:
            major, minor, patch = version.split(".")
            return int(major), int(minor), int(patch)
        else:
            raise ValueError("unsupported string format")
    except ValueError as exc:
        raise ValueError(str(exc)) from None


def version_to_triplet(version: AnyVersionType) -> tuple[int, int, int]:
    """
    Convert a version number to a tuple of three integers.

    :param version: a version number as an integer, a string, a tuple of three integers,
        or a mapping with required keys: "major", "minor", "patch".
    :return: version number as a tuple of three integers.
    """
    try:
        if isinstance(version, int):
            return version_int_to_triplet(version)
        elif isinstance(version, str):
            return version_str_to_triplet(version)
        elif isinstance(version, t.Sequence):
            integers = tuple(int(x) for x in version)
            if not integers:
                raise ValueError("empty version tuple")
            elif len(integers) == 1:
                return integers[0], 0, 0
            elif len(integers) == 2:
                return integers[0], integers[1], 0
            elif len(integers) == 3:
                return integers[0], integers[1], integers[2]
            else:
                raise ValueError("too many integers in version tuple")
        elif isinstance(version, t.Mapping):
            values = {"minor": 0, "patch": 0, **version}
            try:
                return int(values["major"]), int(values["minor"]), int(values["patch"])
            except KeyError as exc:
                raise ValueError(f"missing key '{exc}'") from None
        else:
            raise TypeError(f"Invalid version type: {type(version)!r}")
    except ValueError as exc:
        raise ValueError(f"Invalid version number {version!r}: {exc}") from None
