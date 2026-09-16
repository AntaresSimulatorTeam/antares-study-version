from antares.study.version.model.general_data import GeneralData
from antares.study.version.upgrade_app.upgrader_1002 import upgrade_general_data


def test_adds_include_reserves_flag():
    data = GeneralData({"optimization": {"simplex-range": "week"}})

    upgrade_general_data(data)

    assert data["optimization"]["include-reserves"] is False
    assert data["optimization"]["simplex-range"] == "week"


def test_preserves_existing_value_and_creates_missing_section():
    data = GeneralData({"optimization": {"include-reserves": True}})
    upgrade_general_data(data)
    assert data["optimization"]["include-reserves"] is True

    data = GeneralData()
    upgrade_general_data(data)
    assert data["optimization"]["include-reserves"] is False
