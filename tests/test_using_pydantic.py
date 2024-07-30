import datetime
import json
import typing as t
import uuid
from unittest import mock

import freezegun
from pydantic import BaseModel, Field, field_validator

from antares.study.version import StudyVersion


class StudyDTO(BaseModel):
    id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
    name: str
    version: StudyVersion
    created: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc))

    @field_validator("version", mode="before")
    def _validate_version(cls, v: t.Any) -> StudyVersion:
        return StudyVersion.parse(v)


class TestPydanticStudyVersion:
    def test_init(self) -> None:
        study = StudyDTO(name="foo", version=StudyVersion(4, 5))
        assert study.name == "foo"
        assert study.version.major == 4
        assert study.version.minor == 5
        assert study.version.patch == 0
        assert study.version == StudyVersion(4, 5, 0)

    def test_init_with_string(self) -> None:
        obj = {"name": "foo", "version": "4.5"}
        study = StudyDTO(**obj)  # type: ignore
        assert study.name == "foo"
        assert study.version.major == 4
        assert study.version.minor == 5
        assert study.version.patch == 0
        assert study.version == StudyVersion(4, 5, 0)

    @freezegun.freeze_time("2024-12-31 12:30")
    def test_to_json(self) -> None:
        with mock.patch("uuid.uuid4", return_value=uuid.UUID("4930a577-63d2-4ea9-b0b9-581110d97475")):
            study = StudyDTO(name="foo", version=StudyVersion(4, 5))
        result = study.model_dump_json()
        assert isinstance(result, str)
        # Compare dicts, since the order of the keys is not guaranteed
        assert json.loads(result) == {
            "created": "2024-12-31T12:30:00Z",
            "id": "4930a577-63d2-4ea9-b0b9-581110d97475",
            "name": "foo",
            "version": {"major": 4, "minor": 5, "patch": 0},
        }

    def test_from_dict(self) -> None:
        obj = {"name": "foo", "version": {"major": 4, "minor": 5}}
        study = StudyDTO(**obj)  # type: ignore
        assert study.name == "foo"
        assert study.version == StudyVersion(4, 5)
