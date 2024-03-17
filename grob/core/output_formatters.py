from pathlib import Path
from typing import Dict, List, Mapping, Optional, Union

from grob.types import Group, GroupKey, TagName

SqueezedGroup = Union[Path, List[Path], None]
FormattedGroup = Union[Group, SqueezedGroup]
FormattedGroups = Union[List[FormattedGroup], Mapping[GroupKey, FormattedGroup]]


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
            for tag, files in group.items():
                if isinstance(files, list):
                    group[tag] = sorted(file.relative_to(relative_to) for file in files)
                elif files is not None:
                    group[tag] = files.relative_to(relative_to)
    formatted_groups: Mapping[GroupKey, FormattedGroup]
    if squeeze and len(tag_names) == 1:
        tag_name = tag_names[0]
        formatted_groups = {key: group.get(tag_name) for key, group in groups.items()}
    else:
        formatted_groups = groups
    formatted_groups = {key: formatted_groups[key] for key in sorted(formatted_groups)}
    if with_keys:
        return formatted_groups
    return list(formatted_groups.values())
