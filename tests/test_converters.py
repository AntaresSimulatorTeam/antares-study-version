import typing as t

import pytest

from antares.study.version.converters import (
    AnyVersionType,
    version_int_to_triplet,
    version_str_to_triplet,
    version_to_triplet,
)


@pytest.mark.parametrize(
    "version, expected",
    [
        (962, (9, 6, 2)),
        (1970, (19, 7, 0)),
        (9, (9, 0, 0)),
        (0, (0, 0, 0)),
        pytest.param(-9, (0, 0, 0), marks=pytest.mark.xfail(raises=ValueError, strict=True)),
    ],
)
def test_version_int_to_triplet(version: int, expected: tuple[int, int, int]) -> None:
    actual = version_int_to_triplet(version)
    assert actual == expected


@pytest.mark.parametrize(
    "version, expected",
    [
        ("962", (9, 6, 2)),
        ("9.6.2", (9, 6, 2)),
        ("9.6", (9, 6, 0)),
        ("9", (9, 0, 0)),
        pytest.param("9.6.2.5", (0, 0, 0), marks=pytest.mark.xfail(raises=ValueError, strict=True)),
        pytest.param("first.second", (0, 0, 0), marks=pytest.mark.xfail(raises=ValueError, strict=True)),
        pytest.param("", (0, 0, 0), marks=pytest.mark.xfail(raises=ValueError, strict=True)),
    ],
)
def test_version_str_to_triplet(version: str, expected: tuple[int, int, int]) -> None:
    actual = version_str_to_triplet(version)
    assert actual == expected


@pytest.mark.parametrize(
    "version, expected",
    [
        (962, (9, 6, 2)),
        ("962", (9, 6, 2)),
        ((9, 6, 2), (9, 6, 2)),
        ((9, 6), (9, 6, 0)),
        ((9,), (9, 0, 0)),
        ([9, 6, 2], (9, 6, 2)),
        ([9, 6], (9, 6, 0)),
        ([9], (9, 0, 0)),
        ({"major": 9}, (9, 0, 0)),
        ({"major": 9, "minor": "6"}, (9, 6, 0)),
        ({"major": 9, "minor": "6", "patch": True}, (9, 6, 1)),
        pytest.param({9, 6, 2}, (0, 0, 0), marks=pytest.mark.xfail(raises=TypeError, strict=True)),
        pytest.param(9.6, (0, 0, 0), marks=pytest.mark.xfail(raises=TypeError, strict=True)),
        pytest.param([], (0, 0, 0), marks=pytest.mark.xfail(raises=ValueError, strict=True)),
        pytest.param([9, 6, 2, 5], (0, 0, 0), marks=pytest.mark.xfail(raises=ValueError, strict=True)),
        pytest.param(["foo", "bar"], (0, 0, 0), marks=pytest.mark.xfail(raises=ValueError, strict=True)),
        pytest.param({"foo": 5, "bar": 6}, (0, 0, 0), marks=pytest.mark.xfail(raises=ValueError, strict=True)),
    ],
)
def test_version_to_triplet(version: AnyVersionType, expected: tuple[int, int, int]) -> None:
    actual = version_to_triplet(version)
    assert actual == expected
