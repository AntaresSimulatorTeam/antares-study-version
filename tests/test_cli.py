import configparser
import datetime
import typing as t
from pathlib import Path
from unittest import mock
from unittest.mock import ANY

import click
import pytest
from click.testing import CliRunner

from antares.study.version import StudyVersion
from antares.study.version.__about__ import __date__, __version__
from antares.study.version.cli import cli
from antares.study.version.create_app import TEMPLATES_BY_VERSIONS
from antares.study.version.ini_reader import IniReader
from tests.conftest import StudyAssets
from tests.helpers import are_same_dir


class TestCli:
    def test_cli__version(self) -> None:
        runner = CliRunner()
        result = runner.invoke(t.cast(click.BaseCommand, cli), ["--version"])
        assert result.exit_code == 0
        version_str = result.output.strip()
        assert version_str.startswith(f"v{__version__}")
        assert __date__ in version_str

    def test_cli__show(self, study_dir: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(t.cast(click.BaseCommand, cli), ["show", str(study_dir)])
        assert result.exit_code == 0
        show_str = result.output.strip()
        assert "Caption: Thermal fleet optimization" in show_str
        assert "Version: v9.2" in show_str
        assert "Created: 2009-07-02 08:42:15" in show_str
        assert "Last Save: 2023-06-07 09:01:23" in show_str
        assert "Author: John Doe" in show_str

    @pytest.mark.parametrize("study_version", list(TEMPLATES_BY_VERSIONS))
    def test_cli__create(self, tmp_path: Path, study_version: StudyVersion) -> None:
        now = datetime.datetime.now()

        study_dir = tmp_path / "My Study"
        runner = CliRunner()
        args = ["create", str(study_dir), f"--version={study_version:2d}", "--author=Jane Doe", "--caption=New Study"]
        result = runner.invoke(t.cast(click.BaseCommand, cli), args)
        assert result.exit_code == 0, result.output

        study_antares_file = study_dir / "study.antares"
        parser = configparser.ConfigParser()
        parser.read(study_antares_file, encoding="utf-8")
        section_dict = dict(parser["antares"])
        if study_version < 900:
            expected_version = f"{study_version:ddd}"
        else:
            expected_version = f"{study_version.major}.{study_version.minor}"

        expected = {
            "caption": "New Study",
            "version": expected_version,
            "created": ANY,
            "lastsave": ANY,
            "author": "Jane Doe",
        }
        assert expected == section_dict
        created_date = datetime.datetime.fromtimestamp(float(section_dict["created"]))
        last_save_date = datetime.datetime.fromtimestamp(float(section_dict["lastsave"]))
        one_sec = datetime.timedelta(seconds=1)
        assert now - one_sec <= created_date <= now + one_sec
        assert now - one_sec <= last_save_date <= now + one_sec

    def test_cli__create__versions(self) -> None:
        runner = CliRunner()
        args = ["create", "--versions"]
        result = runner.invoke(t.cast(click.BaseCommand, cli), args)
        assert result.exit_code == 0

        show_str = result.output.strip()
        assert "Available versions: 7.0, 7.1, 7.2, 8.0" in show_str

    def test_upgrade__nominal_case(self, study_assets: StudyAssets) -> None:
        runner = CliRunner()
        target_version = "8.8"
        result = runner.invoke(
            t.cast(click.BaseCommand, cli), ["upgrade", str(study_assets.study_dir), f"--version={target_version}"]
        )
        assert result.exit_code == 0

        # compare the content of the input directory
        actual_input_dir = study_assets.study_dir.joinpath("input")
        expected_input_dir = study_assets.expected_dir.joinpath("input")
        assert are_same_dir(actual_input_dir, expected_input_dir)

        ini_reader = IniReader()
        actual_antares_file = study_assets.study_dir / "study.antares"
        actual_antares = ini_reader.read(actual_antares_file, section="antares")
        assert actual_antares["antares"] == {
            "caption": "Thermal fleet",
            "version": 880,  # legacy version format
            "created": mock.ANY,
            "lastsave": mock.ANY,
            "author": "Robert Smith",
        }
