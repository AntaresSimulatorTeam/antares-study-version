from antares.study.version.ini_reader import IniReader
from antares.study.version.upgrade_app.upgrader_0701 import UpgradeTo0701
from tests.conftest import StudyAssets


def test_nominal_case(study_assets: StudyAssets):
    """
    Check that `settings/generaldata.ini` is upgraded to version 710.
    """

    # upgrade the study
    UpgradeTo0701.upgrade(study_assets.study_dir)

    # compare generaldata.ini
    actual_path = study_assets.study_dir.joinpath("settings/generaldata.ini")
    actual = IniReader().read(actual_path)
    expected_path = study_assets.expected_dir.joinpath("settings/generaldata.ini")
    expected = IniReader().read(expected_path)
    assert actual == expected
