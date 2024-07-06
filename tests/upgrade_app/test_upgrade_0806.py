from antares.study.version.upgrade_app.upgrader_0806 import UpgradeTo0806
from tests.conftest import StudyAssets
from tests.helpers import are_same_dir


def test_nominal_case(study_assets: StudyAssets):
    """
    Check that 'st-storage' folder is created and filled.
    """

    # upgrade the study
    UpgradeTo0806.upgrade(study_assets.study_dir)

    # compare input folder
    actual_input_path = study_assets.study_dir.joinpath("input")
    expected_input_path = study_assets.expected_dir.joinpath("input")
    assert are_same_dir(actual_input_path, expected_input_path)
