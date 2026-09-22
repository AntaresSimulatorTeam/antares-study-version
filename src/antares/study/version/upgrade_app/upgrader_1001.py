from pathlib import Path

from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod
from ..model.general_data import GENERAL_DATA_PATH, GeneralData


class UpgradeTo1001(UpgradeMethod):
    """
    This class upgrades the study from version 9.3 to version 10.1.
    """

    old = StudyVersion(9, 3)
    new = StudyVersion(10, 1)
    files = [GENERAL_DATA_PATH]

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 10.1.

        Adds the new ``hydro-rule-curves`` compatibility flag for scenarized hydro
        reservoir levels. Its default value ``single`` preserves the previous behavior.

        Args:
            study_dir: The study directory.
        """
        data = GeneralData.from_ini_file(study_dir)
        data.setdefault("compatibility", {}).setdefault("hydro-rule-curves", "single")
        data.to_ini_file(study_dir)
