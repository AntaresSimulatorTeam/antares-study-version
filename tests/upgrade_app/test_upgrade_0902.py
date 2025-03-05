from antares.study.version.model.general_data import GeneralData
from antares.study.version.upgrade_app.upgrader_0902 import UpgradeTo0902
from tests.conftest import StudyAssets
from tests.helpers import are_same_dir


def test_nominal_case(study_assets: StudyAssets):
    """
    Check that the files are correctly modified
    """

    # upgrade the study
    UpgradeTo0902.upgrade(study_assets.study_dir)

    # compare generaldata.ini
    actual = GeneralData.from_ini_file(study_assets.study_dir)
    expected = GeneralData.from_ini_file(study_assets.expected_dir)
    assert actual == expected

    # compare st-storage folders (st-storage)
    actual_input_path = study_assets.study_dir / "input" / "st-storage"
    expected_input_path = study_assets.expected_dir / "input" / "st-storage"
    assert are_same_dir(actual_input_path, expected_input_path)
