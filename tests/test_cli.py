import os
from pathlib import Path

import pytest

from grob.cli.app import create_parser


@pytest.mark.parametrize(
    "args, attrs",
    [
        (".", {"spec": ".", "root_dir": Path(os.getcwd())}),
        (". .", {"spec": ".", "root_dir": Path(".")}),
        (". . --json", {"output_format": "json"}),
        (". . -j", {"output_format": "json"}),
        (". . --jsonl", {"output_format": "jsonl"}),
        (". . -l", {"output_format": "jsonl"}),
        (". . --human", {"output_format": "human"}),
        (". . -h", {"output_format": "human"}),
        (". . --csv", {"output_format": "csv"}),
        (". . --tsv", {"output_format": "tsv"}),
        (". . -f csv", {"output_format": "csv"}),
        (". . --output-format csv", {"output_format": "csv"}),
        (". .", {"squeeze": True}),
        (". . --no-squeeze", {"squeeze": False}),
        (". .", {"compress_to_list": True}),
        (". . --no-list", {"compress_to_list": False}),
        (". . --multiple a b c", {"multiple_allowed": ["a", "b", "c"]}),
        (". . --multiple all", {"multiple_allowed": True}),
        (". . --multiple", {"multiple_allowed": True}),
        (". . --multiple false", {"multiple_allowed": False}),
        (". . --multiple 0", {"multiple_allowed": False}),
        (". . --multiple no", {"multiple_allowed": False}),
        (". . --multiple none", {"multiple_allowed": False}),
        (". . --multiple yes", {"multiple_allowed": True}),
        (". . --multiple 1", {"multiple_allowed": True}),
        (". . --multiple true", {"multiple_allowed": True}),
        (". . --optional a b c", {"optional_tags": ["a", "b", "c"]}),
        (". . --optional all", {"optional_tags": True}),
        (". . --optional", {"optional_tags": True}),
        (". . --optional false", {"optional_tags": False}),
        (". . --optional 0", {"optional_tags": False}),
        (". . --optional no", {"optional_tags": False}),
        (". . --optional none", {"optional_tags": False}),
        (". . --optional yes", {"optional_tags": True}),
        (". . --optional 1", {"optional_tags": True}),
        (". . --optional true", {"optional_tags": True}),
        (". . --fail-on-missing a b c", {"fail_on_missing": ["a", "b", "c"]}),
        (". . --fail-on-missing all", {"fail_on_missing": True}),
        (". . --fail-on-missing", {"fail_on_missing": True}),
        (". . --fail-on-missing false", {"fail_on_missing": False}),
        (". . --fail-on-missing 0", {"fail_on_missing": False}),
        (". . --fail-on-missing no", {"fail_on_missing": False}),
        (". . --fail-on-missing none", {"fail_on_missing": False}),
        (". . --fail-on-missing yes", {"fail_on_missing": True}),
        (". . --fail-on-missing 1", {"fail_on_missing": True}),
        (". . --fail-on-missing true", {"fail_on_missing": True}),
        (". . --remove-on-missing all", {"remove_on_missing": True}),
        (". . --remove-on-missing", {"remove_on_missing": True}),
        (". . --remove-on-missing false", {"remove_on_missing": False}),
        (". . --remove-on-missing 0", {"remove_on_missing": False}),
        (". . --remove-on-missing no", {"remove_on_missing": False}),
        (". . --remove-on-missing none", {"remove_on_missing": False}),
        (". . --remove-on-missing yes", {"remove_on_missing": True}),
        (". . --remove-on-missing 1", {"remove_on_missing": True}),
        (". . --remove-on-missing true", {"remove_on_missing": True}),
        (". .", {"with_keys": None}),
        (". . --with-keys", {"with_keys": True}),
        (". . -k", {"with_keys": True}),
        (". . --without-keys", {"with_keys": False}),
        (". . -K", {"with_keys": False}),
        (". . --key foo_{bar}_{index}", {"key_formatter": "foo_{bar}_{index}"}),
        (". .", {"key_formatter": None}),
        (". . --absolute", {"use_relative_path": False}),
        (". . --relative", {"use_relative_path": True}),
        (". .", {"use_relative_path": False}),
    ],
)
def test_create_parser(args, attrs):
    parser = create_parser()
    args = parser(args.split())
    for attr, expected_value in attrs.items():
        assert getattr(args, attr) == expected_value
