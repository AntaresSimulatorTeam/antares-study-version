from pathlib import Path

from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod
from ..model.general_data import GENERAL_DATA_PATH, GeneralData


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

        Adds the new ``include-reserves`` optimization flag (default ``false``) and removes
        the ``intra-modal``, ``correlateddraws``, ``horizon`` and ``readonly`` properties of the
        ``general`` section, which are now ignored by the simulator.

        Args:
            study_dir: The study directory.
        """
        data = GeneralData.from_ini_file(study_dir)
        general = data.setdefault("general", {})
        general.pop("intra-modal", None)
        general.pop("correlateddraws", None)
        general.pop("horizon", None)
        general.pop("readonly", None)
        data.setdefault("optimization", {})["include-reserves"] = False
        data.to_ini_file(study_dir)
