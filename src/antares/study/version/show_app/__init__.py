import dataclasses
import functools
import typing as t
from pathlib import Path

from antares.study.version import StudyVersion
from antares.study.version.exceptions import ApplicationError
from antares.study.version.model.exceptions import ValidationError
from antares.study.version.model.study_antares import StudyAntares
from antares.study.version.upgrade_app.scenario_mapping import scenarios


@dataclasses.dataclass
class ShowApp:
    """
    Show the details of a study in human-readable format (name, version, creation date, etc.)
    """

    study_dir: Path

    def __post_init__(self):
        self.study_dir = Path(self.study_dir)
        if not self.study_dir.exists():
            raise FileNotFoundError(f"Study directory not found: {self.study_dir}")

    @functools.cached_property
    def study_antares(self) -> StudyAntares:
        try:
            return StudyAntares.from_ini_file(self.study_dir)
        except ValidationError as e:
            raise ApplicationError(str(e)) from e

    @property
    def available_upgrades(self) -> t.List[StudyVersion]:
        try:
            start = self.study_antares.version
            end = scenarios[-1].new  # type: ignore
            update_methods = scenarios[start:end]  # type: ignore
        except KeyError:
            return []
        else:
            return [meth.new for meth in update_methods]  # type: ignore

    def __call__(self, file: t.Optional[t.TextIO] = None):
        study_antares = self.study_antares
        try:
            available_upgrades = ", ".join(f"v{ver:2d}" for ver in self.available_upgrades)
        except ApplicationError:
            available_upgrades = "None"
        print(str(study_antares), file=file)
        print(f"Available Upgrades: {available_upgrades}", file=file)
