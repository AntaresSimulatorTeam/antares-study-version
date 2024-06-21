from pathlib import Path

from antares.study.version.model.general_data import GENERAL_DATA_PATH, GeneralData
from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod


class UpgradeTo0701(UpgradeMethod):
    """
    This class upgrades the study from version 6.0 (or above) to version 7.1.
    """

    old = StudyVersion(6, 0)
    new = StudyVersion(7, 1)
    files = [GENERAL_DATA_PATH]

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 7.1.

        Args:
            study_dir: The study directory.
        """
        data = GeneralData.from_ini_file(study_dir)
        data["general"]["geographic-trimming"] = data["general"].pop("filtering")
        data["general"]["thematic-trimming"] = False
        data["optimization"]["link-type"] = "local"
        data["other preferences"]["hydro-pricing-mode"] = "fast"
        data.to_ini_file(study_dir)
