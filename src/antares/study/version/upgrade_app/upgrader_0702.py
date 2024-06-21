from pathlib import Path

from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod


class UpgradeTo0702(UpgradeMethod):
    """
    This class upgrades the study from version 7.1 to version 7.2.
    """

    old = StudyVersion(7, 1)
    new = StudyVersion(7, 2)

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 7.2.

        There is no input modification between the 7.1.0 and the 7.2.0 versions.

        Args:
            study_dir: The study directory.
        """
