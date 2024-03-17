from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

from grob.core.files import find_by_tag, group_by_key
from grob.core.group_validation import filter_and_validate_groups
from grob.core.key_formatters import get_key_formatter
from grob.core.output_formatters import FormattedGroups, format_groups
from grob.core.parsers import AnonymousParser, MultiPartKey
from grob.core.tags import Tag, create_tags
from grob.core.walker import walk
from grob.types import GroupKey, TagSpec


def find(
    specs: Union[TagSpec, Dict[str, TagSpec]],
    root_dir: Path,
    key_formatter: Union[str, Callable[[MultiPartKey], GroupKey], None],
    use_relative_paths: bool = False,
    squeeze: bool = True,
    with_keys: Optional[bool] = None,
    compress_to_list: bool = True,
) -> FormattedGroups:
    root_dir = root_dir.resolve()
    tags = create_tags(specs)
    with_keys = _update_with_keys(with_keys, allow_auto_keys=compress_to_list, tags=tags)
    key_formatter = get_key_formatter(key_formatter, tags=tags)
    files = walk(root_dir)
    files_by_tag = find_by_tag(files, tags)
    groups = group_by_key(files_by_tag, key_formatter=key_formatter)
    groups = filter_and_validate_groups(groups, tags=tags)
    return format_groups(
        groups,
        tag_names=[tag.name for tag in tags],
        relative_to=root_dir if use_relative_paths else None,
        squeeze=squeeze,
        with_keys=with_keys,
    )


def _update_with_keys(with_keys: Optional[bool], allow_auto_keys: bool, tags: List[Tag]) -> bool:
    if with_keys is not None:
        return with_keys
    can_compress = len(tags) == 1 and isinstance(tags[0].parser, AnonymousParser)
    if can_compress and allow_auto_keys:
        return False
    return True
