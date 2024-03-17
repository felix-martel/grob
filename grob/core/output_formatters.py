from pathlib import Path
from typing import Dict, List, Optional, TypeAlias, Union

from grob.types import Group, GroupKey, TagName

SqueezedGroup: TypeAlias = Optional[str]
FormattedGroup: TypeAlias = Union[Group, SqueezedGroup]
FormattedGroups: TypeAlias = Union[List[FormattedGroup], Dict[GroupKey, FormattedGroup]]


def format_groups(
    groups: Dict[GroupKey, Group],
    tag_names: List[TagName],
    relative_to: Optional[Path] = None,
    squeeze: bool = True,
    with_keys: bool = True,
) -> FormattedGroups:
    if relative_to is not None:
        # Paths are absolute
        for group in groups.values():
            for tag in group:
                if isinstance(group[tag], list):
                    group[tag] = [path.relative_to(relative_to) if path is not None else path for path in group[tag]]
                else:
                    group[tag] = group[tag].relative_to(relative_to) if group[tag] is not None else group[tag]
    if squeeze and len(tag_names) == 1:
        tag_name = tag_names[0]
        groups = {key: group.get(tag_name) for key, group in groups.items()}
    if with_keys:
        return groups
    return list(groups.values())
