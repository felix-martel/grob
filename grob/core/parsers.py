import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Match, Optional, Pattern, Protocol, Union

from grob.core.errors import InvalidFlagError
from grob.core.frozendict import frozendict
from grob.types import GroupKey, KeyPart

# TODO: replace this by a protocol (a union of `Mapping` and `Hashable`)
MultiPartKey = frozendict[KeyPart, str]
REGEX_FLAG: str = ":r"


class SinglePartParserProtocol(Protocol):
    """Parser that can parse a path into a string key.

    A _key_ is a string identifying the group the file belongs to. All files with the same key will be added to the
    same group of files. Whenever possible, prefer multipart parsers and multipart keys over string keys.
    """

    def __call__(self, path: Path) -> Optional[GroupKey]:
        pass


class MultiPartParserProtocol(Protocol):
    """Parser that can parse a path into a multipart key.

    A _multipart key_ is a mapping from part names to values, e.g. `{"parent": "foo", "extension": "json"}`. These
    different parts can be merged together to build the actual, user-facing key. Multipart keys enable extra
    features compare to regular string keys, most notably the option to distribute files over multiple groups.

    Multipart parsers must declare the list of key part names they can extract. When a key is extracted from a path,
    all parts must be present. Optional parts aren't supported.

    Multipart keys must be represented as `frozendict`, to ensure they are hashable. Any other mapping type supporting
    `__hash__` is supported.
    """

    key_parts: List[KeyPart]

    def __call__(self, path: Path) -> Optional[MultiPartKey]:
        pass


Parser = Union[MultiPartParserProtocol, SinglePartParserProtocol]


class CallableMultiPartParser:
    def __init__(self, func: Callable[[Path], Optional[Dict[str, str]]], key_parts: List[str]) -> None:
        self.func = func
        self.key_parts = [KeyPart(key_part) for key_part in key_parts]

    def __call__(self, path: Path) -> Optional[MultiPartKey]:
        key = self.func(path)
        if key is None:
            return None
        return frozendict(key)

    def __eq__(self, other: Any) -> bool:
        return all(
            [isinstance(other, CallableMultiPartParser), self.func == other.func, self.key_parts == other.key_parts]
        )


class AnonymousParser(CallableMultiPartParser):
    DEFAULT_PART_NAME: KeyPart = KeyPart("path")

    def __init__(self, regex: Pattern) -> None:
        super().__init__(
            func=lambda path: {"path": path.as_posix()} if regex.search(str(path)) else None,
            key_parts=[self.DEFAULT_PART_NAME],
        )


class CallableParser:
    def __init__(self, func: Callable[[Path], Optional[str]]) -> None:
        self.func = func

    def __call__(self, path: Path) -> Optional[GroupKey]:
        key = self.func(path)
        return GroupKey(key) if key is not None else None

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, CallableParser) and self.func == other.func


class PatternParser:
    def __init__(self, pattern: Union[str, Pattern]) -> None:
        if isinstance(pattern, re.Pattern):
            self.pattern = None
            self.regex = pattern
        elif pattern.endswith(REGEX_FLAG):
            self.pattern = None
            self.regex = re.compile(pattern[: -len(REGEX_FLAG)])
        else:
            self.pattern = pattern
            self.regex = _convert_pattern_to_regex(pattern)
        self.key_parts = _get_named_parts(self.regex)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.pattern or self.regex}')"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, PatternParser) and self.regex == other.regex

    def __call__(self, path: Path) -> Optional[MultiPartKey]:
        matches = self.regex.search(str(path))
        if not matches:
            return None
        return frozendict({KeyPart(key): value for key, value in matches.groupdict().items() if value is not None})


def _create_named_capturing_group(match_obj: Match) -> str:
    flags = match_obj["flags"] or ""
    if "d" in flags:
        content = r"\d"
    elif "a" in flags:
        content = "[a-zA-Z0-9]"
    else:
        content = "[^/]"
    if length_constraints := re.search(r"(?P<min_length>\d+)\\-(?P<max_length>\d+)", flags):
        # Match a (possibly open-ended) range of characters
        length_constraint = "".join(
            ["{" + length_constraints["min_length"], ",", length_constraints["max_length"], "}"]
        )
    elif length_constraints := re.search(r"(?P<constraint>[><])?(?P<number>\d+)", flags):
        constraint = length_constraints["constraint"]
        number = length_constraints["number"]
        if constraint == ">":
            length_constraint = f"{{{number},}}"
        elif constraint == "<":
            length_constraint = f"{{,{number}}}"
        else:
            # Match a fixed number of characters
            length_constraint = f"{{{number}}}"
    else:
        # Match an arbitrary number of characters
        length_constraint = "+"
        if "g" not in flags and "a" not in flags and "d" not in flags:
            length_constraint += "?"
    unrecognized_flags = re.sub(r"[-agd<>\\:\d]", "", re.sub(r"(\d*)?-(\d*)?", "", flags))
    if unrecognized_flags:
        raise InvalidFlagError(flags, match_obj.string)
    name = match_obj["placeholder"]
    optional = match_obj["optional"]
    return f"(?P<{name}>{content}{length_constraint}){optional}"


def _convert_pattern_to_regex(pattern: str) -> Pattern:
    option_groups = []
    for group in re.findall(r"\([^/()]+(?:|[^/()]+)+\)", pattern):
        before = re.escape(group)
        after = "(?:" + "|".join(re.escape(option) for option in group[1:-1].split("|")) + ")"
        option_groups.append((before, after))
    # Unescape escaped parenthesis
    pattern = pattern.replace(r"\(", "(").replace(r"\)", ")")
    pattern = re.escape(pattern)
    for before, after in option_groups:
        pattern = pattern.replace(before, after)
    pattern = re.sub(r"(/)?\\\*\\\*(?(1)/?|/)", r"\1([^/]+/)*", pattern)
    pattern = pattern.replace(r"\*", "[^/]*")
    # Replace placeholders {name} by named capturing group (P<name>...)
    pattern = re.sub(
        r"\\{(?P<placeholder>[a-zA-Z_]\w*)(?P<flags>:[^}]+)?\\}(?P<optional>\??)",
        _create_named_capturing_group,
        pattern,
    )
    pattern += "$"
    regex = pattern
    return re.compile(regex)


def _get_named_parts(regex: Pattern) -> List[KeyPart]:
    return [KeyPart(part) for part in regex.groupindex]
