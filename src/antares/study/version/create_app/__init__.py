import dataclasses
import datetime
import typing as t
import zipfile
from importlib.resources import contents, open_binary
from pathlib import Path

from antares.study.version.exceptions import ApplicationError
from antares.study.version.model.study_antares import StudyAntares
from antares.study.version.model.study_version import StudyVersion

_RESOURCES_PACKAGE = "antares.study.version.create_app.resources"


def get_template_version(template_name: str) -> StudyVersion:
    template_name = template_name.replace(".zip", "")
    version_str = template_name.split("_")[-1]  # 880.zip
    return StudyVersion.parse(version_str)


TEMPLATES_BY_VERSIONS: t.Dict[StudyVersion, str] = {
    get_template_version(name): name for name in contents(_RESOURCES_PACKAGE) if name.endswith(".zip")
}


def available_versions() -> t.List[str]:
    """
    Return a list of available template versions.

    Returns:
        A list of available template versions.
    """
    return [f"{ver:2d}" for ver in sorted(TEMPLATES_BY_VERSIONS)]


@dataclasses.dataclass
class CreateApp:
    """
    Create a new study.
    """

    study_dir: Path
    caption: str
    version: StudyVersion
    author: str

    def __post_init__(self):
        self.study_dir = Path(self.study_dir)
        self.caption = self.caption.strip()
        self.version = StudyVersion.parse(self.version)
        self.author = self.author.strip()
        if self.study_dir.exists():
            raise FileExistsError(f"Study directory already exists: '{self.study_dir}'")
        if not self.caption:
            raise ValueError("Caption cannot be empty")

    def __call__(self) -> None:
        try:
            template_name = TEMPLATES_BY_VERSIONS[self.version]
        except KeyError:
            msg = f"No available template for version {self.version}: available templates are {available_versions()}"
            raise ApplicationError(msg)
        print(f"Extracting template {template_name} to '{self.study_dir}'...")
        with open_binary(_RESOURCES_PACKAGE, template_name) as zip_file:
            with zipfile.ZipFile(zip_file, mode="r") as archive:
                archive.extractall(self.study_dir)

        creation_date = datetime.datetime.now()
        study_antares = StudyAntares(
            version=self.version,
            caption=self.caption,
            created_date=creation_date,
            last_save_date=creation_date,
            author=self.author,
        )
        print("Writing 'study.antares' file...")
        study_antares.to_ini_file(self.study_dir, update_save_date=False)
        print(f"Study '{self.caption}' created successfully.")
