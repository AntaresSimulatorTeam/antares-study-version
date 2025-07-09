from antares.study.version.ini_reader import IniReader
from antares.study.version.model.general_data import GeneralData
from antares.study.version.upgrade_app.upgrader_0903 import UpgradeTo0903
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
