import typing as t
from pathlib import Path

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
            ["input", str(Path("input").joinpath("other")), str(Path("input") / "other" / "other")],
            ["input"],
        ),
        (
            [str(Path("input") / "other1.txt"), str(Path("input") / "other2.txt")],
            [str(Path("input") / "other1.txt"), str(Path("input") / "other2.txt")],
        ),
        (
            [str(Path("input") / "other1.txt"), str(Path("input") / "other2.txt"), str(Path("input") / "other3.txt")],
            [str(Path("input") / "other1.txt"), str(Path("input") / "other2.txt"), str(Path("input") / "other3.txt")],
        ),
    ],
)
def test_filter_out_child_files(files: t.List[str], expected: t.List[str]) -> None:
    assert filter_out_child_files(files) == expected
