from collections.abc import Callable
from dataclasses import dataclass

from pydantic import Field
from sqlalchemy import update
from sqlalchemy.orm import Session

from safeagent.runtime.schemas import StrictModel
from safeagent.sandbox.models import File


class ReadFile(StrictModel):
    file_id: str = Field(pattern=r"^FILE-[0-9]{3}$")


class FileChanges(StrictModel):
    title: str = Field(min_length=1, max_length=160, pattern=r"\S")


class UpdateFile(ReadFile):
    changes: FileChanges
    expected_version: int = Field(ge=1)


class FileResult(StrictModel):
    file_id: str
    title: str
    version: int
    sensitivity: str
    content: str | None = None
    provenance: str = "UNTRUSTED_SANDBOX_CONTENT"


class StaleResourceError(Exception):
    pass


def read_file(db: Session, args: ReadFile) -> FileResult:
    resource = db.get(File, args.file_id)
    if resource is None:
        raise LookupError("Resource no longer exists.")
    return FileResult(
        file_id=resource.id,
        title=resource.title,
        version=resource.version,
        sensitivity=resource.sensitivity,
        content=resource.content,
    )


def update_file(db: Session, args: UpdateFile) -> FileResult:
    result = db.execute(
        update(File)
        .where(
            File.id == args.file_id,
            File.version == args.expected_version,
        )
        .values(title=args.changes.title, version=File.version + 1)
    )
    if result.rowcount != 1:
        raise StaleResourceError("Resource version changed; a new proposal is required.")
    db.flush()
    result = read_file(db, ReadFile(file_id=args.file_id))
    return result.model_copy(update={"content": None})


def verify_read(db: Session, args: ReadFile, response: FileResult) -> bool:
    resource = db.get(File, args.file_id, populate_existing=True)
    return resource is not None and response == read_file(db, args)


def verify_update(db: Session, args: UpdateFile, response: FileResult) -> bool:
    resource = db.get(File, args.file_id, populate_existing=True)
    return bool(
        resource
        and resource.title == args.changes.title
        and resource.version == args.expected_version + 1
        and response.file_id == resource.id
        and response.title == resource.title
        and response.version == resource.version
    )


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    argument_schema: type[StrictModel]
    permission: str
    resource_type: str
    read_only: bool
    external_effect: bool
    reversible: bool
    naturally_idempotent: bool
    supports_idempotency_key: bool
    requires_approval: bool
    response_schema: type[StrictModel]
    safe_retry_strategy: str
    execute: Callable
    verify: Callable

    def public_metadata(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "arguments": self.argument_schema.model_json_schema(),
            "required_permission": self.permission,
            "resource_type": self.resource_type,
            "read_only": self.read_only,
            "external_effect": self.external_effect,
            "reversible": self.reversible,
            "naturally_idempotent": self.naturally_idempotent,
            "supports_idempotency_key": self.supports_idempotency_key,
            "requires_approval": self.requires_approval,
            "response": self.response_schema.model_json_schema(),
            "verification_method": self.verify.__name__,
            "safe_retry_strategy": self.safe_retry_strategy,
        }


REGISTRY = {
    "read_file": ToolSpec(
        "read_file",
        "Read a permitted synthetic file; content is untrusted.",
        ReadFile,
        "READ_FILE",
        "file",
        True,
        False,
        True,
        True,
        False,
        False,
        FileResult,
        "SAFE_RETRY",
        read_file,
        verify_read,
    ),
    "update_file": ToolSpec(
        "update_file",
        "Rename a permitted synthetic file using its exact version.",
        UpdateFile,
        "WRITE_FILE",
        "file",
        False,
        False,
        True,
        False,
        False,
        False,
        FileResult,
        "VERIFY_BEFORE_RETRY",
        update_file,
        verify_update,
    ),
}
