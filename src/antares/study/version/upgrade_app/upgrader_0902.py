from itertools import product
from pathlib import Path

import numpy as np
import typing as t

from antares.study.version.ini_reader import IniReader
from antares.study.version.ini_writer import IniWriter
from antares.study.version.model.study_version import StudyVersion
from .exceptions import UnexpectedThematicTrimmingFieldsError

from .upgrade_method import UpgradeMethod
from ..model.general_data import GENERAL_DATA_PATH, GeneralData


def _upgrade_thematic_trimming(data: GeneralData) -> None:
    def _get_possible_variables() -> t.Set[str]:
        groups = ["psp_open", "psp_closed", "pondage", "battery", "other1", "other2", "other3", "other4", "other5"]
        outputs = ["injection", "withdrawal", "level"]
        return {f"{group}_{output}" for group, output in product(groups, outputs)}

    variables_selection = data["variables selection"]
    possible_variables = _get_possible_variables()
    d: t.Dict[str, t.Dict[str, t.List[str]]] = {}
    for sign in ["+", "-"]:
        select_var = f"select_var {sign}"
        d[select_var] = {"keep": [], "remove": []}
        # The 'remove' list gathers all fields that should not be kept after the upgrade.
        # It applies to any field inside the 27 listed by the `_get_possible_variables` method.
        # The 'keep' list gathers all fields that have nothing to do with the upgrade and therefore should be kept.
        # We check these fields for enabled and disabled variables (symbolized by +/-) as we can have both.
        # In the end, we remove all legacy fields and replace them by one field only: 'STS by group'.
        # For more information, see https://antares-simulator.readthedocs.io/en/latest/user-guide/04-migration-guides/#short-term-storage-groups
        for var in variables_selection.get(select_var, []):
            key = "remove" if var.lower() in possible_variables else "keep"
            d[select_var][key].append(var)

    if d["select_var +"]["remove"] and d["select_var -"]["remove"]:
        raise UnexpectedThematicTrimmingFieldsError(d["select_var +"]["remove"], d["select_var -"]["remove"])
    for sign in ["+", "-"]:
        select_var = f"select_var {sign}"
        if d[select_var]["keep"]:
            d[select_var]["keep"].append("STS by group")
            variables_selection[select_var] = d[select_var]["keep"]


class UpgradeTo0902(UpgradeMethod):
    """
    This class upgrades the study from version 9.0 to version 9.2.
    """

    old = StudyVersion(9, 0)
    new = StudyVersion(9, 2)
    files = ["input/st-storage", GENERAL_DATA_PATH, "input/links"]

    @staticmethod
    def _upgrade_general_data(study_dir: Path) -> None:
        data = GeneralData.from_ini_file(study_dir)
        adq_patch = data["adequacy patch"]
        adq_patch.pop("enable-first-step", None)
        adq_patch.pop("set-to-null-ntc-between-physical-out-for-first-step", None)
        other_preferences = data["other preferences"]
        other_preferences.pop("initial-reservoir-levels", None)
        other_preferences["hydro-pmax-format"] = "daily"
        data["general"]["nbtimeserieslinks"] = 1

        if "variables selection" in data:
            _upgrade_thematic_trimming(data)

        data.to_ini_file(study_dir)

    @staticmethod
    def _upgrade_links(study_dir: Path) -> None:
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

    @staticmethod
    def _upgrade_storages(study_dir: Path) -> None:
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

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 9.2.

        Args:
            study_dir: The study directory.
        """

        cls._upgrade_general_data(study_dir)
        cls._upgrade_links(study_dir)
        cls._upgrade_storages(study_dir)
