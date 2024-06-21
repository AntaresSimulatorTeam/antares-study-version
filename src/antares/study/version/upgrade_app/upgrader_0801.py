from pathlib import Path

from antares.study.version.model.general_data import GENERAL_DATA_PATH, GeneralData
from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod


class UpgradeTo0801(UpgradeMethod):
    """
    This class upgrades the study from version 8.0 to version 8.1.
    """

    old = StudyVersion(8, 0)
    new = StudyVersion(8, 1)
    files = [GENERAL_DATA_PATH, "input"]

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 8.1.

        Args:
            study_dir: The study directory.
        """
        data = GeneralData.from_ini_file(study_dir)
        data["other preferences"]["renewable-generation-modelling"] = "aggregated"
        data.to_ini_file(study_dir)
        study_dir.joinpath("input", "renewables", "clusters").mkdir(parents=True, exist_ok=True)
        study_dir.joinpath("input", "renewables", "series").mkdir(parents=True, exist_ok=True)
