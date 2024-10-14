from itertools import product
from pathlib import Path

import numpy as np

from antares.study.version.ini_reader import IniReader
from antares.study.version.ini_writer import IniWriter
from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod
from ..model.general_data import GENERAL_DATA_PATH, GeneralData


class UpgradeTo0902(UpgradeMethod):
    """
    This class upgrades the study from version 9.0 to version 9.2.
    """

    old = StudyVersion(9, 0)
    new = StudyVersion(9, 2)
    files = ["input/st-storage", GENERAL_DATA_PATH, "input/links"]

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 9.2.

        Args:
            study_dir: The study directory.
        """

        # =======================
        #  GENERAL DATA
        # =======================

        data = GeneralData.from_ini_file(study_dir)
        adq_patch = data["adequacy patch"]
        del adq_patch["enable-first-step"]
        del adq_patch["set-to-null-ntc-between-physical-out-for-first-step"]
        other_preferences = data["other preferences"]
        del other_preferences["initial-reservoir-levels"]
        other_preferences["hydro-pmax-format"] = "daily"
        data["general"]["nbtimeserieslinks"] = 1

        # Migrates the thematic trimming part
        if "variables selection" in data:
            variables_selection = data["variables selection"]
            groups = ["psp_open", "psp_closed", "pondage", "battery", "other1", "other2", "other3", "other4", "other5"]
            outputs = ["_injection", "_withdrawal", "_level"]
            possible_variables = {f"{group}{output}" for group, output in product(groups, outputs)}
            sign = "+" if "select_var +" in variables_selection else "-"
            selected_var_section = variables_selection[f"select_var {sign}"]
            copied_list = []
            count = 0
            for var in selected_var_section:
                if var.lower() not in possible_variables:
                    copied_list.append(var)
                    count = 1
            if count == 1:
                copied_list.append("STS by group")
            variables_selection[f"select_var {sign}"] = copied_list

        data.to_ini_file(study_dir)

        # =======================
        #  LINKS
        # =======================

        links_path = study_dir / "input" / "links"
        default_prepro = np.tile([1, 1, 0, 0, 0, 0], (365, 1))
        default_modulation = np.ones(dtype=int, shape=(8760, 1))
        for area in links_path.iterdir():
            area_path = links_path / area
            capacity_folder = area_path / "capacities"
            if not capacity_folder.exists():
                # the folder doesn't contain any existing link
                continue

            ini_path = area_path / "properties.ini"
            reader = IniReader()
            writer = IniWriter()
            sections = reader.read(ini_path)
            area_names = []
            for area_name, section in sections.items():
                area_names.append(area_name)
                section["unitcount"] = 1
                section["nominalcapacity"] = 0
                section["law.planned"] = "uniform"
                section["law.forced"] = "uniform"
                section["volatility.planned"] = 0
                section["volatility.forced"] = 0
                section["force-no-generation"] = True
            writer.write(sections, ini_path)

            prepro_path = area_path / "prepro"
            prepro_path.mkdir()
            for area_name in area_names:
                np.savetxt(prepro_path / f"{area_name}_direct.txt", default_prepro, delimiter="\t", fmt="%.6f")
                np.savetxt(prepro_path / f"{area_name}_indirect.txt", default_prepro, delimiter="\t", fmt="%.6f")
                np.savetxt(prepro_path / f"{area_name}_mod.txt", default_modulation, delimiter="\t", fmt="%.6f")

        # =======================
        #  ST STORAGES
        # =======================

        st_storage_dir = study_dir / "input" / "st-storage"
        reader = IniReader()
        writer = IniWriter()
        cluster_files = (st_storage_dir / "clusters").glob("*/list.ini")
        for file_path in cluster_files:
            sections = reader.read(file_path)
            for section in sections.values():
                section["efficiencywithdrawal"] = 1
            writer.write(sections, file_path)

        matrices_to_create = ["cost-injection.txt", "cost-withdrawal.txt", "cost-level.txt"]
        series_path = st_storage_dir / "series"
        for area in series_path.iterdir():
            area_dir = st_storage_dir / "series" / area
            for storage in area_dir.iterdir():
                final_dir = area_dir / storage
                for matrix in matrices_to_create:
                    (final_dir / matrix).touch()
