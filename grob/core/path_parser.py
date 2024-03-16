import re
from pathlib import Path
from typing import Dict, List, Optional, Pattern, Union

from grob.types import KeyPart


class PathParser:
    def __init__(self, pattern: Union[str, Pattern]) -> None:
        if isinstance(pattern, re.Pattern):
            self.pattern = None
            self.regex = pattern
        else:
            self.pattern = pattern
            self.regex = _convert_pattern_to_regex(pattern)
        self.key_parts = _get_named_parts(self.regex)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.pattern or self.regex}')"

    def __call__(self, path: Path) -> Optional[Dict[KeyPart, str]]:
        matches = self.regex.search(str(path))
        if not matches:
            return None
        return {KeyPart(key): value for key, value in matches.groupdict().items() if value is not None}


def _create_named_capturing_group(match_obj):
    name = match_obj["placeholder"]
    modifier = "" if match_obj["greedy"] else "?"
    optional = match_obj["optional"]
    return f"(?P<{name}>[^/]+{modifier}){optional}"


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
    pattern = pattern.replace(r"\*", "[^/]+")
    # Replace placeholders {name} by named capturing group (P<name>...)
    pattern = re.sub(
        r"\\{(?P<placeholder>[a-zA-Z_]\w*)(?P<greedy>!g)?\\}(?P<optional>\??)", _create_named_capturing_group, pattern
    )
    pattern += "$"
    regex = pattern
    return re.compile(regex)


def _get_named_parts(regex: Pattern) -> List[KeyPart]:
    return [KeyPart(part) for part in regex.groupindex]
