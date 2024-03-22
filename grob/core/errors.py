import textwrap
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Union

from grob.types import KeyPart

# TODO: add URL to documentation


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


class AmbiguousTagError(GrobError):
    def __init__(self, file_path: Path, other_file_path: Path, key: Union[str, Dict[str, str]], tag_name: str) -> None:
        message = textwrap.dedent(
            f"""\
            Found two different files for key {key} and tag '{tag_name}': {file_path} and {other_file_path}.
            To fix this issue, either provide a more specific pattern for tag '{tag_name}' or mark it as accepting
            multiple files with `--multiple {tag_name}` on the command-line and argument
            `allow_multiple=['{tag_name}', ...]` on Python.
            """
        )
        super().__init__(message)


class MissingTagError(GrobError):
    def __init__(self, tag_names: Iterable[str], key: str) -> None:
        tag_names = list(tag_names)
        message = textwrap.dedent(
            f"""\
            Tags '{"', '".join(tag_names)}' are missing for key '{key}'. To fix this issue, either provide a broader
            pattern to ensure files are found for all required tags, or mark them as non-mandatory with
            `--remove-on-missing {' '.join(tag_names)}` on the command-line or
            `remove_on_missing=['{"', '".join(tag_names)}']` on Python.
            """
        )
        super().__init__(message)


class InvalidKeyFormatterError(GrobError):
    def __init__(self, key_formatter: Any) -> None:
        message = textwrap.dedent(
            f"""\
            Invalid key formatter {key_formatter} of type {type(key_formatter)}. Key formatter can be either:
            - a format string, for example `{{a}}_{{b}}`
            - a callable, taking a dictionary of key parts and returning a string
            Key formatter can also be omitted entirely, in which case keys will be obtained by concatenating key parts
            with an underscore.
            """
        )
        super().__init__(message)


class InvalidTagSpecificationError(GrobError):
    def __init__(self, tag_spec: Any) -> None:
        if isinstance(tag_spec, dict) and "spec" not in tag_spec:
            error = "missing mandatory key `spec`"
        else:
            error = f"expected a dictionary object `{{'spec': <SPEC_PATTERN, ...}}`, got a {type(tag_spec)} instead"
        message = f"Invalid tag specification {tag_spec} of type {type(tag_spec)}: {error}"
        super().__init__(message)


class InvalidParserSpecificationError(GrobError):
    def __init__(self, parser_spec: Any) -> None:
        message = textwrap.dedent(
            f"""\
            "Invalid parser specification {parser_spec}. Parsers can be either:
            - a pattern string, such as `{{year}}/{{title}}/*.pdf
            - a callable, taking a file path as input and returning a key
            - a dictionary with a key `spec` containing a pattern string and a callable, as well as extra arguments
            """
        )
        super().__init__(message)


class InvalidFlagError(GrobError):
    def __init__(self, flags: str, pattern: str) -> None:
        message = textwrap.dedent(
            f"""\
            Invalid flag '{flags}' for pattern '{pattern}'. Supported flags are:
            - `a` and `d` for alphanumeric and digit, respectively
            - `g` for toggling greedy mode
            - `n:`, `n:m`, `:m` for length constraints, with `n` and `m` digits
            """
        )
        super().__init__(message)
