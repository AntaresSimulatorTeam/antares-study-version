from pathlib import Path

from antares.study.version.ini_reader import IniReader
from antares.study.version.ini_writer import IniWriter
from antares.study.version.model.study_version import StudyVersion

from .upgrade_method import UpgradeMethod


class UpgradeTo0808(UpgradeMethod):
    """
    This class upgrades the study from version 8.7 to version 8.8.
    """

    old = StudyVersion(8, 7)
    new = StudyVersion(8, 8)
    files = ["input/st-storage/clusters"]

    @classmethod
    def upgrade(cls, study_dir: Path) -> None:
        """
        Upgrades the study to version 8.8.

        Args:
            study_dir: The study directory.
        """
        st_storage_dir = study_dir / "input" / "st-storage" / "clusters"
        if not st_storage_dir.exists():
            # The folder only exists for studies in v8.6+ that have some short term storage clusters.
            # For every other case, this upgrader has nothing to do.
            return

        reader = IniReader()
        writer = IniWriter()
        cluster_files = st_storage_dir.glob("*/list.ini")
        for file_path in cluster_files:
            sections = reader.read(file_path)
            for section in sections.values():
                section["enabled"] = True
            writer.write(sections, file_path)
