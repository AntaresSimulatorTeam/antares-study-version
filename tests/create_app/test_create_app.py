import datetime
import re
from pathlib import Path
from unittest import mock
import configparser

import pytest

from antares.study.version import StudyVersion
from antares.study.version.create_app import TEMPLATES_BY_VERSIONS, CreateApp
from antares.study.version.exceptions import ApplicationError

AVAILABLE_VERSIONS = list(TEMPLATES_BY_VERSIONS)


class TestCreateApp:
    def test_no_template_available(self, tmp_path: Path):
        study_dir = tmp_path.joinpath("my-new-study")
        study_version = StudyVersion.parse("2.8")
        app = CreateApp(study_dir=study_dir, caption="My New App", version=study_version, author="Robert Smith")
        with pytest.raises(ApplicationError, match=re.escape(f"{study_version:2d}")):
            app()

    @pytest.mark.parametrize("study_version", AVAILABLE_VERSIONS)
    def test_create_app(self, tmp_path: Path, study_version: StudyVersion):
        study_dir = tmp_path.joinpath("my-new-study")
        app = CreateApp(study_dir=study_dir, caption="My New App", version=study_version, author="Robert Smith")
        app()

        study_antares_file = study_dir / "study.antares"
        ini_reader = configparser.ConfigParser()
        ini_reader.read(study_antares_file, encoding="utf-8")
        properties = ini_reader["antares"]
        expected_version = study_version
        assert properties == {
            "author": "Robert Smith",
            "caption": "My New App",
            "created": mock.ANY,
            "lastsave": mock.ANY,
            "version": expected_version,
        }

        created_date = datetime.datetime.fromtimestamp(int(properties["created"]))
        last_save_date = datetime.datetime.fromtimestamp(int(properties["lastsave"]))
        assert last_save_date == created_date
