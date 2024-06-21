import re

# Invalid chars was taken from Antares Simulator (C++).
_sub_invalid_chars = re.compile(r"[^a-zA-Z0-9_(),& -]+").sub


def transform_name_to_id(name: str, lower: bool = True) -> str:
    """
    Transform a name into an identifier by replacing consecutive
    invalid characters by a single white space, and then whitespaces
    are striped from both ends.

    Valid characters are `[a-zA-Z0-9_(),& -]` (including space).

    Args:
        name: The name to convert.
        lower: The flag used to turn the identifier in lower case.
    """
    valid_id = _sub_invalid_chars(" ", name).strip()
    return valid_id.lower() if lower else valid_id
