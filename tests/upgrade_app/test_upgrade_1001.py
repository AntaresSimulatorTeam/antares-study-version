from pathlib import Path

from antares.study.version import StudyVersion
from antares.study.version.ini_reader import IniReader
from antares.study.version.upgrade_app import UpgradeApp

STUDY_ANTARES_FILE = """\
[antares]
caption = Thermal fleet optimization
version = 9.3
created = 1246524135
lastsave = 1686128483
author = John Doe
"""


def test_nominal_case(tmp_path: Path) -> None:
    """
    Check that upgrading from 9.3 to 10.1 only bumps the version number.

    The 9.3 -> 10.1 upgrade is a no-op on disk: only ``study.antares`` is updated.
    """
    study_dir = tmp_path / "My Study"
    study_dir.mkdir()
    (study_dir / "study.antares").write_text(STUDY_ANTARES_FILE)

    app = UpgradeApp(study_dir, version=StudyVersion(10, 1))  # type: ignore
    app()

    actual = IniReader().read(study_dir / "study.antares")
    assert str(actual["antares"]["version"]) == "10.1"
