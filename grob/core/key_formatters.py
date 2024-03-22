from typing import Any, Callable, List, Protocol, Type, TypeVar, Union, cast

from grob.core.errors import InvalidKeyFormatterError
from grob.core.parsers import MultiPartKey
from grob.core.tags import Tag
from grob.types import GroupKey, KeyPart

Self = TypeVar("Self", bound="FstringFormatter")


class KeyFormatter(Protocol):
    def __call__(self, key: MultiPartKey) -> GroupKey:
        pass


class FstringFormatter:
    def __init__(self, format_string: str) -> None:
        self.format_string = format_string

    def __call__(self, key: MultiPartKey) -> GroupKey:
        return GroupKey(self.format_string.format(**key))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, FstringFormatter) and self.format_string == other.format_string

    @classmethod
    def from_parts(cls: Type[Self], key_parts: List[KeyPart], sep: str = "_") -> Self:
        return cls(sep.join("{" + key_part + "}" for key_part in key_parts))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.format_string!r})"


def get_key_formatter(
    key_formatter: Union[str, Callable[[MultiPartKey], GroupKey], None], tags: List[Tag]
) -> KeyFormatter:
    if key_formatter is None:
        return _get_default_key_formatter(tags)
    elif isinstance(key_formatter, str):
        return FstringFormatter(key_formatter)
    elif not callable(key_formatter):
        raise InvalidKeyFormatterError(key_formatter)
    else:
        return cast(KeyFormatter, key_formatter)


def _get_default_key_formatter(tags: List[Tag]) -> KeyFormatter:
    # TODO: make it handle missing key parts
    key_parts = []
    for tag in tags:
        for key_part in getattr(tag.parser, "key_parts", []):
            if key_part not in key_parts:
                key_parts.append(key_part)
    return FstringFormatter.from_parts(key_parts)
