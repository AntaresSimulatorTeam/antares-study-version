from pathlib import Path

from antares.study.version.model.general_data import GENERAL_DATA_PATH, GeneralData
from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod


class UpgradeTo0805(UpgradeMethod):
    """
    This class upgrades the study from version 8.4 to version 8.5.
    """

    old = StudyVersion(8, 4)
    new = StudyVersion(8, 5)
    files = [GENERAL_DATA_PATH]

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 8.5.

        Args:
            study_dir: The study directory.
        """
        data = GeneralData.from_ini_file(study_dir)
        adequacy_patch = data["adequacy patch"]
        adequacy_patch["price-taking-order"] = "DENS"
        adequacy_patch["include-hurdle-cost-csr"] = False
        adequacy_patch["check-csr-cost-function"] = False
        adequacy_patch["threshold-initiate-curtailment-sharing-rule"] = 1.0
        adequacy_patch["threshold-display-local-matching-rule-violations"] = 0.0
        adequacy_patch["threshold-csr-variable-bounds-relaxation"] = 7
        data.to_ini_file(study_dir)
