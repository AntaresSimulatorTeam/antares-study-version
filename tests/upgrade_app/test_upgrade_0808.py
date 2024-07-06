from antares.study.version.upgrade_app.upgrader_0808 import UpgradeTo0808
from tests.conftest import StudyAssets
from tests.helpers import are_same_dir


def test_nominal_case(study_assets: StudyAssets):
    """
    Check that short term storages are correctly modified
    """

    # upgrade the study
    UpgradeTo0808.upgrade(study_assets.study_dir)

    # compare st-storage folders (st-storage)
    actual_input_path = study_assets.study_dir / "input" / "st-storage"
    expected_input_path = study_assets.expected_dir / "input" / "st-storage"
    assert are_same_dir(actual_input_path, expected_input_path)
