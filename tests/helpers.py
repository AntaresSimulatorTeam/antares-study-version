import filecmp
import typing as t
from pathlib import Path

DEFAULT_IGNORES = frozenset(filecmp.DEFAULT_IGNORES) | {"study.ico"}


def are_same_dir(dir1: Path, dir2: Path, *, ignore: t.Collection[str] = DEFAULT_IGNORES) -> bool:
    """
    Compare two directories recursively.
    """

    dirs_cmp = filecmp.dircmp(dir1, dir2, ignore=list(ignore))
    if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0 or len(dirs_cmp.funny_files) > 0:
        return False

    # check files content ignoring newline character (to avoid crashing on Windows)
    for common_file in dirs_cmp.common_files:
        file_1 = dir1 / common_file
        file_2 = dir2 / common_file

        try:
            with open(file_1, mode="r", encoding="utf-8") as f1:
                with open(file_2, mode="r", encoding="utf-8") as f2:
                    content_1 = f1.read().splitlines(keepends=False)
                    content_2 = f2.read().splitlines(keepends=False)
                    if content_1 != content_2:
                        return False
        except UnicodeDecodeError:
            raise ValueError(f"File '{common_file}' is not UTF-8 encoded")

    # iter through common dirs recursively
    for common_dir in dirs_cmp.common_dirs:
        path_common_dir = Path(common_dir)
        new_dir1 = dir1 / path_common_dir
        new_dir2 = dir2 / path_common_dir
        if not are_same_dir(new_dir1, new_dir2):
            return False
    return True
