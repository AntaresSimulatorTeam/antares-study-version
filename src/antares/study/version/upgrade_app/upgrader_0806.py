from pathlib import Path

from antares.study.version.model.general_data import GENERAL_DATA_PATH, GeneralData
from antares.study.version.model.study_version import StudyVersion

from .helpers import transform_name_to_id
from .upgrade_method import UpgradeMethod


class UpgradeTo0806(UpgradeMethod):
    """
    This class upgrades the study from version 8.5 to version 8.6.
    """

    old = StudyVersion(8, 5)
    new = StudyVersion(8, 6)
    files = [GENERAL_DATA_PATH, "input"]

    # noinspection SpellCheckingInspection
    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 8.6.

        Args:
            study_dir: The study directory.
        """
        data = GeneralData.from_ini_file(study_dir)
        data["adequacy patch"]["enable-first-step"] = False
        data.to_ini_file(study_dir)

        study_dir.joinpath("input", "st-storage", "clusters").mkdir(parents=True, exist_ok=True)
        study_dir.joinpath("input", "st-storage", "series").mkdir(parents=True, exist_ok=True)
        areas_path = study_dir.joinpath("input", "areas", "list.txt")
        area_names = areas_path.read_text(encoding="utf-8").splitlines(keepends=False)
        area_ids = (transform_name_to_id(area_name) for area_name in area_names)
        for area_id in area_ids:
            st_storage_path = study_dir.joinpath("input", "st-storage", "clusters", area_id)
            st_storage_path.mkdir(parents=True, exist_ok=True)
            (st_storage_path / "list.ini").touch()

            hydro_series_path = study_dir.joinpath("input", "hydro", "series", area_id)
            hydro_series_path.mkdir(parents=True, exist_ok=True)
            (hydro_series_path / "mingen.txt").touch()
