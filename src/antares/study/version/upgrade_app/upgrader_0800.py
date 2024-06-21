from pathlib import Path

from antares.study.version.model.general_data import GENERAL_DATA_PATH, GeneralData
from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod


class UpgradeTo0800(UpgradeMethod):
    """
    This class upgrades the study from version 7.2 to version 8.0.
    """

    old = StudyVersion(7, 2)
    new = StudyVersion(8, 0)
    files = [GENERAL_DATA_PATH]

    # noinspection SpellCheckingInspection
    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 8.0.

        Args:
            study_dir: The study directory.
        """
        data = GeneralData.from_ini_file(study_dir)
        data["other preferences"]["hydro-heuristic-policy"] = "accommodate rule curves"
        data["optimization"]["include-exportstructure"] = False
        data["optimization"]["include-unfeasible-problem-behavior"] = "error-verbose"
        data["general"]["custom-scenario"] = data["general"].pop("custom-ts-numbers")
        data.to_ini_file(study_dir)
