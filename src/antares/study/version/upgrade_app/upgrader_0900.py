from pathlib import Path

from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod


class UpgradeTo0900(UpgradeMethod):
    """
    This class upgrades the study from version 8.8 to version 9.0.
    """

    old = StudyVersion(8, 8)
    new = StudyVersion(9, 0)
    files = ["study.antares"]

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 9.0.

        Args:
            study_dir: The study directory.
        """
        # Nothing to do since version number is handled in src/antares/study/version/model/study_antares.py
        pass
