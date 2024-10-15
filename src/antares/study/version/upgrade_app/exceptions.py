from typing import List


class UpgradeError(Exception):
    """
    Base class for exceptions in this module.
    """


class UnexpectedMatrixLinksError(UpgradeError):
    """
    Exception raised when there are unresolved matrix links in the directory.
    """

    def __init__(self, link_path: str):
        """
        Initialize the exception.

        Args:
            link_path: The relative path to the unresolved link.
        """
        message = (
            f"Found unexpected '{link_path}' file in the directory."
            f" The links must be resolved before the upgrade can be done using the denormalization mechanism"
            f" that allows to replace the matrix links by valid TSV matrices."
        )
        super().__init__(message)


class UnexpectedThematicTrimmingFieldsError(UpgradeError):
    """
    Exception raised when there are unexpected thematic trimming fields in the generaldata.ini file.
    """

    def __init__(self, enabled_fields: List[str], disabled_fields: List[str]):
        message = (
            f"Found these enabled fields {enabled_fields} with these disabled fields {disabled_fields} in the"
            f" generaldata.ini. We cannot determine if the new variable `STS by group` should be enabled or disabled."
            f" Choose one before upgrading your study."
        )
        super().__init__(message)
