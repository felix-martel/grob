import io
import json
import textwrap
from pathlib import Path

import pytest

from grob.core.output_writers import write_groups
from grob.types import GroupKey, TagName

T1 = TagName("T1")
T2 = TagName("T2")
T3 = TagName("T3")


@pytest.fixture
def two_tags():
    yield (
        {
            GroupKey("k1"): {T1: Path("k1_t1"), T2: Path("k1_t2")},
            GroupKey("k2"): {T1: Path("k2_t1"), T2: Path("k2_t2")},
            GroupKey("k3"): {T1: Path("k3_t1"), T2: Path("k3_t2")},
        },
        [T1, T2],
    )


@pytest.fixture
def single_tag():
    yield (
        {
            GroupKey("k1"): {T1: Path("k1_t1")},
            GroupKey("k2"): {T1: Path("k2_t1")},
            GroupKey("k3"): {T1: Path("k3_t1")},
        },
        [T1],
    )


@pytest.fixture
def squeezed_with_keys():
    yield (
        {
            GroupKey("k1"): Path("k1_t1"),
            GroupKey("k2"): Path("k2_t1"),
            GroupKey("k3"): Path("k3_t1"),
        },
        [T1],
    )


@pytest.fixture
def squeezed_without_keys():
    yield (
        [
            Path("k1_t1"),
            Path("k2_t1"),
            Path("k3_t1"),
        ],
        [T1],
    )


@pytest.fixture
def multiple_files_per_tag():
    yield (
        {
            GroupKey("k1"): {T1: Path("k1_t1"), T2: [Path("k1_t2"), Path("k1_t2_copy")]},
            GroupKey("k2"): {T1: Path("k2_t1"), T2: [Path("k2_t2"), Path("k2_t2_copy")]},
            GroupKey("k3"): {T1: Path("k3_t1"), T2: [Path("k3_t2"), Path("k3_t2_copy")]},
        },
        [T1, T2],
    )


@pytest.fixture
def multiple_files_per_tag_without_keys():
    yield (
        [
            {T1: Path("k1_t1"), T2: [Path("k1_t2"), Path("k1_t2_copy")]},
            {T1: Path("k2_t1"), T2: [Path("k2_t2"), Path("k2_t2_copy")]},
            {T1: Path("k3_t1"), T2: [Path("k3_t2"), Path("k3_t2_copy")]},
        ],
        [T1, T2],
    )


@pytest.mark.parametrize(
    "group, expected_result",
    [
        (
            "two_tags",
            {
                "k1": {"T1": "k1_t1", "T2": "k1_t2"},
                "k2": {"T1": "k2_t1", "T2": "k2_t2"},
                "k3": {"T1": "k3_t1", "T2": "k3_t2"},
            },
        ),
        (
            "single_tag",
            {
                "k1": {"T1": "k1_t1"},
                "k2": {"T1": "k2_t1"},
                "k3": {"T1": "k3_t1"},
            },
        ),
        (
            "squeezed_with_keys",
            {
                "k1": "k1_t1",
                "k2": "k2_t1",
                "k3": "k3_t1",
            },
        ),
        ("squeezed_without_keys", ["k1_t1", "k2_t1", "k3_t1"]),
        (
            "multiple_files_per_tag",
            {
                "k1": {"T1": "k1_t1", "T2": ["k1_t2", "k1_t2_copy"]},
                "k2": {"T1": "k2_t1", "T2": ["k2_t2", "k2_t2_copy"]},
                "k3": {"T1": "k3_t1", "T2": ["k3_t2", "k3_t2_copy"]},
            },
        ),
        (
            "multiple_files_per_tag_without_keys",
            [
                {"T1": "k1_t1", "T2": ["k1_t2", "k1_t2_copy"]},
                {"T1": "k2_t1", "T2": ["k2_t2", "k2_t2_copy"]},
                {"T1": "k3_t1", "T2": ["k3_t2", "k3_t2_copy"]},
            ],
        ),
    ],
)
def test_write_groups_with_json(group, expected_result, request):
    stream = io.StringIO()
    groups, tags = request.getfixturevalue(group)
    write_groups(
        groups=groups,
        stream=stream,
        tag_names=tags,
    )
    result = json.loads(stream.getvalue())
    assert result == expected_result


