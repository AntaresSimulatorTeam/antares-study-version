from pathlib import Path

from antares.study.version.ini_writer import IniWriter
from antares.study.version.model.general_data import GENERAL_DATA_PATH, GeneralData
from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod


class UpgradeTo0803(UpgradeMethod):
    """
    This class upgrades the study from version 8.2 to version 8.3.
    """

    old = StudyVersion(8, 2)
    new = StudyVersion(8, 3)
    files = [GENERAL_DATA_PATH, "input/areas"]

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 8.3.

        Args:
            study_dir: The study directory.
        """
        data = GeneralData.from_ini_file(study_dir)
        data["adequacy patch"] = {
            "include-adq-patch": False,
            "set-to-null-ntc-between-physical-out-for-first-step": True,
            "set-to-null-ntc-from-physical-out-to-physical-in-for-first-step": True,
        }
        data["optimization"]["include-split-exported-mps"] = False
        data.to_ini_file(study_dir)
        areas = (p for p in study_dir.glob("input/areas/*") if p.is_dir())
        for folder_path in areas:
            writer = IniWriter()
            writer.write(
                {"adequacy-patch": {"adequacy-patch-mode": "outside"}},
                folder_path / "adequacy_patch.ini",
            )
