from pathlib import Path
from typing import Callable, Dict, Union

from grob.core.files import find_by_tag, group_by_key
from grob.core.group_validation import filter_and_validate_groups
from grob.core.key_formatters import get_key_formatter
from grob.core.output_formatters import format_groups
from grob.core.parsers import MultiPartKey
from grob.core.tags import create_tags
from grob.core.walker import walk
from grob.types import GroupKey, TagSpec


def find(
    specs: Union[TagSpec, Dict[str, TagSpec]],
    root_dir: Path,
    key_formatter: Union[str, Callable[[MultiPartKey], GroupKey], None],
    use_relative_paths: bool = False,
    squeeze: bool = True,
    with_keys: bool = True,
):
    root_dir = root_dir.resolve()
    tags = create_tags(specs)
    key_formatter = get_key_formatter(key_formatter, tags=tags)
    files = walk(root_dir)
    files_by_tag = find_by_tag(files, tags)
    groups = group_by_key(files_by_tag, key_formatter=key_formatter)
    groups = filter_and_validate_groups(groups, tags=tags)
    groups = format_groups(
        groups,
        tag_names=[tag.name for tag in tags],
        relative_to=root_dir if use_relative_paths else None,
        squeeze=squeeze,
        with_keys=with_keys,
    )
    return groups
