from pathlib import Path

from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod


class UpgradeTo1001(UpgradeMethod):
    """
    This class upgrades the study from version 9.3 to version 10.1.
    """

    old = StudyVersion(9, 3)
    new = StudyVersion(10, 1)

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 10.1.

        Args:
            study_dir: The study directory.
        """
        # Nothing to do since version number is handled in src/antares/study/version/model/study_antares.py
        pass
