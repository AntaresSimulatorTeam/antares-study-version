import dataclasses
import datetime
import io
import textwrap
import typing as t
from configparser import RawConfigParser

import pytest

from antares.study.version.model import SolverVersion, StudyVersion


class TestSolverVersion:
    @pytest.mark.parametrize(
        "args, expected",
        [
            pytest.param((4, 5, 6, 7), (4, 5, 6), marks=pytest.mark.xfail(raises=TypeError, strict=True)),
            pytest.param((4, 5, 6), (4, 5, 6)),
            pytest.param((4, 5), (4, 5, 0)),
            pytest.param((4,), (4, 0, 0)),
            pytest.param((), (0, 0, 0), marks=pytest.mark.xfail(raises=TypeError, strict=True)),
            pytest.param(("4", "5", "6"), (4, 5, 6)),
            pytest.param(("4", "5"), (4, 5, 0)),
            pytest.param(("4",), (4, 0, 0)),
        ],
    )
    def test_init(self, args: t.Sequence[t.Union[int, str]], expected: t.Tuple[int, int, int]) -> None:
        version = SolverVersion(*args)
        assert version.major == expected[0]
        assert version.minor == expected[1]
        assert version.patch == expected[2]

    def test___str__(self) -> None:
        version = SolverVersion(4, 5, 6)
        result = version.__str__()
        assert isinstance(result, str)
        assert result == "4.5.6"

    def test___int__(self) -> None:
        version = SolverVersion(4, 5, 6)
        result = version.__int__()
        assert isinstance(result, int)
        assert result == 456

    def test_parse(self) -> None:
        version = SolverVersion.parse(SolverVersion(4, 5, 6))
        assert version.major == 4
        assert version.minor == 5
        assert version.patch == 6

    @pytest.mark.parametrize(
        "format_spec, expected",
        [
            pytest.param("", "4.5.6", id="empty"),
            pytest.param("1d", "4", id="format-1d"),
            pytest.param("2d", "4.5", id="format-2d"),
            pytest.param("3d", "4.5.6", id="format-3d"),
            pytest.param("01d", "04", id="format-01d"),
            pytest.param("02d", "04.05", id="format-02d"),
            pytest.param("03d", "04.05.06", id="format-03d"),
            pytest.param("ddd", "456", id="format-ddd"),
            pytest.param("X", "", marks=pytest.mark.xfail(raises=ValueError, strict=True)),
        ],
    )
    def test___format__(self, format_spec: str, expected: str) -> None:
        version = SolverVersion(4, 5, 6)
        result = version.__format__(format_spec)
        assert isinstance(result, str)
        assert result == expected


class TestStudyVersion:
    @pytest.mark.parametrize(
        "args, expected",
        [
            pytest.param((4, 5, 6, 7), (4, 5), marks=pytest.mark.xfail(raises=TypeError, strict=True)),
            pytest.param((4, 5, 6), (4, 5)),
            pytest.param((4, 5), (4, 5)),
            pytest.param((4, 5, 0), (4, 5)),
            pytest.param((4,), (4, 0)),
            pytest.param((), (0, 0, 0), marks=pytest.mark.xfail(raises=TypeError, strict=True)),
            pytest.param(("4", "5", "6"), (4, 5)),
            pytest.param(("4", "5"), (4, 5)),
            pytest.param(("4",), (4, 0)),
        ],
    )
    def test_init(self, args: t.Sequence[t.Union[int, str]], expected: t.Tuple[int, int, int]) -> None:
        version = StudyVersion(*args)
        assert version.major == expected[0]
        assert version.minor == expected[1]

    def test___str__(self) -> None:
        version = StudyVersion(4, 5)
        result = version.__str__()
        assert isinstance(result, str)
        assert result == "4.5"

    def test___int__(self) -> None:
        version = StudyVersion(4, 5)
        result = version.__int__()
        assert isinstance(result, int)
        assert result == 450

    def test_parse(self) -> None:
        version = StudyVersion.parse(StudyVersion(4, 5))
        assert version.major == 4
        assert version.minor == 5

    @pytest.mark.parametrize(
        "format_spec, expected",
        [
            pytest.param("", "4.5", id="empty"),
            pytest.param("1d", "4", id="format-1d"),
            pytest.param("2d", "4.5", id="format-2d"),
            pytest.param("3d", "4.5.0", id="format-3d"),
            pytest.param("01d", "04", id="format-01d"),
            pytest.param("02d", "04.05", id="format-02d"),
            pytest.param("03d", "04.05.00", id="format-03d"),
            pytest.param("ddd", "450", id="format-ddd"),
            pytest.param("X", "", marks=pytest.mark.xfail(raises=ValueError, strict=True)),
        ],
    )
    def test___format__(self, format_spec: str, expected: str) -> None:
        version = StudyVersion(4, 5)
        result = version.__format__(format_spec)
        assert isinstance(result, str)
        assert result == expected


