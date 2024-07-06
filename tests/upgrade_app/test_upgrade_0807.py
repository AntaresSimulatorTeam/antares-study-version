from antares.study.version.upgrade_app.upgrader_0807 import UpgradeTo0807
from tests.conftest import StudyAssets
from tests.helpers import are_same_dir


def test_nominal_case(study_assets: StudyAssets):
    """
    Check that binding constraints and thermal folders are correctly modified
    """

    # upgrade the study
    UpgradeTo0807.upgrade(study_assets.study_dir)

    # compare input folders (bindings + thermals)
    actual_input_path = study_assets.study_dir.joinpath("input")
    expected_input_path = study_assets.expected_dir.joinpath("input")
    assert are_same_dir(actual_input_path, expected_input_path)


def test_empty_binding_constraints(study_assets: StudyAssets):
    """
    Check that binding constraints and thermal folders are correctly modified
    """

    # upgrade the study
    UpgradeTo0807.upgrade(study_assets.study_dir)

    # compare input folders (bindings + thermals)
    actual_input_path = study_assets.study_dir.joinpath("input")
    expected_input_path = study_assets.expected_dir.joinpath("input")
    assert are_same_dir(actual_input_path, expected_input_path)
