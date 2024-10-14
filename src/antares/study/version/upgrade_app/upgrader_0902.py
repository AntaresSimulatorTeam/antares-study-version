import copy
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
            clusters = [
                "psp_open",
                "psp_closed",
                "pondage",
                "battery",
                "other1",
                "other2",
                "other3",
                "other4",
                "other5",
            ]
            outputs = ["_injection", "_withdrawal", "_level"]
            possible_variables = {f"{group}{output}" for group, output in product(clusters, outputs)}
            selected_var_section = variables_selection.get("select_var -", None) or variables_selection["select_var +"]
            copied_section = copy.deepcopy(selected_var_section)
            count = 0
            for key, var in selected_var_section.values():
                if var.lower() in possible_variables:
                    del copied_section[key]
                    count = 1
            if count == 1:
                copied_section[len(copied_section)] = "STS by group"
            for key in ["select_var -", "select_var +"]:
                if key in variables_selection:
                    variables_selection[key] = copied_section

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
        if not st_storage_dir.exists():
            # The folder only exists for studies in v8.6+ that have some short term storage clusters.
            # For every other case, this upgrader has nothing to do.
            return

        reader = IniReader()
        writer = IniWriter()
        cluster_files = st_storage_dir.glob("*/list.ini")
        for file_path in cluster_files:
            sections = reader.read(file_path)
            for section in sections.values():
                section["efficiencywithdrawal"] = 1
            writer.write(sections, file_path)

        matrices_to_create = ["cost-injection.txt", "cost-withdrawal.txt", "cost-level.txt"]
        series_path = st_storage_dir / "series"
        for area in series_path.iterdir():
            area_dir = st_storage_dir / "series" / area
            for matrix in matrices_to_create:
                (area_dir / matrix).touch()
