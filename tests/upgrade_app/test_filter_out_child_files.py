import typing as t

import pytest

from antares.study.version.upgrade_app import filter_out_child_files


@pytest.mark.parametrize(
    "files, expected",
    [
        ([], []),
        (
            ["document.txt", "document.txt", "document.txt"],
            ["document.txt"],
        ),
        (
            ["input", "input/other", "input/other/other"],
            ["input"],
        ),
        (
            ["input/other1.txt", "input/other2.txt"],
            ["input/other1.txt", "input/other2.txt"],
        ),
        (
            ["input/other1.txt", "input/other2.txt", "other3.txt"],
            ["input/other1.txt", "input/other2.txt", "other3.txt"],
        ),
    ],
)
def test_filter_out_child_files(files: t.List[str], expected: t.List[str]) -> None:
    assert filter_out_child_files(files) == expected
