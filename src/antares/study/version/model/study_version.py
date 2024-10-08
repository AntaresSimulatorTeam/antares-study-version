import dataclasses
import functools
import typing as t

from antares.study.version.converters import version_to_triplet

T = t.TypeVar("T", bound="_TripletVersion")


@dataclasses.dataclass(frozen=True, eq=False, order=False, unsafe_hash=True, init=True, repr=True)
@functools.total_ordering
class _TripletVersion:
    """
    Manage version numbers like (major, minor, patch) triplet.
    """

    major: int
    minor: int
    patch: int

    # Factory function

    @classmethod
    def parse(cls: t.Type[T], other: object) -> T:
        if isinstance(other, _TripletVersion):
            return cls(other.major, other.minor, other.patch)
        elif isinstance(other, (int, str, t.Sequence, t.Mapping)):
            return cls(*version_to_triplet(other))
        else:
            raise TypeError(f"Invalid version type: {type(other)!r}")

    # Conversion methods

    def __str__(self) -> str:
        if self.patch:
            return f"{self.major}.{self.minor}.{self.patch}"
        elif self.minor:
            return f"{self.major}.{self.minor}"
        else:
            return f"{self.major}"

    def __int__(self) -> int:
        return self.major * 100 + self.minor * 10 + self.patch

    def __iter__(self) -> t.Iterator[int]:
        yield self.major
        if self.minor:
            yield self.minor
            if self.patch:
                yield self.patch

    # Comparison operators

    def __ne__(self, other: object) -> bool:
        if isinstance(other, _TripletVersion):
            return (self.major, self.minor, self.patch).__ne__((other.major, other.minor, other.patch))
        elif isinstance(other, (int, str, t.Sequence, t.Mapping)):
            return self.__ne__(self.parse(other))
        else:
            return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _TripletVersion):
            return (self.major, self.minor, self.patch).__eq__((other.major, other.minor, other.patch))
        elif isinstance(other, (int, str, t.Sequence, t.Mapping)):
            return self.__eq__(self.parse(other))
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, _TripletVersion):
            return (self.major, self.minor, self.patch).__lt__((other.major, other.minor, other.patch))
        elif isinstance(other, (int, str, t.Sequence, t.Mapping)):
            return self.__lt__(self.parse(other))
        else:
            return NotImplemented

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, _TripletVersion):
            return (self.major, self.minor, self.patch).__gt__((other.major, other.minor, other.patch))
        elif isinstance(other, (int, str, t.Sequence, t.Mapping)):
            return self.__gt__(self.parse(other))
        else:
            return NotImplemented

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    # Format method

    def __format__(self, format_spec: str) -> str:
        """
        Format the version number "X.Y.Z" according to the format specifier:

        - "" => "X.Y.Z" or "X.Y" if patch is 0, or "X" if minor is 0.
        - "1d" => "X",
        - "2d" => "X.Y",
        - "01d" => "0X",
        - "02d" => "0X.0Y"
        - "d.d.d" => "XYZ"

        :param format_spec: format specifier.

        :return: the formatted version number.
        """
        major, minor, patch = self.major, self.minor, self.patch
        if not format_spec:
            return str(self)
        elif format_spec == "1d":
            return f"{major}"
        elif format_spec == "2d":
            return f"{major}.{minor}"
        elif format_spec == "3d":
            return f"{major}.{minor}.{patch}"
        elif format_spec == "01d":
            return f"{major:02d}"
        elif format_spec == "02d":
            return f"{major:02d}.{minor:02d}"
        elif format_spec == "03d":
            return f"{major:02d}.{minor:02d}.{patch:02d}"
        elif format_spec == "ddd":
            return f"{int(self):03d}"
        else:
            raise ValueError(f"Invalid format specifier: '{format_spec}'")


class SolverVersion(_TripletVersion):
    def __init__(self, major: t.Union[str, int], minor: t.Union[str, int] = 0, patch: t.Union[str, int] = 0):
        try:
            super().__init__(int(major), int(minor), int(patch))
        except ValueError:
            msg = f"Invalid parameters: {(major, minor, patch)!r}: you should use `parse` method instead."
            raise ValueError(msg) from None


class StudyVersion(_TripletVersion):
    def __init__(self, major: t.Union[str, int], minor: t.Union[str, int] = 0, _ignored_patch: t.Union[str, int] = 0):
        try:
            super().__init__(int(major), int(minor), 0)
        except ValueError:
            msg = f"Invalid parameters: {(major, minor)!r}: you should use `parse` method instead."
            raise ValueError(msg) from None


class SolverMinorVersion(SolverVersion):
    """
    Represents a SolverVersion but when we don't want to take the `patch` into account. Used inside antares-launcher.
    """

    pass
