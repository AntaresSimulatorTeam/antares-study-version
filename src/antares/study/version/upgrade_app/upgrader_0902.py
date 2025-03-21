from itertools import product
from pathlib import Path

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
    files = ["input/st-storage", GENERAL_DATA_PATH, "input/hydro/hydro.ini", "input/areas"]

    @staticmethod
    def _upgrade_general_data(study_dir: Path) -> None:
        data = GeneralData.from_ini_file(study_dir)
        adq_patch = data["adequacy patch"]
        adq_patch.pop("enable-first-step", None)
        adq_patch.pop("set-to-null-ntc-between-physical-out-for-first-step", None)
        other_preferences = data["other preferences"]
        other_preferences.pop("initial-reservoir-levels", None)
        other_preferences["shedding-policy"] = "accurate shave peaks"
        data["compatibility"] = {"hydro-pmax": "daily"}

        if "variables selection" in data:
            _upgrade_thematic_trimming(data)

        data.to_ini_file(study_dir)

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
                section["penalize-variation-injection"] = False
                section["penalize-variation-withdrawal"] = False
            writer.write(sections, file_path)

        matrices_to_create = [
            "cost-injection.txt",
            "cost-withdrawal.txt",
            "cost-level.txt",
            "cost-variation-injection.txt",
            "cost-variation-withdrawal.txt",
        ]
        series_path = st_storage_dir / "series"
        if not Path(series_path).is_dir():
            return
        for area in series_path.iterdir():
            area_dir = st_storage_dir / "series" / area
            for storage in area_dir.iterdir():
                final_dir = area_dir / storage
                for matrix in matrices_to_create:
                    (final_dir / matrix).touch()

    @staticmethod
    def _upgrade_hydro(study_dir: Path) -> None:
        # Retrieves the list of existing areas
        all_areas_ids = set()
        for element in (study_dir / "input" / "areas").iterdir():
            if element.is_dir():
                all_areas_ids.add(element.name)

        # Builds the new section to add to the file
        new_section = {area_id: 1 for area_id in all_areas_ids}

        # Adds the section to the file
        ini_path = study_dir / "input" / "hydro" / "hydro.ini"
        reader = IniReader()
        sections = reader.read(ini_path)
        sections["overflow spilled cost difference"] = new_section
        writer = IniWriter()
        writer.write(sections, ini_path)

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 9.2.

        Args:
            study_dir: The study directory.
        """

        cls._upgrade_general_data(study_dir)
        cls._upgrade_storages(study_dir)
        cls._upgrade_hydro(study_dir)
