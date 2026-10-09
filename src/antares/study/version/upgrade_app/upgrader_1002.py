from pathlib import Path

from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod
from ..model.general_data import GENERAL_DATA_PATH, GeneralData


class UpgradeTo1002(UpgradeMethod):
    """
    This class upgrades the study from version 9.3 to version 10.2.
    """

    old = StudyVersion(9, 3)
    new = StudyVersion(10, 2)
    files = [GENERAL_DATA_PATH]

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 10.2.

        - Adds the ``hydro-rule-curves`` compatibility flag for scenarized hydro reservoir levels.
          Its default value ``single`` preserves the previous behavior.
        - Adds the ``include-reserves`` optimization flag (default ``false``).
        - Removes the ``intra-modal``, ``correlateddraws`` and ``readonly`` properties
          of the ``general`` section, which are now ignored by the simulator.
          The ``horizon`` property is kept, as it is still used by the web app to know
          how the input time series were built.

        Args:
            study_dir: The study directory.
        """
        data = GeneralData.from_ini_file(study_dir)
        general = data.setdefault("general", {})
        general.pop("intra-modal", None)
        general.pop("correlateddraws", None)
        general.pop("readonly", None)
        data.setdefault("optimization", {})["include-reserves"] = False
        data.setdefault("compatibility", {}).setdefault("hydro-rule-curves", "single")
        data.to_ini_file(study_dir)
