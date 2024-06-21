from antares.study.version.upgrade_app.upgrader_0702 import UpgradeTo0702
from conftest import StudyAssets
from helpers import are_same_dir


def test_nominal_case(study_assets: StudyAssets):
    """
    Check that `settings/generaldata.ini` is upgraded to version 720.
    """

    # upgrade the study
    UpgradeTo0702.upgrade(study_assets.study_dir)

    # compare folder
    assert are_same_dir(study_assets.study_dir, study_assets.expected_dir)
