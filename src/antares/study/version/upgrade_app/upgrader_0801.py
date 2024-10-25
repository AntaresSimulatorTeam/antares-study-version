from pathlib import Path

from antares.study.version.model.general_data import GENERAL_DATA_PATH, GeneralData
from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod
from antares.study.version.ini_writer import IniWriter
from antares.study.version.ini_reader import IniReader


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

        # Migrate thermal group from Other to Other 1
        thermal_cluster_dir = study_dir / "input" / "thermal" / "clusters"
        for area in thermal_cluster_dir.iterdir():
            ini_path = thermal_cluster_dir / area / "list.ini"
            sections = IniReader().read(ini_path)
            for section in sections.values():
                if section["group"].lower() == "Other".lower():
                    section["group"] = "other 1"
            IniWriter().write(sections, ini_path)
