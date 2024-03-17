from typing import Dict, List

from grob.core.errors import MissingTagError
from grob.core.tags import Tag
from grob.types import Group, GroupKey, OnMissing


def filter_and_validate_groups(groups: Dict[GroupKey, Group], tags: List[Tag]) -> Dict[GroupKey, Group]:
    filtered_groups: Dict[GroupKey, Group] = {}
    all_tags = {tag.name for tag in tags}
    optional_tags = {tag.name for tag in tags if tag.on_missing == OnMissing.ignore}
    mandatory_tags = {tag.name for tag in tags if tag.on_missing == OnMissing.fail}
    default_group: Group = {
        tag.name: [] if tag.allow_multiple else None for tag in tags if tag.on_missing == OnMissing.ignore
    }

    # TODO: add a mode where all groups are processed (e.g. to display all invalid groups at once)
    #  could be useful for a --dry-run option
    for group_key, group in groups.items():
        missing_tags = all_tags - group.keys()
        if missing_tags.issubset(optional_tags):
            filtered_groups[group_key] = {**default_group, **group}
        elif missing_mandatory_tags := mandatory_tags & missing_tags:
            raise MissingTagError(tag_names=missing_mandatory_tags, key=group_key)
        else:
            # Remove the group from the outputs
            continue
    return filtered_groups
