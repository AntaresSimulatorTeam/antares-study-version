import typing as t
from pathlib import Path

import numpy as np
import numpy.typing as npt
import pandas as pd

from antares.study.version.ini_reader import IniReader
from antares.study.version.ini_writer import IniWriter
from antares.study.version.model.study_version import StudyVersion

from .exceptions import UnexpectedMatrixLinksError
from .upgrade_method import UpgradeMethod


class UpgradeTo0807(UpgradeMethod):
    """
    This class upgrades the study from version 8.6 to version 8.7.
    """

    old = StudyVersion(8, 6)
    new = StudyVersion(8, 7)
    files = ["input/bindingconstraints", "input/thermal"]
    should_denormalize = True

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 8.7.

        Args:
            study_dir: The study directory.
        """
        binding_constraints_dit = study_dir / "input" / "bindingconstraints"

        # Check if there are unresolved matrix links in the directory
        unresolved_link = next(iter(binding_constraints_dit.glob("*.txt.link")), False)
        if isinstance(unresolved_link, Path):
            raise UnexpectedMatrixLinksError(unresolved_link.relative_to(study_dir).as_posix())

        # Split existing binding constraints in 3 different files
        binding_constraints_files = binding_constraints_dit.glob("*.txt")
        for file in binding_constraints_files:
            name = file.stem
            if file.stat().st_size == 0:
                lt, gt, eq = pd.Series(), pd.Series(), pd.Series()  # type: ignore
            else:
                df = pd.read_csv(file, sep="\t", header=None)
                lt, gt, eq = df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]
            for term, suffix in zip([lt, gt, eq], ["lt", "gt", "eq"]):
                # noinspection PyTypeChecker
                np.savetxt(
                    binding_constraints_dit / f"{name}_{suffix}.txt",
                    t.cast(npt.NDArray[np.float64], term.values),
                    delimiter="\t",
                    fmt="%.6f",
                )
            file.unlink()

        ini_reader = IniReader()
        ini_writer = IniWriter()

        # Add property group for every section in .ini file
        ini_file_path = binding_constraints_dit / "bindingconstraints.ini"
        data = ini_reader.read(ini_file_path)
        for section in data:
            data[section]["group"] = "default"
        ini_writer.write(data, ini_file_path)

        # Add properties for thermal clusters in .ini file
        ini_files = study_dir.glob("input/thermal/clusters/*/list.ini")
        thermal_path = study_dir / Path("input/thermal/series")
        for ini_file_path in ini_files:
            data = ini_reader.read(ini_file_path)
            area_id = ini_file_path.parent.name
            for cluster in data:
                new_thermal_path = thermal_path / area_id / cluster.lower()
                (new_thermal_path / "CO2Cost.txt").touch()
                (new_thermal_path / "fuelCost.txt").touch()
                data[cluster]["costgeneration"] = "SetManually"
                data[cluster]["efficiency"] = 100
                data[cluster]["variableomcost"] = 0
            ini_writer.write(data, ini_file_path)
