import enum
from pathlib import Path
from typing import Callable, Dict, List, NewType, Optional, Pattern, Union

GroupKey = NewType("GroupKey", str)
"""Represents the key uniquely identifying a group of files."""

KeyPart = NewType("KeyPart", str)
"""Represents a named part of the key.

A key is usually obtained by joining key parts in a fixed order.
"""

TagName = NewType("TagName", str)
"""Represents a specific type of file within a group."""

Group = Dict[TagName, Union[Path, List[Path], None]]
"""Represents a group of files that share the same key, broken down by tag."""

TagSpec = Union[str, Pattern, Callable[[Path], str]]
"""Represents one tag in a group.

A `TagSpec` represents any object that a user can provide in order to declare a tag. Tags themselves have their own
representation in `grob`: `TagSpec` is simply the user-facing representation of this.
"""

Parser = Callable[[Path], Optional[Dict[KeyPart, str]]]
"""A callable that can be used to parse file paths in order to extract key parts."""


class OnMissing(enum.Enum):
    """Controls what happens when a tag is missing from a group of files.

    Attributes:
        ignore: set the tag to None
        skip: discard the group entirely
        fail: raise an error
    """

    ignore = "ignore"
    skip = "skip"
    fail = "fail"
