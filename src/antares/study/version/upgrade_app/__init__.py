import dataclasses
import functools
import logging
import shutil
import tempfile
import typing as t
from pathlib import Path, PurePath

from ..exceptions import ApplicationError
from ..model.exceptions import ValidationError
from ..model.study_antares import StudyAntares
from ..model.study_version import StudyVersion
from .scenario_mapping import scenarios
from .upgrade_method import UpgradeMethod

logger = logging.getLogger(__name__)

UPGRADE_TEMPORARY_DIR_SUFFIX = ".upgrade.tmp"
UPGRADE_TEMPORARY_DIR_PREFIX = "~"


def is_temporary_upgrade_dir(path: Path) -> bool:
    """Check if a directory is a temporary upgrade directory."""
    return (
        path.name.startswith(UPGRADE_TEMPORARY_DIR_PREFIX)
        and "".join(path.suffixes[-2:]) == UPGRADE_TEMPORARY_DIR_SUFFIX
        and path.is_dir()
    )


def filter_out_child_files(files: t.Collection[str]) -> t.List[str]:
    """
    Filters out child files from a list of files.

    This function takes a list of file and folder paths and returns a list that excludes files or
    folders that are children of other items in the list. This can be useful to avoid duplicates when
    copying files or folders.

    Args:
        files: List of file and folder paths as strings.

    Returns:
        List of file and folder paths, excluding children already present in the list.
    """
    # Sort the files to ensure that parent directories are processed before the children.
    paths = sorted(PurePath(f) for f in files)

    # If the list is empty, return an empty list.
    if not paths:
        return []

    # Initialize the list of filtered paths with the first path.
    first, *paths = paths
    filtered_paths = [first]

    # Iterate over the remaining paths.
    for path in paths:
        # Check if the path is not already in the filtered list and is not a child of an existing path.
        last_path = filtered_paths[-1]
        if path not in filtered_paths and not any(parent == last_path for parent in path.parents):
            filtered_paths.append(path)

    return [str(p) for p in filtered_paths]


@dataclasses.dataclass
class UpgradeApp:
    """
    Create a new study.
    """

    study_dir: Path
    version: StudyVersion

    def __post_init__(self):
        """Parse, validate and initialize the fields of the object."""
        self.study_dir = Path(self.study_dir)
        self.version = StudyVersion.parse(self.version)
        if not self.study_dir.exists():
            raise FileNotFoundError(f"Study directory not found: {self.study_dir}")

    @functools.cached_property
    def study_antares(self) -> StudyAntares:
        """Load the 'study.antares' file of the study."""
        try:
            return StudyAntares.from_ini_file(self.study_dir)
        except ValidationError as e:
            raise ApplicationError(e.args[0]) from e

    @property
    def upgrade_methods(self) -> t.List[UpgradeMethod]:
        """Get the list of upgrade methods to apply to the study."""
        start = self.study_antares.version
        end = self.version
        try:
            return scenarios[start:end]  # type: ignore
        except KeyError as e:
            raise ApplicationError(e.args[0]) from e

    @property
    def should_denormalize(self) -> bool:
        """Check if the study should be denormalized before the upgrade."""
        return any(meth.should_denormalize for meth in self.upgrade_methods)

    def __call__(self) -> None:
        with tempfile.TemporaryDirectory(
            suffix=UPGRADE_TEMPORARY_DIR_SUFFIX, prefix=UPGRADE_TEMPORARY_DIR_PREFIX, dir=self.study_dir.parent
        ) as path:
            tmp_path = Path(path)

            # Prepare the upgrade
            files_to_upgrade = {f for meth in self.upgrade_methods for f in meth.files} | {"study.antares"}
            files_to_retrieve = self._copies_only_necessary_files(files_to_upgrade, tmp_path)

            try:
                # Perform the upgrade
                for meth in self.upgrade_methods:
                    meth.upgrade(self.study_dir)

                # Update the 'study.antares' file
                self.study_antares.version = self.version
                self.study_antares.to_ini_file(self.study_dir)

            except Exception:
                # If an error occurs, restore the original files
                self._safely_replace_original_files(files_to_retrieve, tmp_path)
                raise

    def _copies_only_necessary_files(self, files_to_upgrade: t.Collection[str], tmp_path: Path) -> t.List[str]:
        """
        Copies files concerned by the version upgrader into a temporary directory.

        Args:
            files_to_upgrade: List of the files and folders concerned by the upgrade.
            tmp_path: Path to the temporary directory where the file modification will be performed.

        Returns:
            The list of files and folders that were really copied. It's the same as files_to_upgrade but
            without any children that has parents already in the list.
        """
        files_to_copy = filter_out_child_files(files_to_upgrade)
        files_to_retrieve = []
        for relpath in files_to_copy:
            src_path = self.study_dir / relpath
            if not src_path.exists():
                # This can happen when upgrading a study to v8.8.
                continue
            dst_path = tmp_path / relpath
            if src_path.is_dir():
                if not dst_path.exists():
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                    files_to_retrieve.append(relpath)
            else:
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src_path, dst_path)
                files_to_retrieve.append(relpath)
        return files_to_retrieve

    def _safely_replace_original_files(self, files_to_replace: t.List[str], tmp_path: Path) -> None:
        """
        Replace files/folders of the study that should be upgraded by their copy already upgraded in the tmp directory.
        It uses Path.rename() and an intermediary tmp directory to swap the folders safely.
        In the end, all tmp directories are removed.

        Args:
            files_to_replace: List of files and folders that were really copied
            tmp_path: Path to the temporary directory where the file modification will be performed.
            (cf. _copies_only_necessary_files's doc just above)
        """
        for k, path in enumerate(files_to_replace):
            backup_dir = Path(
                tempfile.mkdtemp(
                    suffix=f".backup_{k}.tmp",
                    prefix="~",
                    dir=self.study_dir.parent,
                )
            )
            backup_dir.rmdir()
            original_path = self.study_dir / path
            original_path.rename(backup_dir)
            (tmp_path / path).rename(original_path)
            if backup_dir.is_dir():
                shutil.rmtree(backup_dir)
            else:
                backup_dir.unlink()
