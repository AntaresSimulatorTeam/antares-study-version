import typing as t
from pathlib import Path

import numpy as np
import numpy.typing as npt
import pandas

from antares.study.version.model.study_version import StudyVersion

from .exceptions import UnexpectedMatrixLinksError
from .upgrade_method import UpgradeMethod


class UpgradeTo0802(UpgradeMethod):
    """
    This class upgrades the study from version 8.1 to version 8.2.
    """

    old = StudyVersion(8, 1)
    new = StudyVersion(8, 2)
    files = ["input/links"]
    should_denormalize = True

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 8.2.

        Args:
            study_dir: The study directory.
        """
        links = (p for p in study_dir.glob("input/links/*") if p.is_dir())
        for folder_path in links:
            # Check if there are unresolved matrix links in the directory
            unresolved_link = next(iter(folder_path.glob("*.txt.link")), False)
            if isinstance(unresolved_link, Path):
                raise UnexpectedMatrixLinksError(unresolved_link.relative_to(study_dir).as_posix())

            all_txt = folder_path.glob("*.txt")
            for txt in all_txt:
                df = pandas.read_csv(txt, sep="\t", header=None)
                df_parameters = df.iloc[:, 2:8]
                df_direct = df.iloc[:, 0]
                df_indirect = df.iloc[:, 1]
                name = Path(txt).stem
                np.savetxt(
                    folder_path / f"{name}_parameters.txt",
                    t.cast(npt.NDArray[np.float64], df_parameters.values),
                    delimiter="\t",
                    fmt="%.6f",
                )
                (folder_path / "capacities").mkdir(exist_ok=True)
                np.savetxt(
                    folder_path / "capacities" / f"{name}_direct.txt",
                    t.cast(npt.NDArray[np.float64], df_direct.values),
                    delimiter="\t",
                    fmt="%.6f",
                )
                np.savetxt(
                    folder_path / "capacities" / f"{name}_indirect.txt",
                    t.cast(npt.NDArray[np.float64], df_indirect.values),
                    delimiter="\t",
                    fmt="%.6f",
                )
                (folder_path / f"{name}.txt").unlink()
