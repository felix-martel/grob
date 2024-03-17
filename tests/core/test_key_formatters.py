import re

import pytest

from grob.core.key_formatters import FstringFormatter, get_key_formatter
from grob.core.tags import create_tags


def test_get_key_formatter_with_callable():
    formatter = get_key_formatter(str, [])
    assert formatter is str


def test_get_key_formatter_with_string():
    formatter = get_key_formatter("{a}_{b}-{c}", [])
    assert formatter == FstringFormatter("{a}_{b}-{c}")


@pytest.mark.parametrize(
    "tag_specs, expected_formatter",
    [
        ("{a}_{b}", FstringFormatter("{a}_{b}")),
        ({"t1": "{z}_{x}", "t2": "{z}_{y}"}, FstringFormatter("{z}_{x}_{y}")),
        (re.compile(r"(?P<foo>.*)"), FstringFormatter("{foo}")),
        ({"tag1": {"spec": "_".split, "key_parts": ["b", "a"]}}, FstringFormatter("{b}_{a}")),
    ],
)
def test_get_key_formatter_from_tags(tag_specs, expected_formatter):
    formatter = get_key_formatter(None, create_tags(tag_specs))
    assert formatter == expected_formatter