class TestScenario:
    def test_ini_file(self):
        """
        Read / write version in INI file.
        """

        ini_content = textwrap.dedent(
            """\
            [antares]
            version = 9.1
            caption = My Study
            created = 1618413128
            lastsave = 1625583204
            author = John DOE
            """
        )
        stream = io.StringIO(ini_content)

        config = RawConfigParser()
        config.read_file(stream)

        # We can parse the study version from an INI file
        version = StudyVersion.parse(config["antares"]["version"])
        assert version == StudyVersion(9, 1)

        # We can write the study version to an INI file
        version = StudyVersion(10, 2)
        config["antares"]["version"] = str(version)

        stream.seek(0)
        config.write(stream)
        ini_content = stream.getvalue()
        assert "version = 10.2\n" in ini_content

    def test_version_invalid(self):
        """
        Convert invalid version number
        """

        # We can't construct a version number from an invalid value
        with pytest.raises(ValueError):
            StudyVersion.parse(-1)

        with pytest.raises(ValueError):
            StudyVersion.parse("invalid")

        with pytest.raises(ValueError):
            StudyVersion.parse([])

        with pytest.raises(ValueError):
            StudyVersion.parse([9, 8, 7, 6])

        with pytest.raises(ValueError):
            StudyVersion.parse({"semver": "3.1.2"})

        with pytest.raises(TypeError):
            StudyVersion.parse(8.7)

        with pytest.raises(TypeError):
            StudyVersion.parse({8, 7, 0})

    @pytest.mark.parametrize("other", [8.7, datetime.datetime(2024, 12, 31)])
    def test_invalid_comparison(self, other: t.Any) -> None:
        """
        Compare with invalid version number type
        """

        version = StudyVersion(8, 7)

        # When the other version number is not a valid type, the comparison is NotImplemented
        assert (version == other) is False
        assert (version != other) is True

        # When the other version number is not a valid type, the ordering comparison raises a TypeError
        with pytest.raises(TypeError):
            _ = version < other

        with pytest.raises(TypeError):
            _ = version <= other

        with pytest.raises(TypeError):
            _ = version > other

        with pytest.raises(TypeError):
            _ = version >= other

    # noinspection PyDataclass,PyTypeChecker
    def test_version_int(self):
        """
        Convert version number from/to int and use compare functions
        """

        # We can construct a version number from an integer
        version = StudyVersion.parse(870)
        assert version == StudyVersion(8, 7)

        # We can convert a version number to an integer
        assert int(version) == 870

        # We can compare integer versions using the standard comparison operators
        assert version == 870
        assert version > 860
        assert version < 880
        assert version != 860
        assert version >= 870
        assert version <= 870

        assert 870 == version
        assert 860 < version
        assert 880 > version
        assert 860 != version
        assert 870 <= version
        assert 870 >= version

    # noinspection PyDataclass,PyTypeChecker
    def test_version_str(self):
        """
        Convert version number from/to string and use compare functions
        """

        # We can construct a version number from a string
        version = StudyVersion.parse("8.7")
        assert version == StudyVersion(8, 7)

        # We can convert a version number to a string
        assert str(version) == "8.7"

        # We can compare string versions using the standard comparison operators
        assert version == "8.7"
        assert version > "8.6"
        assert version < "8.8"
        assert version != "8.6"
        assert version >= "8.7"
        assert version <= "8.7"

        assert "8.7" == version
        assert "8.6" < version
        assert "8.8" > version
        assert "8.6" != version
        assert "8.7" <= version
        assert "8.7" >= version

        # We can construct a version number from a string with a single number
        version = StudyVersion.parse("8")
        assert version == StudyVersion(8)
        assert str(version) == "8"

    # noinspection PyDataclass,PyTypeChecker
    def test_version_triplet(self):
        """
        Convert version number from/to triplet and use compare functions
        """

        # We can construct a version number from a triplet
        version = StudyVersion.parse((8, 7))
        assert version == StudyVersion(8, 7)

        # We can convert a version number to a triplet
        assert tuple(version) == (8, 7)

        # We can compare triplet versions using the standard comparison operators
        assert version == (8, 7)
        assert version > (8, 6)
        assert version < (8, 8)
        assert version != (8, 6)
        assert version >= (8, 7)
        assert version <= (8, 7)

        assert (8, 7) == version
        assert (8, 6) < version
        assert (8, 8) > version
        assert (8, 6) != version
        assert (8, 7) <= version
        assert (8, 7) >= version

        # We can construct a version number from a triplet with a single number
        version = StudyVersion.parse((8,))
        assert version == StudyVersion(8)
        assert tuple(version) == (8,)

        # We can construct a Solver version number from a triplet with 3 numbers
        version = SolverVersion.parse((8, 7, 2))
        assert version == SolverVersion(8, 7, 2)
        assert tuple(version) == (8, 7, 2)

    # noinspection PyDataclass,PyTypeChecker
    def test_version_list(self):
        """
        Convert version number from/to list and use compare functions
        """

        # We can construct a version number from a list
        version = StudyVersion.parse([8, 7])
        assert version == StudyVersion(8, 7)

        # We can convert a version number to a list
        assert list(version) == [8, 7]

        # We can compare list versions using the standard comparison operators
        assert version == [8, 7]
        assert version > [8, 6]
        assert version < [8, 8]
        assert version != [8, 6]
        assert version >= [8, 7]
        assert version <= [8, 7]

        assert [8, 7] == version
        assert [8, 6] < version
        assert [8, 8] > version
        assert [8, 6] != version
        assert [8, 7] <= version
        assert [8, 7] >= version

        # We can construct a version number from a list with a single number
        version = StudyVersion.parse([8])
        assert version == StudyVersion(8)
        assert list(version) == [8]

    # noinspection PyDataclass,PyTypeChecker
    def test_version_dict(self):
        """
        Convert version number from/to dict and use compare functions
        """

        # We can construct a version number from a dict
        version = StudyVersion.parse({"major": 8, "minor": 7})
        assert version == StudyVersion(8, 7)

        # We can convert a version number to a dict
        assert dataclasses.asdict(version) == {"major": 8, "minor": 7, "patch": 0}

        # We can compare dict versions using the standard comparison operators
        assert version == {"major": 8, "minor": 7}
        assert version > {"major": 8, "minor": 6}
        assert version < {"major": 8, "minor": 8}
        assert version != {"major": 8, "minor": 6}
        assert version >= {"major": 8, "minor": 7}
        assert version <= {"major": 8, "minor": 7}

        assert {"major": 8, "minor": 7} == version
        assert {"major": 8, "minor": 6} < version
        assert {"major": 8, "minor": 8} > version
        assert {"major": 8, "minor": 6} != version
        assert {"major": 8, "minor": 7} <= version
        assert {"major": 8, "minor": 7} >= version

        # We can construct a version number from a dict with a single number
        version = StudyVersion.parse({"major": 8})
        assert version == StudyVersion(8)
        assert dataclasses.asdict(version) == {"major": 8, "minor": 0, "patch": 0}

    # noinspection PyDataclass,PyTypeChecker
    def test_study_solver_version_comparison(self):
        """
        Compare study and solver versions
        """

        # We can compare study and solver versions using the standard comparison operators
        study_version = StudyVersion(8, 7)

        assert study_version == SolverVersion(8, 7, 0)
        assert study_version > SolverVersion(8, 6, 0)
        assert study_version < SolverVersion(8, 8, 0)
        assert study_version != SolverVersion(8, 7, 1)
        assert study_version >= SolverVersion(8, 7, 0)
        assert study_version <= SolverVersion(8, 7, 0)

        solver_version = SolverVersion(8, 7, 0)

        assert solver_version == StudyVersion(8, 7)
        assert solver_version < StudyVersion(8, 8)
        assert solver_version > StudyVersion(8, 6)
        assert solver_version != StudyVersion(8, 8)
        assert solver_version <= StudyVersion(8, 7)
        assert solver_version >= StudyVersion(8, 7)

    @pytest.mark.parametrize(
        "versions",
        [
            pytest.param(
                [
                    StudyVersion(8, 7),
                    StudyVersion(8, 6),
                    StudyVersion(8, 8),
                    StudyVersion(9, 0),
                    StudyVersion(7, 0),
                ],
                id="study-versions",
            ),
            pytest.param(
                [
                    SolverVersion(8, 7, 0),
                    SolverVersion(8, 6, 0),
                    SolverVersion(8, 8, 0),
                    SolverVersion(9, 0, 0),
                    SolverVersion(7, 0, 0),
                    SolverVersion(8, 6, 2),
                ],
                id="solver-versions",
            ),
        ],
    )
    def test_sort_min_max(self, versions: t.Sequence[t.Union[StudyVersion, SolverVersion]]) -> None:
        """
        Sort versions
        """
        # We can sort versions using the standard sort function
        actual = sorted(versions)
        expected = sorted(versions, key=lambda v: (v.major, v.minor, v.patch))
        assert actual == expected

        # We can sort versions in reverse order using the standard sort function
        actual = sorted(versions, reverse=True)
        expected = sorted(versions, key=lambda v: (v.major, v.minor, v.patch), reverse=True)
        assert actual == expected

        # We can get the minimum version using the standard min function
        actual = min(versions)  # type: ignore
        expected = min(versions, key=lambda v: (v.major, v.minor, v.patch))  # type: ignore
        assert actual == expected

        # We can get the maximum version using the standard max function
        actual = max(versions)  # type: ignore
        expected = max(versions, key=lambda v: (v.major, v.minor, v.patch))  # type: ignore
        assert actual == expected

    def test_version_as_dict_key(self):
        """
        Use version as dictionary key
        """

        # We can use a version as a dictionary key
        versions = {
            StudyVersion(8, 7): "eight-seven",
            StudyVersion(8, 6): "eight-six",
            StudyVersion(8, 8): "eight-eight",
            StudyVersion(9, 0): "nine-zero",
            StudyVersion(7, 0): "seven-zero",
        }
        assert versions[StudyVersion(8, 7)] == "eight-seven"
        assert versions[StudyVersion(8, 6)] == "eight-six"
        assert versions[StudyVersion(8, 8)] == "eight-eight"
        assert versions[StudyVersion(9, 0)] == "nine-zero"
        assert versions[StudyVersion(7, 0)] == "seven-zero"
