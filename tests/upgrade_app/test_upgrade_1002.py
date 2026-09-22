from antares.study.version.model.general_data import GENERAL_DATA_PATH, GeneralData
from antares.study.version.upgrade_app.upgrader_1002 import UpgradeTo1002
from tests.conftest import StudyAssets
from tests.helpers import DEFAULT_IGNORES, are_same_dir


def test_nominal_case(study_assets: StudyAssets):
    """
    Check that the `include-reserves` optimization flag is added to `generaldata.ini`,
    that the deprecated `general` properties are removed, and that no other file is modified.
    """

    # upgrade the study
    UpgradeTo1002.upgrade(study_assets.study_dir)

    # compare generaldata.ini
    actual = GeneralData.from_ini_file(study_assets.study_dir)
    expected = GeneralData.from_ini_file(study_assets.expected_dir)
    assert actual == expected
    assert actual["optimization"]["include-reserves"] is False
    for key in ("intra-modal", "correlateddraws", "horizon", "readonly"):
        assert key not in actual["general"]

    # the upgrade only touches generaldata.ini: everything else must be untouched
    assert are_same_dir(
        study_assets.study_dir,
        study_assets.expected_dir,
        ignore=DEFAULT_IGNORES | {GENERAL_DATA_PATH.split("/")[-1]},
    )
