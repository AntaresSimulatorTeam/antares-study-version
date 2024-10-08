"""
Antares Study (and Solver) version models.
"""

from .converters import version_to_triplet  # noqa: F401
from .model import SolverVersion, StudyVersion, SolverMinorVersion  # noqa: F401

__all__ = ("SolverVersion", "StudyVersion", "SolverMinorVersion")
