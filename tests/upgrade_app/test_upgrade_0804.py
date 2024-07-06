from antares.study.version.ini_reader import IniReader
from antares.study.version.upgrade_app.upgrader_0804 import UpgradeTo0804
from tests.conftest import StudyAssets


def test_nominal_case(study_assets: StudyAssets):
    """
    Check that `settings/generaldata.ini` is upgraded to version 840.
    """

    # upgrade the study
    UpgradeTo0804.upgrade(study_assets.study_dir)

    # compare generaldata.ini
    actual_path = study_assets.study_dir.joinpath("settings/generaldata.ini")
    actual = IniReader().read(actual_path)
    expected_path = study_assets.expected_dir.joinpath("settings/generaldata.ini")
    expected = IniReader().read(expected_path)
    assert actual == expected
