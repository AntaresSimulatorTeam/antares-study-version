import dataclasses
import datetime
import typing as t
from pathlib import Path

from antares.study.version.show_app import ShowApp
from antares.study.version.upgrade_app import scenarios

if t.TYPE_CHECKING:
    from antares.study.version import StudyVersion

STUDY_ANTARES_FILE_0600 = """\
[antares]
caption = Thermal fleet optimization
version = 6.0
created = 1246524135
lastsave = 1686128483
author = John Doe
"""


class TestShowApp:
    def test_study_antares(self, study_dir: Path) -> None:
        app = ShowApp(study_dir)
        actual = app.study_antares
        expected = {
            "author": "John Doe",
            "caption": "Thermal fleet optimization",
            "created_date": datetime.datetime(2009, 7, 2, 8, 42, 15),
            "last_save_date": datetime.datetime(2023, 6, 7, 9, 1, 23),
            "version": {"major": 9, "minor": 2, "patch": 0},
        }
        assert dataclasses.asdict(actual) == expected

    def test_available_upgrades(self, study_dir: Path) -> None:
        app = ShowApp(study_dir)
        actual = app.available_upgrades
        expected: t.List[StudyVersion] = []
        assert actual == expected

        # patch version
        study_antares_file = study_dir / "study.antares"
        study_antares_file.write_text(STUDY_ANTARES_FILE_0600)
        app = ShowApp(study_dir)
        actual = app.available_upgrades
        expected = list(meth.new for meth in scenarios.values())
        assert actual == expected
