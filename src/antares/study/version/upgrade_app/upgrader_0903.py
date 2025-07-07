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
    def _get_possible_thermal_variables() -> t.Set[str]:
        groups = ["nuclear", "lignite", "coal", "battery", "gas", "oil", "mix. fuel", "misc. dtg", "misc. dtg 2", "misc. dtg 3", "misc. dtg 4"]
        return groups

    def _get_possible_renewable_variables() -> t.Set[str]:
        groups = ["wind offshore", "wind onshore", "solar concrt.", "solar pv", "solar rooft", "renw. 1", "renw. 2", "renw. 3", "renw. 4"]
        return groups

    variables_selection = data["variables selection"]
    possible_variables = _get_possible_thermal_variables()
    d: t.Dict[str, t.Dict[str, t.List[str]]] = {}
    for sign in ["+", "-"]:
        select_var = f"select_var {sign}"
        d[select_var] = {"keep": [], "remove": []}
        # The 'remove' list gathers all fields that should not be kept after the upgrade.
        # It applies to any field listed by the `_get_possible_variables` methods.
        # The 'keep' list gathers all fields that have nothing to do with the upgrade and therefore should be kept.
        # We check these fields for enabled and disabled variables (symbolized by +/-) as we can have both.
        # In the end, we remove all legacy fields and replace them either by "DISPATCH. GEN." or "RENEWABLE GEN.".
        for var in variables_selection.get(select_var, []):
            key = "remove" if var.lower() in possible_variables else "keep"
            d[select_var][key].append(var)

    if d["select_var +"]["remove"] and d["select_var -"]["remove"]:
        raise UnexpectedThematicTrimmingFieldsError(d["select_var +"]["remove"], d["select_var -"]["remove"])
    for sign in ["+", "-"]:
        select_var = f"select_var {sign}"
        if d[select_var]["keep"]:
            d[select_var]["keep"].append("DISPATCH. GEN.")
            variables_selection[select_var] = d[select_var]["keep"]

    possible_variables = _get_possible_renewable_variables()
    d: t.Dict[str, t.Dict[str, t.List[str]]] = {}
    for sign in ["+", "-"]:
        select_var = f"select_var {sign}"
        d[select_var] = {"keep": [], "remove": []}
        # The 'remove' list gathers all fields that should not be kept after the upgrade.
        # It applies to any field listed by the `_get_possible_variables` methods.
        # The 'keep' list gathers all fields that have nothing to do with the upgrade and therefore should be kept.
        # We check these fields for enabled and disabled variables (symbolized by +/-) as we can have both.
        # In the end, we remove all legacy fields and replace them either by "DISPATCH. GEN." or "RENEWABLE GEN.".
        for var in variables_selection.get(select_var, []):
            key = "remove" if var.lower() in possible_variables else "keep"
            d[select_var][key].append(var)

    if d["select_var +"]["remove"] and d["select_var -"]["remove"]:
        raise UnexpectedThematicTrimmingFieldsError(d["select_var +"]["remove"], d["select_var -"]["remove"])
    for sign in ["+", "-"]:
        select_var = f"select_var {sign}"
        if d[select_var]["keep"]:
            d[select_var]["keep"].append("RENEWABLE GEN.")
            variables_selection[select_var] = d[select_var]["keep"]

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
