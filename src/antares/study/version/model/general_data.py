from pathlib import Path

from antares.study.version.ini_reader import IniReader
from antares.study.version.ini_writer import IniWriter

GENERAL_DATA_PATH = "settings/generaldata.ini"

DUPLICATE_KEYS = [
    "playlist_year_weight",
    "playlist_year +",
    "playlist_year -",
    "select_var -",
    "select_var +",
]


class GeneralData(dict):
    @classmethod
    def from_ini_file(cls, study_dir: Path) -> "GeneralData":
        reader = IniReader(special_keys=DUPLICATE_KEYS)
        ini_path = study_dir / GENERAL_DATA_PATH
        data = reader.read(ini_path)
        return cls(**data)

    def to_ini_file(self, study_dir: Path) -> None:
        writer = IniWriter(special_keys=DUPLICATE_KEYS)
        ini_path = study_dir / GENERAL_DATA_PATH
        writer.write(self, ini_path)
