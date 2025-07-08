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
    def _get_variables_to_remove() -> t.Set[str]:
        groups = ["psp_open", "psp_closed", "pondage", "battery", "other1", "other2", "other3", "other4", "other5"]
        outputs = ["injection", "withdrawal", "level"]
        return {f"{group}_{output}" for group, output in product(groups, outputs)}

    variables_selection = data["variables selection"]
    var_to_remove = _get_variables_to_remove()
    
    d: t.Dict[str, t.Dict[str, t.List[str]]] = {}
    for sign in ["+", "-"]:
        select_var = f"select_var {sign}"
        d[select_var] = []
        
        # append all variables not in the list to remove
        for var in variables_selection.get(select_var, []):
            if not var.lower() in var_to_remove:
                d[select_var].append(var)

    # we don't want to remove all groups we don't append STS by group
    select_var_minus = f"select_var -"
    variables_selection[select_var_minus] = d[select_var_minus]

    # if some groups were enabled we reactivate the var
    select_var_plus = f"select_var +"
    if d[select_var_plus]:
        for var in variables_selection.get(select_var_plus, []):
            if var.lower() in var_to_remove:
                d[select_var_plus].append("STS by group")
    variables_selection[select_var_plus] = d[select_var_plus]


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
