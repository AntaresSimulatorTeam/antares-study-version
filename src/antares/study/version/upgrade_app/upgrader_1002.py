from pathlib import Path

from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod
from ..model.general_data import GENERAL_DATA_PATH, GeneralData


def upgrade_general_data(data: GeneralData) -> None:
    data.setdefault("optimization", {}).setdefault("include-reserves", False)


class UpgradeTo1002(UpgradeMethod):
    """
    This class upgrades the study from version 10.1 to version 10.2.
    """

    old = StudyVersion(10, 1)
    new = StudyVersion(10, 2)
    files = [GENERAL_DATA_PATH]

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 10.2.

        Adds the new ``include-reserves`` optimization flag, which gates the reserves
        feature. Its default value ``False`` preserves the previous behavior.

        Args:
            study_dir: The study directory.
        """
        data = GeneralData.from_ini_file(study_dir)
        upgrade_general_data(data)
        data.to_ini_file(study_dir)
