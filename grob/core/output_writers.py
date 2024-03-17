import csv
import json
from functools import partial
from itertools import zip_longest
from pathlib import Path
from typing import Any, Iterable, List, Literal, Protocol, TextIO, Union

from grob.core.output_formatters import FormattedGroups
from grob.types import TagName


def write_groups(
    groups: FormattedGroups,
    stream: TextIO,
    tag_names: List[TagName],
    output_format: Literal["json", "jsonl", "human", "csv", "tsv"] = "json",
) -> None:
    """Write groups to `stream` in the chosen format."""
    squeezed = _is_squeezed(groups)
    with_keys = _has_keys(groups)
    formatter = _FORMATTERS[output_format]()
    formatter(groups, stream, tag_names=tag_names, with_keys=with_keys, squeezed=squeezed)


class _PathJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Path):
            return obj.as_posix()
        return super().default(obj)


def _has_keys(groups: FormattedGroups) -> bool:
    return not isinstance(groups, list)


def _is_squeezed(groups: FormattedGroups) -> bool:
    is_squeezed_list = isinstance(groups, list) and groups and not isinstance(groups[0], dict)
    is_squeezed_dict = isinstance(groups, dict) and groups and not isinstance(next(iter(groups.values())), dict)
    return is_squeezed_dict or is_squeezed_list


class OutputFormatter(Protocol):
    def __call__(
        self,
        groups: FormattedGroups,
        stream: TextIO,
        tag_names: List[str],
        squeezed: bool = False,
        with_keys: bool = True,
    ):
        pass


class JsonOutputFormatter:
    def __call__(
        self,
        groups: FormattedGroups,
        stream: TextIO,
        tag_names: List[str],
        squeezed: bool = False,
        with_keys: bool = True,
    ) -> None:
        json.dump(groups, stream, cls=_PathJSONEncoder)


class JsonlOutputFormatter:
    def __call__(
        self,
        groups: FormattedGroups,
        stream: TextIO,
        tag_names: List[str],
        squeezed: bool = False,
        with_keys: bool = True,
    ) -> None:
        for record in self._iter_records(groups, squeezed=squeezed, with_keys=with_keys):
            stream.write(json.dumps(record, cls=_PathJSONEncoder) + "\n")

    @staticmethod
    def _iter_records(groups: FormattedGroups, squeezed: bool, with_keys: bool) -> Iterable[Any]:
        if with_keys:
            for key, group in groups.items():
                if squeezed:
                    yield {"key": key, "file": group}
                else:
                    yield {"key": key, "files": group}
        else:
            yield from groups


class TableOutputFormatter:
    def __init__(self, separator: str, line_terminator: str = "\n") -> None:
        self.delimiter = separator
        self.line_terminator = line_terminator

    def __call__(
        self,
        groups: FormattedGroups,
        stream: TextIO,
        tag_names: List[str],
        squeezed: bool = False,
        with_keys: bool = True,
    ) -> None:
        writer = csv.writer(stream, delimiter=self.delimiter, lineterminator=self.line_terminator)
        for row in self._iter_rows(groups, squeezed=squeezed, with_keys=with_keys, tag_names=tag_names):
            writer.writerow(row)

    def _iter_rows(
        self, groups: FormattedGroups, tag_names: List[str], squeezed: bool, with_keys: bool
    ) -> Iterable[List[str]]:
        # Don't yield header when output is squeezed to a single column and no keys are displayed
        if not squeezed or with_keys:
            header = ["files"] if squeezed else tag_names
            if with_keys:
                header = ["key", *header]

            yield header

        for key, group in groups.items() if with_keys else zip_longest([], groups):
            if squeezed:
                files = [self._format_path(group)]
            else:
                files = [self._format_path(group.get(tag_name, "")) for tag_name in tag_names]
            yield [key, *files] if with_keys else files

    @staticmethod
    def _format_path(path_or_paths: Union[str, Path, List[Path], List[str]]) -> str:
        paths = [path_or_paths] if not isinstance(path_or_paths, list) else path_or_paths
        formatted_paths = [path if isinstance(path, str) else path.as_posix() for path in paths if path is not None]
        return ", ".join(formatted_paths)


class HumanOutputFormatter(TableOutputFormatter):
    def __call__(
        self,
        groups: FormattedGroups,
        stream: TextIO,
        tag_names: List[str],
        squeezed: bool = False,
        with_keys: bool = True,
    ) -> None:
        raise NotImplementedError()


_FORMATTERS = {
    "human": HumanOutputFormatter,
    "json": JsonOutputFormatter,
    "jsonl": JsonlOutputFormatter,
    "csv": partial(TableOutputFormatter, separator=","),
    "tsv": partial(TableOutputFormatter, separator="\t"),
}
