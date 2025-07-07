from itertools import product
from pathlib import Path

import typing as t

from antares.study.version.ini_reader import IniReader
from antares.study.version.ini_writer import IniWriter
from antares.study.version.model.study_version import StudyVersion
from .exceptions import UnexpectedThematicTrimmingFieldsError

from .upgrade_method import UpgradeMethod
from ..model.general_data import GENERAL_DATA_PATH, GeneralData

class UpgradeTo0903(UpgradeMethod):
    """
    This class upgrades the study from version 9.2 to version 9.3.
    """

    old = StudyVersion(9, 2)
    new = StudyVersion(9, 3)

    @staticmethod
    def _upgrade_general_data(study_dir: Path) -> None:
        data = GeneralData.from_ini_file(study_dir)
        general = data["general"]
        general.pop("refreshtimeseries", None)
        general.pop("refreshintervalload", None)
        general.pop("refreshintervalhydro", None)
        general.pop("refreshintervalwind", None)
        general.pop("refreshintervalthermal", None)
        general.pop("refreshintervalsolar", None)

        data.to_ini_file(study_dir)


    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 9.3.

        Args:
            study_dir: The study directory.
        """

        cls._upgrade_general_data(study_dir)
