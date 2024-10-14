import configparser
import dataclasses
import datetime
import textwrap
import typing as t
from pathlib import Path

from .exceptions import ValidationError
from .study_version import StudyVersion

STUDY_ANTARES_PATH = "study.antares"
DOTTED_VERSION = "9.0"


@dataclasses.dataclass(frozen=False, eq=False, order=False, unsafe_hash=False, init=True, repr=True)
class StudyAntares:
    """
    Object model which represents ``study.antares`` file.

    A ``study.antares`` file is a INI file containing the following section:

    ::

        [antares]
        caption = Thermal fleet optimization
        version = 9.2
        created = 1246524135
        lastsave = 1686128483
        author = John Doe

    Usage:

    >>> from antares.study.version.model.study_antares import StudyAntares

    >>> data = {
    ...     "caption": "Thermal fleet optimization",
    ...     "version": "9.2",
    ...     "created_date": 1246524135,
    ...     "last_save_date": 1686128483,
    ...     "author": "John Doe",
    ... }

    >>> study_antares = StudyAntares(**data)

    >>> study_antares.caption
    'Thermal fleet optimization'
    >>> study_antares.version
    StudyVersion(major=9, minor=2, patch=0)
    >>> study_antares.created_date
    datetime.datetime(2009, 7, 2, 10, 42, 15)
    >>> study_antares.last_save_date
    datetime.datetime(2023, 6, 7, 11, 1, 23)
    >>> study_antares.author
    'John Doe'

    >>> from pprint import pprint
    >>> pprint(study_antares.to_dict(), width=80)
    {'author': 'John Doe',
     'caption': 'Thermal fleet optimization',
     'created_date': 1246524135.0,
     'last_save_date': 1686128483.0,
     'version': '9.1'}
    """

    caption: str
    version: StudyVersion
    created_date: datetime.datetime
    last_save_date: datetime.datetime
    author: str

    # Conversion and validation methods
    # ---------------------------------

    def __post_init__(self) -> None:
        """
        Parse and validate the fields of the object.
        """
        errors = {}
        for field in dataclasses.fields(self):
            field_name = field.name
            val_method_name = f"_validate_{field_name}"
            val_method = getattr(self.__class__, val_method_name, None)
            if val_method is None:
                continue
            value = getattr(self, field_name)
            try:
                value = val_method(value)
            except (ValueError, TypeError) as error:
                errors[field_name] = str(error)
            else:
                setattr(self, field_name, value)
        if errors:
            raise ValidationError("Invalid 'study.antares' file", errors)

    @classmethod
    def _validate_caption(cls, value: t.Any) -> str:
        return str(value).strip()

    @classmethod
    def _validate_version(cls, value: t.Any) -> StudyVersion:
        return StudyVersion.parse(value)

    @classmethod
    def _validate_date(cls, value: t.Any) -> datetime.datetime:
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return datetime.datetime.utcnow()

        return datetime.datetime.utcfromtimestamp(value)

    _validate_created_date = _validate_date
    _validate_last_save_date = _validate_date

    # Serialization methods
    # ---------------------

    def to_dict(self) -> t.Dict[str, t.Any]:
        """
        Serialize the object to a dictionary.
        """
        return {
            "version": str(self.version),
            "caption": self.caption,
            "created_date": int(self.created_date.timestamp()),
            "last_save_date": int(self.last_save_date.timestamp()),
            "author": self.author,
        }

    @classmethod
    def from_ini_file(cls, study_dir: t.Union[str, Path]) -> "StudyAntares":
        """
        Parse a ``study.antares`` file and return a new instance of the object.

        Args:
            study_dir: Path to the study directory.

        Returns:
            A new instance of the object.
        """
        ini_path = Path(study_dir) / STUDY_ANTARES_PATH
        parser = configparser.ConfigParser()
        parser.read(ini_path, encoding="utf-8")
        section = parser["antares"]
        return cls(
            caption=section["caption"],
            version=StudyVersion.parse(section["version"]),
            created_date=section["created"],  # type: ignore
            last_save_date=section["lastsave"],  # type: ignore
            author=section["author"],
        )

    def to_ini_file(self, study_dir: t.Union[str, Path], update_save_date: bool = True) -> None:
        """
        Serialize the object to a ``study.antares`` file.

        Args:
            study_dir: Path to the study directory.
            update_save_date: If True, update the ``last_save_date`` field to the current date and time.
        """
        if update_save_date:
            self.last_save_date = datetime.datetime.now()

        section_dict = self.to_dict()

        if self.version < DOTTED_VERSION:  # type: ignore
            # Old versions of Antares Studies used a different format for the version number
            section_dict["version"] = f"{self.version:ddd}"
        else:
            section_dict["version"] = f"{self.version.major}.{self.version.minor}"

        section_dict["created"] = section_dict.pop("created_date")
        section_dict["lastsave"] = section_dict.pop("last_save_date")

        parser = configparser.ConfigParser()
        parser["antares"] = section_dict
        ini_path = Path(study_dir) / STUDY_ANTARES_PATH
        with ini_path.open(mode="w", encoding="utf-8") as file:
            parser.write(file)

    # Human-readable representation
    # -----------------------------

    def __str__(self) -> str:
        """
        Return a string representation of the object.
        """
        return textwrap.dedent(
            f"""\
            Caption: {self.caption}
            Version: v{self.version:2d}
            Created: {self.created_date:%Y-%m-%d %H:%M:%S}
            Last Save: {self.last_save_date:%Y-%m-%d %H:%M:%S}
            Author: {self.author}"""
        )
