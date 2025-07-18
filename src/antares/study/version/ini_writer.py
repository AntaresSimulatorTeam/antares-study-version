import ast
import configparser
import typing as t
from pathlib import Path

JSON = dict[str, t.Any]


class IniConfigParser(configparser.RawConfigParser):
    def __init__(self, special_keys: t.Optional[list[str]] = None) -> None:
        super().__init__()
        self.special_keys = special_keys

    # noinspection SpellCheckingInspection
    def optionxform(self, optionstr: str) -> str:
        return optionstr

    def _write_line(  # type:ignore
        self,
        delimiter,
        fp,
        key,
        section_name,
        value,
    ) -> None:
        value = self._interpolation.before_write(  # type:ignore
            self, section_name, key, value
        )
        if value is not None or not self._allow_no_value:  # type:ignore
            value = delimiter + str(value).replace("\n", "\n\t")
        else:
            value = ""
        fp.write(f"{key}{value}\n")

    def _write_section(  # type:ignore
        self,
        fp,
        section_name,
        section_items,
        delimiter,
    ) -> None:
        """Write a single section to the specified `fp`."""
        fp.write(f"[{section_name}]\n")
        for key, value in section_items:
            if self.special_keys and key in self.special_keys and isinstance(ast.literal_eval(value), list):
                for sub_value in ast.literal_eval(value):
                    self._write_line(delimiter, fp, key, section_name, sub_value)
            else:
                self._write_line(delimiter, fp, key, section_name, value)
        fp.write("\n")


class IniWriter:
    """
    Standard INI writer.
    """

    def __init__(self, special_keys: t.Optional[list[str]] = None):
        self.special_keys = special_keys

    def write(self, data: JSON, path: Path) -> None:
        """
        Write `.ini` file from JSON content

        Args:
            data: JSON content.
            path: path to `.ini` file.
        """
        config_parser = IniConfigParser(special_keys=self.special_keys)
        config_parser.read_dict(data)
        with path.open("w") as fp:
            config_parser.write(fp)


class SimpleKeyValueWriter(IniWriter):
    """
    Simple key/value INI writer.
    """

    def write(self, data: JSON, path: Path) -> None:
        """
        Write `.ini` file from JSON content

        Args:
            data: JSON content.
            path: path to `.ini` file.
        """
        with path.open("w") as fp:
            for key, value in data.items():
                if value is not None:
                    fp.write(f"{key}={value}\n")
