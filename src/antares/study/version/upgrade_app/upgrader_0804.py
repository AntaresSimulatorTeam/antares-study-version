from pathlib import Path

from antares.study.version.model.general_data import GENERAL_DATA_PATH, GeneralData
from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod

_TRANSMISSION_CAPACITIES = {
    True: "local-values",
    False: "null-for-all-links",
    "infinite": "infinite-for-all-links",
}


class UpgradeTo0804(UpgradeMethod):
    """
    This class upgrades the study from version 8.3 to version 8.4.
    """

    old = StudyVersion(8, 3)
    new = StudyVersion(8, 4)
    files = [GENERAL_DATA_PATH]

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 8.4.

        Args:
            study_dir: The study directory.
        """
        data = GeneralData.from_ini_file(study_dir)
        actual_capacities = data["optimization"]["transmission-capacities"]
        data["optimization"]["transmission-capacities"] = _TRANSMISSION_CAPACITIES[actual_capacities]
        data["optimization"].pop("include-split-exported-mps", None)
        data.to_ini_file(study_dir)
