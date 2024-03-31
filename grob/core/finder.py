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
    patterns: Union[TagSpec, Dict[str, TagSpec]],
    root_dir: Union[str, Path],
    key_formatter: Union[str, Callable[[MultiPartKey], GroupKey], None] = None,
    use_relative_paths: bool = False,
    squeeze: bool = True,
    with_keys: Optional[bool] = None,
    compress_to_list: bool = True,
) -> FormattedGroups:
    """Find and group files together using glob-like patterns.

    A single pattern will create a tag with a default name:
    ```
    "data/image_{index}.png"
    ```
    will create groups `{"001": {"default": "data/image_001.png"}, "002": {"default": "data/image_002.png"}...}`.

    A dictionary will create one tag for each key in the dictionary. The values of the dictionary can be either a
    pattern, or a dictionary specifying tag-specific options, e.g.:
    ```
    {
        "image": "data/{year}/image_{index}.png",
        "legend": {
            "spec": "legends/legend_*_{year}_{index}.txt,
            "allow_multiple": True,
            "on_missing": "ignore",
        }
    }
    ```
    will create two tags `image` and `legend`, the latter being optional and accepting multiple files.

    Args:
        patterns: describes how to find and group files. It can be a single pattern (in which case a tag with a default
            name will be created) or a mapping from tag names to patterns. For tag-specific options (i.e. indicate what
            to do if a tag is missing from a group), a mapping from tag names to tag options can be provided
        root_dir: where to look for files. `root_dir` will be walked recursively
        key_formatter: specify how to format keys. By default, all key parts (such as `year` or `index` in the example
            above) are concatenated with underscores. `key_formatter` can be either a f-string or a function that takes
            a dictionary of parts (e.g. `{"year": 2020, "index": 1}`) and returns a string
        use_relative_paths: if True, return paths relative to `root_dir`. Otherwise, return absolute paths
        squeeze: if True, the output will be squeezed when possible (i.e. tag will be omitted from the output if it is
            not ambiguous)
        with_keys: whether to include the group keys in the output
        compress_to_list: if True, the value of `with_keys` will be automatically set from `patterns`. Ignored if
            `with_keys` is passed

    Returns:
        files matching `patterns`, grouped by common keys and tags
    """
    root_dir = Path(root_dir)
    root_dir = root_dir.resolve()
    tags = create_tags(patterns)
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
