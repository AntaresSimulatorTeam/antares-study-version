from antares.study.version.ini_reader import IniReader
from antares.study.version.upgrade_app.upgrader_0803 import UpgradeTo0803
from tests.conftest import StudyAssets
from tests.helpers import are_same_dir


def test_nominal_case(study_assets: StudyAssets):
    """
    Check that `settings/generaldata.ini` is upgraded to version 830.
    """

    # upgrade the study
    UpgradeTo0803.upgrade(study_assets.study_dir)

    # compare generaldata.ini
    actual_path = study_assets.study_dir.joinpath("settings/generaldata.ini")
    actual = IniReader().read(actual_path)
    expected_path = study_assets.expected_dir.joinpath("settings/generaldata.ini")
    expected = IniReader().read(expected_path)
    assert actual == expected

    # compare areas
    actual_area_path = study_assets.study_dir.joinpath("input/areas")
    expected_area_path = study_assets.expected_dir.joinpath("input/areas")
    assert are_same_dir(actual_area_path, expected_area_path)
