import dataclasses
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Tuple, Union

from grob.core.errors import AmbiguousTagError
from grob.core.frozendict import frozendict
from grob.core.parsers import MultiPartKey
from grob.core.tags import DistributableTag, MultiPartTag, Tag
from grob.types import Group, GroupKey, KeyPart


@dataclasses.dataclass
class FileCollection:
    tag: Tag
    files: Dict[Union[GroupKey, MultiPartKey], Union[Path, List[Path]]] = dataclasses.field(default_factory=dict)

    def add_if_matches(self, file: Path) -> bool:
        key = self.tag.parser(file)
        if key is None:
            return False
        if self.tag.allow_multiple:
            # Typing this properly would require overloading (values are lists if `allow_multiple`, paths otherwise)
            self.files.setdefault(key, []).append(file)  # type: ignore[union-attr]
        elif key not in self.files:
            self.files[key] = file
        else:
            raise AmbiguousTagError(file, self.files[key], key=key, tag_name=self.tag.name)  # type: ignore[arg-type]
        return True


def find_by_tag(files: Iterable[Path], tags: List[Tag]) -> List[FileCollection]:
    """Find all files matching one of the provided tags.

    Args:
        files: iterator over paths to analyze
        tags: tags to search for

    Returns:
        for each input tag, a collection of files matching this tag. Note that a file can only belong to a single
            collection: when it first matches a tag, the search stops for this file. In other words, `tags` order
            matters: most specific tags should come first.
    """
    file_collections = [FileCollection(tag=tag) for tag in tags]
    for file in files:
        for collection in file_collections:
            added = collection.add_if_matches(file)
            if added:
                break
    return file_collections


def group_by_key(
    file_collections: List[FileCollection], key_formatter: Callable[[MultiPartKey], GroupKey]
) -> Dict[GroupKey, Group]:
    """Group files from different collections by common key.

    Args:
        file_collections: collection to join
        key_formatter: how to transform multipart keys into string keys

    Returns:
        a mapping from group key to tag name to file path(s). If a tag is marked with `allow_multiple=True`, it will
            contain a list of paths. Otherwise, it will contain a single path. Note that groups aren't validated:
            `group_by_key` doesn't guarantee that all manatory tags are present in each group.
    """
    multi_part_collections, distributable_collections, single_part_collections = _sort_collections_by_type(
        file_collections
    )
    groups: Dict[MultiPartKey, Group] = {}
    for collection in multi_part_collections:
        for key, path in collection.files.items():
            groups.setdefault(key, {})[collection.tag.name] = path  # type: ignore[arg-type]
    for collection in distributable_collections:
        for key, group in groups.items():
            join_key: frozendict[KeyPart, str] = frozendict(
                {
                    part: key[part]
                    for part in key.keys() - set(collection.tag.distribute_over)  # type: ignore[attr-defined]
                }
            )
            if join_key in collection.files:
                group[collection.tag.name] = collection.files[join_key]
    formatted_groups = {key_formatter(key_parts): group for key_parts, group in groups.items()}
    for collection in single_part_collections:
        for key, path in collection.files.items():
            formatted_groups.setdefault(key, {})[collection.tag.name] = path  # type: ignore[arg-type]
    return formatted_groups


def _sort_collections_by_type(
    file_collections: List[FileCollection]
) -> Tuple[List[FileCollection], List[FileCollection], List[FileCollection]]:
    # Return:
    # - first, regular tags (i.e. they don't need to be distributed)
    # - second, tags that require distribution (i.e. they only have a subset of all key parts)
    # - third, tags that return directly a formatted key (no key part)
    multi_part_collections = []
    distributable_collections = []
    single_part_collections = []
    for collection in file_collections:
        if isinstance(collection.tag, DistributableTag):
            distributable_collections.append(collection)
        elif isinstance(collection.tag, MultiPartTag):
            multi_part_collections.append(collection)
        else:
            single_part_collections.append(collection)
    distributable_collections = sorted(
        distributable_collections,
        key=lambda collection: len(collection.tag.parser.key_parts),  # type: ignore[union-attr]
    )
    return multi_part_collections, distributable_collections, single_part_collections
