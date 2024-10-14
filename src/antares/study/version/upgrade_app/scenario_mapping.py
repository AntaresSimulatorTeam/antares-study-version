import collections.abc
import typing as t

from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod
from .upgrader_0701 import UpgradeTo0701
from .upgrader_0702 import UpgradeTo0702
from .upgrader_0800 import UpgradeTo0800
from .upgrader_0801 import UpgradeTo0801
from .upgrader_0802 import UpgradeTo0802
from .upgrader_0803 import UpgradeTo0803
from .upgrader_0804 import UpgradeTo0804
from .upgrader_0805 import UpgradeTo0805
from .upgrader_0806 import UpgradeTo0806
from .upgrader_0807 import UpgradeTo0807
from .upgrader_0808 import UpgradeTo0808
from .upgrader_0900 import UpgradeTo0900
from .upgrader_0902 import UpgradeTo0902

ALL_UPGRADE_METHODS = (
    UpgradeTo0701(),
    UpgradeTo0702(),
    UpgradeTo0800(),
    UpgradeTo0801(),
    UpgradeTo0802(),
    UpgradeTo0803(),
    UpgradeTo0804(),
    UpgradeTo0805(),
    UpgradeTo0806(),
    UpgradeTo0807(),
    UpgradeTo0808(),
    UpgradeTo0900(),
    UpgradeTo0902(),
)


class ScenarioMapping(collections.abc.Mapping):
    """
    Manage the upgrade scenario of a study from one version to another.

    The upgrade scenario is a sequence of upgrade methods that can be applied to a study
    to upgrade it from one version to another.

    This mapping is used to find the upgrade method that can upgrade from a given version,
    or to get the list of upgrade methods from one version to another.
    """

    def __init__(self, methods: t.Sequence[UpgradeMethod] = ()) -> None:
        """
        Initialize the upgrade scenario from an ordered list of upgrade methods.

        Args:
            methods: The list of upgrade methods.
        """
        self._methods = methods
        for prev_meth, next_meth in zip(self._methods[:-1], self._methods[1:]):
            prev_version = prev_meth.new
            next_version = next_meth.old
            if prev_version != next_version:
                raise ValueError(f"Upgrade methods are not in the right order: {prev_version} != {next_version}")

    def _get_upgrade_method(self, study_version: StudyVersion) -> UpgradeMethod:
        """
        Find the next study version from the given version.

        Args:
            study_version: The current version as a string.

        Returns:
            The next version as a string.
        """
        for meth in self._methods:
            if meth.can_upgrade(study_version):
                return meth
        raise KeyError(f"Cannot upgrade from version '{study_version}'")

    def _iter_upgrade_methods(
        self, start: StudyVersion, end: t.Optional[StudyVersion]
    ) -> t.Generator[UpgradeMethod, None, None]:
        """
        Get the upgrade scenario from the start version to the end version.

        Args:
            start: The start version.
            end: The end version.

        Returns:
            The list of upgrade methods.
        """

        iter_methods = iter(self._methods)

        # First, find the first upgrade method that can upgrade from the start version
        for meth in iter_methods:
            if meth.can_upgrade(start) and (end is None or meth.new <= end):  # type: ignore
                yield meth
                break
        else:
            # No upgrade method found
            return

        # Then, find the next upgrade methods until the end version
        curr = meth.new
        for meth in iter_methods:
            if meth.can_upgrade(curr) and (end is None or meth.new <= end):
                yield meth
                curr = meth.new
            else:
                # We reached the end version or we passed it
                return

    def _get_upgrade_methods(
        self, from_version: StudyVersion, to_version: t.Optional[StudyVersion]
    ) -> t.Tuple[UpgradeMethod, ...]:
        """
        Get the upgrade scenario from the start version to the end version.

        Args:
            from_version: The start version.
            to_version: The end version.

        Returns:
            The list of upgrade methods.
        """
        if to_version is None:
            methods = tuple(self._iter_upgrade_methods(from_version, to_version))
            if not methods:
                raise KeyError(f"Cannot upgrade from version '{from_version}': unknown version")
            return methods
        else:
            if from_version == to_version:
                raise KeyError(f"Your study is already in version '{to_version}'")
            elif from_version > to_version:
                raise KeyError(f"Cannot downgrade from version '{from_version}' to '{to_version}'")

            methods = tuple(self._iter_upgrade_methods(from_version, to_version))

            if not methods:
                raise KeyError(f"Cannot upgrade from version '{from_version}': unknown version")
            elif methods[-1].new != to_version:
                raise KeyError(f"Cannot upgrade to version '{to_version}': version unreachable")

            return methods

    def __getitem__(
        self, index: t.Union[int, StudyVersion, slice]
    ) -> t.Union[UpgradeMethod, t.Sequence[UpgradeMethod]]:
        """
        Get the upgrade method from the given version or slice (range of versions).

        Args:
            index: The version or slice.

        Returns:
            The upgrade method or a list of upgrade methods.
        """
        if isinstance(index, int):
            return self._methods[index]
        elif isinstance(index, slice):
            start = index.start
            stop = index.stop
            return self._get_upgrade_methods(start, stop)
        elif isinstance(index, StudyVersion):
            return self._get_upgrade_method(index)
        else:
            raise TypeError(f"Invalid key type: {type(index)!r}")

    def __contains__(self, study_version: StudyVersion) -> bool:  # type: ignore
        """
        Check if a study version can be upgraded.
        """
        try:
            self._get_upgrade_method(study_version)
        except KeyError:
            return False
        else:
            return True

    def __len__(self) -> int:
        """
        Get the number of upgrade methods.
        """
        return self._methods.__len__()

    def __iter__(self) -> t.Iterator[StudyVersion]:
        """
        Iterate over the new versions of the upgrade methods.
        """
        return (meth.old for meth in self._methods)


scenarios = ScenarioMapping(ALL_UPGRADE_METHODS)
