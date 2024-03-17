from pathlib import Path
from typing import Dict, Iterable, Optional

from grob.types import KeyPart


class GrobError(Exception):
    pass


class InvalidTagError(GrobError):
    def __init__(self, tag_name: str, known_tags: Optional[Iterable[str]] = None) -> None:
        message = f"Tag '{tag_name}' is not recognized. "
        if known_tags:
            message += "Known tags are '" + "', '".join(known_tags) + "'."
        super().__init__(message)


class MissingKeyPartError(GrobError):
    def __init__(self, path: Path, key_parts: Dict[KeyPart, str], expected_parts: Iterable[str], tag_name: str) -> None:
        missing_parts = "', '".join(set(expected_parts) - key_parts.keys())
        existing_parts = "\n".join(f"- {part}={value!r}" for part, value in key_parts.items())
        if existing_parts:
            existing_parts = f"The following parts were extracted:\n{existing_parts}"
        else:
            existing_parts = "No parts were found in path."
        message = (
            f"Missing mandatory key parts '{missing_parts}' for file '{path}' and tag '{tag_name}'. {existing_parts}"
        )
        super().__init__(message)


class AmbiguousFileError(GrobError):
    def __init__(self, file_path: Path, other_file_path: Path, key: str, tag_name: str) -> None:
        message = (
            f"Found two different files for key '{key}' and tag '{tag_name}': {file_path} and {other_file_path}. "
            f"To fix this issue, either provide a more specific pattern for tag '{tag_name}' or mark it as accepting "
            f"multiple files with `--multiple {tag_name}` on the command-line and argument "
            f"`allow_multiple=['{tag_name}', ...]` on Python."
        )
        super().__init__(message)


class MissingTagError(GrobError):
    def __init__(self, tag_names: Iterable[str], key: str) -> None:
        tag_names = list(tag_names)
        missing_tags = "', '".join(tag_names)
        super().__init__(
            f"Tags '{missing_tags}' are missing for key '{key}'. To fix this issue, either provide a broader pattern"
            "to ensure files are found for all required tags, or mark them as non-mandatory with `--remove-on-missing "
            f"{' '.join(tag_names)}` on the command-line or `remove_on_missing=['{missing_tags}']` on Python."
        )
