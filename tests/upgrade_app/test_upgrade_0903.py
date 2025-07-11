from antares.study.version.model.general_data import GeneralData
from antares.study.version.upgrade_app.upgrader_0903 import UpgradeTo0903, upgrade_thematic_trimming
from tests.conftest import StudyAssets


def test_nominal_case(study_assets: StudyAssets):
    """
    Check that the files are correctly modified
    """

    # upgrade the study
    UpgradeTo0903.upgrade(study_assets.study_dir)

    # compare generaldata.ini
    actual = GeneralData.from_ini_file(study_assets.study_dir)
    expected = GeneralData.from_ini_file(study_assets.expected_dir)
    assert actual == expected


def test_filtering():
    # Setup
    data = {
        "variables selection": {
            "select_var +": ["lignite", "solar pv", "another_var"],
            "select_var -": ["nuclear", "wind offshore", "other_var"],
        }
    }
    expected_minus = ["other_var"]
    expected_plus = ["another_var", "DISPATCH. GEN.", "RENEWABLE GEN."]

    # Execute
    upgrade_thematic_trimming(data)

    # Verify
    result_minus = data["variables selection"]["select_var -"]
    result_plus = data["variables selection"]["select_var +"]
    assert result_minus == expected_minus, f"Test filtering failed: expected {expected_minus}, got {result_minus}"
    assert result_plus == expected_plus, f"Test filtering failed: expected {expected_plus}, got {result_plus}"


def test_special_handling_plus():
    # Test case with only thermal variables in "+"
    data = {
        "variables selection": {
            "select_var +": ["coal", "gas", "other_var"],
            "select_var -": [],
        }
    }
    expected_plus = ["other_var", "DISPATCH. GEN."]

    upgrade_thematic_trimming(data)
    result_plus = data["variables selection"]["select_var +"]
    assert result_plus == expected_plus, (
        f"Test special handling plus (thermal) failed: expected {expected_plus}, got {result_plus}"
    )

    # Test case with only renewable variables in "+"
    data = {
        "variables selection": {
            "select_var +": ["solar pv", "wind onshore", "other_var"],
            "select_var -": [],
        }
    }
    expected_plus = ["other_var", "RENEWABLE GEN."]

    upgrade_thematic_trimming(data)
    result_plus = data["variables selection"]["select_var +"]
    assert result_plus == expected_plus, (
        f"Test special handling plus (renewable) failed: expected {expected_plus}, got {result_plus}"
    )

    # Test case with both thermal and renewable variables in "+"
    data = {
        "variables selection": {
            "select_var +": ["coal", "solar pv", "other_var"],
            "select_var -": [],
        }
    }
    expected_plus = ["other_var", "DISPATCH. GEN.", "RENEWABLE GEN."]

    upgrade_thematic_trimming(data)
    result_plus = data["variables selection"]["select_var +"]
    assert result_plus == expected_plus, (
        f"Test special handling plus (both) failed: expected {expected_plus}, got {result_plus}"
    )


def test_mixed_cases():
    # Test case with mixed case variables
    data = {
        "variables selection": {
            "select_var -": ["Nuclear", "WiNd Offshore", "other_var"],
            "select_var +": ["Lignite", "SoLaR PV", "another_var"],
        }
    }
    expected_minus = ["other_var"]
    expected_plus = ["another_var", "DISPATCH. GEN.", "RENEWABLE GEN."]

    upgrade_thematic_trimming(data)
    result_minus = data["variables selection"]["select_var -"]
    result_plus = data["variables selection"]["select_var +"]
    assert result_minus == expected_minus, (
        f"Test mixed cases failed (minus): expected {expected_minus}, got {result_minus}"
    )
    assert result_plus == expected_plus, f"Test mixed cases failed (plus): expected {expected_plus}, got {result_plus}"


def test_empty_input():
    # Test case with empty input lists
    data = {
        "variables selection": {
            "select_var -": [],
            "select_var +": [],
        }
    }
    expected_minus = []
    expected_plus = []

    upgrade_thematic_trimming(data)
    result_minus = data["variables selection"]["select_var -"]
    result_plus = data["variables selection"]["select_var +"]
    assert result_minus == expected_minus, (
        f"Test empty input failed (minus): expected {expected_minus}, got {result_minus}"
    )
    assert result_plus == expected_plus, f"Test empty input failed (plus): expected {expected_plus}, got {result_plus}"


def test_no_removal_variables():
    # Test case with no variables to remove
    data = {
        "variables selection": {
            "select_var -": ["other_var1", "other_var2"],
            "select_var +": ["another_var1", "another_var2"],
        }
    }
    expected_minus = ["other_var1", "other_var2"]
    expected_plus = ["another_var1", "another_var2"]  # No special strings added

    upgrade_thematic_trimming(data)
    result_minus = data["variables selection"]["select_var -"]
    result_plus = data["variables selection"]["select_var +"]
    assert result_minus == expected_minus, (
        f"Test no removal variables failed (minus): expected {expected_minus}, got {result_minus}"
    )
    assert result_plus == expected_plus, (
        f"Test no removal variables failed (plus): expected {expected_plus}, got {result_plus}"
    )