@pytest.mark.parametrize(
    "group, expected_result",
    [
        (
            "two_tags",
            [
                {"key": "k1", "files": {"T1": "k1_t1", "T2": "k1_t2"}},
                {"key": "k2", "files": {"T1": "k2_t1", "T2": "k2_t2"}},
                {"key": "k3", "files": {"T1": "k3_t1", "T2": "k3_t2"}},
            ],
        ),
        (
            "single_tag",
            [
                {"key": "k1", "files": {"T1": "k1_t1"}},
                {"key": "k2", "files": {"T1": "k2_t1"}},
                {"key": "k3", "files": {"T1": "k3_t1"}},
            ],
        ),
        (
            "squeezed_with_keys",
            [
                {"key": "k1", "file": "k1_t1"},
                {"key": "k2", "file": "k2_t1"},
                {"key": "k3", "file": "k3_t1"},
            ],
        ),
        ("squeezed_without_keys", ["k1_t1", "k2_t1", "k3_t1"]),
        (
            "multiple_files_per_tag",
            [
                {"key": "k1", "files": {"T1": "k1_t1", "T2": ["k1_t2", "k1_t2_copy"]}},
                {"key": "k2", "files": {"T1": "k2_t1", "T2": ["k2_t2", "k2_t2_copy"]}},
                {"key": "k3", "files": {"T1": "k3_t1", "T2": ["k3_t2", "k3_t2_copy"]}},
            ],
        ),
        (
            "multiple_files_per_tag_without_keys",
            [
                {"T1": "k1_t1", "T2": ["k1_t2", "k1_t2_copy"]},
                {"T1": "k2_t1", "T2": ["k2_t2", "k2_t2_copy"]},
                {"T1": "k3_t1", "T2": ["k3_t2", "k3_t2_copy"]},
            ],
        ),
    ],
)
def test_write_groups_with_jsonl(group, expected_result, request):
    stream = io.StringIO()
    groups, tags = request.getfixturevalue(group)
    write_groups(
        groups=groups,
        stream=stream,
        tag_names=tags,
        output_format="jsonl",
    )
    results = list(map(json.loads, stream.getvalue().splitlines()))
    assert results == expected_result


@pytest.mark.parametrize(
    "group, expected_result",
    [
        (
            "two_tags",
            textwrap.dedent(
                """\
                key,T1,T2
                k1,k1_t1,k1_t2
                k2,k2_t1,k2_t2
                k3,k3_t1,k3_t2
                """
            ),
        ),
        (
            "single_tag",
            textwrap.dedent(
                """\
                key,T1
                k1,k1_t1
                k2,k2_t1
                k3,k3_t1
                """
            ),
        ),
        (
            "squeezed_with_keys",
            textwrap.dedent(
                """\
                key,files
                k1,k1_t1
                k2,k2_t1
                k3,k3_t1
                """
            ),
        ),
        (
            "squeezed_without_keys",
            textwrap.dedent(
                """\
                k1_t1
                k2_t1
                k3_t1
                """
            ),
        ),
        (
            "multiple_files_per_tag",
            textwrap.dedent(
                """\
                key,T1,T2
                k1,k1_t1,"k1_t2, k1_t2_copy"
                k2,k2_t1,"k2_t2, k2_t2_copy"
                k3,k3_t1,"k3_t2, k3_t2_copy"
                """
            ),
        ),
        (
            "multiple_files_per_tag_without_keys",
            textwrap.dedent(
                """\
                T1,T2
                k1_t1,"k1_t2, k1_t2_copy"
                k2_t1,"k2_t2, k2_t2_copy"
                k3_t1,"k3_t2, k3_t2_copy"
                """
            ),
        ),
    ],
)
def test_write_groups_with_csv(group, expected_result, request):
    stream = io.StringIO()
    groups, tags = request.getfixturevalue(group)
    write_groups(
        groups=groups,
        stream=stream,
        tag_names=tags,
        output_format="csv",
    )
    result = stream.getvalue()
    assert result == expected_result
