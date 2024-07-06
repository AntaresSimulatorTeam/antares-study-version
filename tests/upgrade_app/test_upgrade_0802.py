from antares.study.version.ini_reader import IniReader
from antares.study.version.upgrade_app.upgrader_0802 import UpgradeTo0802
from tests.conftest import StudyAssets
from tests.helpers import are_same_dir


def test_nominal_case(study_assets: StudyAssets):
    """
    Check that `settings/generaldata.ini` is upgraded to version 820.
    """

    # upgrade the study
    UpgradeTo0802.upgrade(study_assets.study_dir)

    # compare generaldata.ini
    actual_path = study_assets.study_dir.joinpath("settings/generaldata.ini")
    actual = IniReader().read(actual_path)
    expected_path = study_assets.expected_dir.joinpath("settings/generaldata.ini")
    expected = IniReader().read(expected_path)
    assert actual == expected

    # compare links
    actual_link_path = study_assets.study_dir.joinpath("input/links")
    expected_link_path = study_assets.expected_dir.joinpath("input/links")
    assert are_same_dir(actual_link_path, expected_link_path)
