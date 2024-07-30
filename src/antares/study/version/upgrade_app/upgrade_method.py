import typing as t
from pathlib import Path

from antares.study.version.model.study_version import StudyVersion


class UpgradeMethod:
    """Raw study upgrade method (old version, new version, upgrade function)."""

    old: StudyVersion = StudyVersion(0, 0)
    new: StudyVersion = StudyVersion(0, 0)
    files: t.Sequence[str] = ()
    should_denormalize: bool = False

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return (
            f"<{cls}("
            f"old={self.old!r}, "
            f"new={self.new!r}, "
            f"files={self.files!r}, "
            f"should_denormalize={self.should_denormalize!r})>"
        )

    def __str__(self) -> str:
        return f"Upgrade Study v{self.old:2d} -> v{self.new:2d}"

    def __post_init__(self):
        self.old = StudyVersion.parse(self.old)
        self.new = StudyVersion.parse(self.new)

    def can_upgrade(self, version: StudyVersion) -> bool:
        return self.old <= version < self.new

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to the new version.

        Args:
            study_dir: The study directory.
        """
        raise NotImplementedError
