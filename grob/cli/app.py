"""Group different files together by extracting keys from their names and matching those keys together.

The simplest PATTERN is '*', which will match all files in ROOT_DIR. In that case, each "group" of files will comprise
a single file. A more useful PATTERN is 'a=A/{name}.*,b=B/{name}.*', which will match files from different directories A
and B based on their stems. The output could look like this:
{
    "file_1": {"a": "A/file_1.txt", "b": "B/file_1.log"},
    "file_2": {"a": "A/file_2.txt", "b": "B/file_2.log"},
    ...
}
Here, 'file_1' and 'file_2' are the _keys_, while 'a' and 'b' are the _tags_. More generally, PATTERN is a
comma-separated list of <tag>=<pattern> pairs, where <tag> is the name of the tag (e.g. 'a' or 'b') and <pattern>
describes where to find the files and how to extract a key from their paths.
"""

import argparse
import os
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Union

_TRUEISH_KEYWORDS = {"true", "yes", "all", "1"}
_FALSEISH_KEYWORDS = {"false", "no", "0", "none"}
RESERVED_KEYWORDS = frozenset(_TRUEISH_KEYWORDS | _FALSEISH_KEYWORDS)


def _cast_to_field_list(raw_list: Optional[List[str]], default: bool = False) -> Union[bool, List[str]]:
    if raw_list is None:
        return default
    if not raw_list or len(raw_list) == 1 and raw_list[0].lower() in {"true", "yes", "1", "all"}:
        return True
    if len(raw_list) == 1 and raw_list[0].lower() in {"false", "no", "0", "none"}:
        return False
    return raw_list


def create_parser() -> Callable[..., argparse.Namespace]:
    current_dir = Path(os.getcwd())
    parser = argparse.ArgumentParser(
        prog="grob",
        description=__doc__,
        allow_abbrev=False,
        add_help=False,
    )
    parser.add_argument(
        "spec",
        metavar="PATTERN",
        type=str,
        default="{name}.*",
        help="Pattern describing which tags are present and how to extract their keys.",
    )
    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR",
        nargs="?",
        type=Path,
        default=current_dir,
        help="Root directory where files are located.",
    )
    parser.add_argument(
        "--multiple",
        dest="multiple_allowed",
        nargs="*",
        default=None,
        metavar="TAG",
        help=(
            "List of tags that accept multiple files. By default, tags expect a single matching file for any given key."
            " When `--multiple` is passed, the tag will contain a list of paths, instead of a single path."
        ),
    )
    parser.add_argument(
        "--optional",
        dest="optional_tags",
        metavar="TAG",
        nargs="*",
        default=None,
        help=(
            "List of optional tags. If a group doesn't have one of these tags, the tag will be present with null value."
            " By default, all tags are mandatory."
        ),
    )
    parser.add_argument(
        "--remove-on-missing",
        metavar="TAG",
        nargs="*",
        default=None,
        help=(
            "List of strictly mandatory tags. If a group doesn't have one of these tags, it will be removed from the "
            "output."
        ),
    )
    parser.add_argument(
        "--fail-on-missing",
        metavar="TAG",
        nargs="*",
        default=None,
        help=(
            "List of mandatory tags. If a group doesn't have one of these tags, grob will fail with exit code 1. This "
            "is the default for all tags."
        ),
    )
    parser.add_argument(
        "--key",
        type=str,
        dest="key_pattern",
        metavar="PATTERN",
        default=None,
        help=(
            "Provide a custom pattern to build the group keys. It can (and should) use any of the placeholders "
            "contained in PATTERN: for example, if PATTERN is '**/{parent}/{name}.{ext}', --key could be "
            "'{parent}-{name}-{ext}'."
        ),
    )
    output_options = parser.add_argument_group(
        title="Output format", description="Controls how the output is formatted."
    )
    output_format = output_options.add_mutually_exclusive_group()
    output_format.add_argument(
        "--output-format",
        "-f",
        type=str,
        default="json",
        choices=["json", "jsonl", "human", "csv", "tsv"],
        help="Specify the output format. Default to 'json'.",
    )
    output_format.add_argument(
        "--json", "-j", action="store_const", const="json", dest="output_format", help="Output a JSON string."
    )
    output_format.add_argument(
        "--jsonl",
        "-l",
        action="store_const",
        const="jsonl",
        dest="output_format",
        help="Output a JSON Line string, i.e. each line is a valid JSON record.",
    )
    output_format.add_argument(
        "--human",
        "-h",
        action="store_const",
        const="human",
        dest="output_format",
        help="Output a human readable table.",
    )
    output_format.add_argument(
        "--csv",
        action="store_const",
        const="csv",
        dest="output_format",
        help=(
            "Output a CSV file, with one group per line and one tag per column. This format isn't recommended when "
            "using --multiple."
        ),
    )
    output_format.add_argument(
        "--tsv",
        action="store_const",
        const="tsv",
        dest="output_format",
        help=(
            "Output a TSV file, with one group per line and one tag per column. This format isn't recommended when "
            "using --multiple."
        ),
    )
    output_options.add_argument(
        "--no-squeeze",
        dest="squeeze",
        action="store_false",
        help=(
            "Never squeeze file groups, even if no named tag were provided. By default, when all groups only contain "
            "one file and no named tag were provided, the output is squeezed into a list of paths."
        ),
    )
    output_options.add_argument(
        "--no-list",
        dest="compress_to_list",
        action="store_false",
        help=(
            "Always return a dictionary, even if no key was provided. By default, if no named placeholder is used, "
            "assume the user isn't interested in the key, but only in the group themselves."
        ),
    )
    output_path_type = output_options.add_mutually_exclusive_group()
    output_path_type.add_argument(
        "--absolute",
        action="store_const",
        const="absolute",
        dest="output_path_anchor",
        help="Output absolute paths.",
    )
    output_path_type.add_argument(
        "--relative-to-cwd",
        action="store_const",
        const="cwd",
        dest="output_path_anchor",
        help="Output paths relative to current working directory.",
    )
    output_path_type.add_argument(
        "--relative-to-root",
        action="store_const",
        const="root",
        dest="output_path_anchor",
        help="Output paths relative to ROOT_DIR. This is the default.",
    )
    output_key = output_options.add_mutually_exclusive_group()
    output_key.add_argument(
        "--with-keys",
        "-k",
        action="store_true",
        dest="with_keys",
        default=True,
        help="Return group keys alongside the group themselves. This is the default.",
    )
    output_key.add_argument(
        "--without-keys",
        "-K",
        action="store_false",
        dest="with_keys",
        help="Return only the file groups, not their keys.",
    )
    parser.add_argument("--help", action="help", help="Show this help message and exit")
    parser.set_defaults(output_path_anchor="root")

    def parse_arguments(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
        parsed_args = parser.parse_args(args=args)
        for attr in ("multiple_allowed", "optional_tags", "fail_on_missing", "remove_on_missing"):
            setattr(parsed_args, attr, _cast_to_field_list(getattr(parsed_args, attr)))
        # TODO: ensure `optional_tags`, `fail_on_missing` and `remove_on_missing` have compatible values (i.e. they
        #  must not overlap)
        return parsed_args

    return parse_arguments


def main() -> None:
    arg_parser = create_parser()
    args = arg_parser()
    print(*(f"{k}={v}" for k, v in args.__dict__.items() if not k.startswith("_")))


if __name__ == "__main__":
    main()
