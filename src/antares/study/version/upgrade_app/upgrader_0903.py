from pathlib import Path

import typing as t

from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod
from ..model.general_data import GeneralData


def _upgrade_thematic_trimming(data: GeneralData) -> None:
    def _get_thermal_variables_to_remove() -> t.Set[str]:
        groups = [
            "nuclear",
            "lignite",
            "coal",
            "battery",
            "gas",
            "oil",
            "mix. fuel",
            "misc. dtg",
            "misc. dtg 2",
            "misc. dtg 3",
            "misc. dtg 4",
        ]
        return groups

    def _get_renewable_variables_to_remove() -> t.Set[str]:
        groups = [
            "wind offshore",
            "wind onshore",
            "solar concrt.",
            "solar pv",
            "solar rooft",
            "renw. 1",
            "renw. 2",
            "renw. 3",
            "renw. 4",
        ]
        return groups

    variables_selection = data["variables selection"]
    var_thermal_to_remove = _get_thermal_variables_to_remove()
    var_renewable_to_remove = _get_renewable_variables_to_remove()

    d: t.Dict[str, t.List[str]] = {}
    for sign in ["+", "-"]:
        select_var = f"select_var {sign}"
        d[select_var] = []

        # append all variables not in the list to remove
        for var in variables_selection.get(select_var, []):
            if var.lower() not in var_thermal_to_remove and var.lower() not in var_renewable_to_remove:
                d[select_var].append(var)

    # we don't want to remove all groups we don't append STS by group
    select_var_minus = "select_var -"
    variables_selection[select_var_minus] = d[select_var_minus]

    # if some groups were enabled we reactivate the var
    append_thermal = False
    append_renewable = False
    select_var_plus = "select_var +"
    for var in variables_selection.get(select_var_plus, []):
        if var.lower() in var_thermal_to_remove:
            append_thermal = True
        if var.lower() in var_renewable_to_remove:
            append_renewable = True

    if append_thermal:
        d[select_var_plus].append("DISPATCH. GEN.")
    if append_renewable:
        d[select_var_plus].append("RENEWABLE GEN.")

    variables_selection[select_var_plus] = d[select_var_plus]


class UpgradeTo0903(UpgradeMethod):
    """
    This class upgrades the study from version 9.2 to version 9.3.
    """

    old = StudyVersion(9, 2)
    new = StudyVersion(9, 3)

    @staticmethod
    def _upgrade_general_data(study_dir: Path) -> None:
        data = GeneralData.from_ini_file(study_dir)
        general = data["general"]
        general.pop("refreshtimeseries", None)
        general.pop("refreshintervalload", None)
        general.pop("refreshintervalhydro", None)
        general.pop("refreshintervalwind", None)
        general.pop("refreshintervalthermal", None)
        general.pop("refreshintervalsolar", None)

        data["other preferences"]["accurate-shave-peaks-include-short-term-storage"] = False
        data["adequacy patch"]["redispatch"] = False

        if "variables selection" in data:
            _upgrade_thematic_trimming(data)

        data.to_ini_file(study_dir)

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 9.3.

        Args:
            study_dir: The study directory.
        """

        cls._upgrade_general_data(study_dir)
