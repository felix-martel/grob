from typing import Any, List

from typing_extensions import Self

from grob.core.parsers import MultiPartKey
from grob.types import GroupKey, KeyPart


class FstringFormatter:
    def __init__(self, format_string: str) -> None:
        self.format_string = format_string

    def __call__(self, key: MultiPartKey) -> GroupKey:
        return GroupKey(self.format_string.format(**key))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, FstringFormatter) and self.format_string == other.format_string

    @classmethod
    def from_parts(cls, key_parts: List[KeyPart], sep: str = "_") -> Self:
        return FstringFormatter(sep.join("{" + key_part + "}" for key_part in key_parts))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.format_string!r})"
