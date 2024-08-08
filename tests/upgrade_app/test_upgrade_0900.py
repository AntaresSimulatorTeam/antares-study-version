# from antares.study.version.upgrade_app.upgrader_0900 import UpgradeTo0900
from antares.study.version.upgrade_app import UpgradeApp
from antares.study.version import StudyVersion
from antares.study.version.ini_reader import IniReader
from tests.conftest import StudyAssets


def get_version(d):  # type: ignore
    """
    Extract version attribute from a nested dict structure
    """
    return d["antares"]["version"]


def test_nominal_case(study_assets: StudyAssets):
    """
    Check that short term storages are correctly modified
    """

    # upgrade the study
    app = UpgradeApp(study_assets.study_dir, version=StudyVersion(9, 0))  # type: ignore
    app()

    actual_path = study_assets.study_dir.joinpath("study.antares")
    actual = IniReader().read(actual_path)
    expected_path = study_assets.expected_dir.joinpath("study.antares")
    expected = IniReader().read(expected_path)
    # Check that antares.version attributes do match
    # We can't check the entire files because of attribute
    # antares.lastsave
    assert get_version(actual) == get_version(expected)
