import io
import json
import textwrap

import pytest

from grob.core.output_formatters import format_groups
from grob.types import GroupKey, TagName

T1 = TagName("T1")
T2 = TagName("T2")
T3 = TagName("T3")


@pytest.fixture
def groups(tmp_path):
    g = {
        GroupKey("k1"): {T1: tmp_path / "k1_t1", T2: tmp_path / "k1_t2"},
        GroupKey("k2"): {T1: tmp_path / "k2_t1", T2: tmp_path / "k2_t2"},
        GroupKey("k3"): {T1: tmp_path / "k3_t1", T2: tmp_path / "k3_t2"},
    }
    yield g


@pytest.fixture
def groups_with_single_tag(tmp_path):
    g = {
        GroupKey("k1"): {T1: tmp_path / "k1_t1"},
        GroupKey("k2"): {T1: tmp_path / "k2_t1"},
        GroupKey("k3"): {T1: tmp_path / "k3_t1"},
    }
    yield g


@pytest.fixture
def groups_with_multiple_files(tmp_path):
    g = {
        GroupKey("k1"): {T1: tmp_path / "k1_t1", T2: [tmp_path / "k1_t2", tmp_path / "k1_t2_copy"]},
        GroupKey("k2"): {T1: tmp_path / "k2_t1", T2: [tmp_path / "k2_t2", tmp_path / "k2_t2_copy"]},
        GroupKey("k3"): {T1: tmp_path / "k3_t1", T2: [tmp_path / "k3_t2", tmp_path / "k3_t2_copy"]},
    }
    yield g


def test_format_groups_with_json(groups, tmp_path):
    stream = io.StringIO()
    format_groups(
        groups=groups,
        stream=stream,
        tag_names=[T1, T2],
    )
    absolute_path = tmp_path.as_posix()
    raw_result = stream.getvalue()
    assert json.loads(raw_result) == {
        "k1": {"T1": f"{absolute_path}/k1_t1", "T2": f"{absolute_path}/k1_t2"},
        "k2": {"T1": f"{absolute_path}/k2_t1", "T2": f"{absolute_path}/k2_t2"},
        "k3": {"T1": f"{absolute_path}/k3_t1", "T2": f"{absolute_path}/k3_t2"},
    }


def test_format_groups_with_json_and_paths_relative_to_root(groups, tmp_path):
    stream = io.StringIO()
    format_groups(groups=groups, stream=stream, tag_names=[T1, T2], relative_to=tmp_path)
    raw_result = stream.getvalue()
    assert json.loads(raw_result) == {
        "k1": {"T1": "k1_t1", "T2": "k1_t2"},
        "k2": {"T1": "k2_t1", "T2": "k2_t2"},
        "k3": {"T1": "k3_t1", "T2": "k3_t2"},
    }


def test_format_groups_with_single_tag_and_squeeze(groups_with_single_tag, tmp_path):
    stream = io.StringIO()
    format_groups(
        groups=groups_with_single_tag,
        stream=stream,
        tag_names=[T1],
    )
    absolute_path = tmp_path.as_posix()
    raw_result = stream.getvalue()
    assert json.loads(raw_result) == {
        "k1": f"{absolute_path}/k1_t1",
        "k2": f"{absolute_path}/k2_t1",
        "k3": f"{absolute_path}/k3_t1",
    }


def test_format_groups_with_single_tag_and_no_squeeze(groups_with_single_tag, tmp_path):
    stream = io.StringIO()
    format_groups(
        groups=groups_with_single_tag,
        stream=stream,
        tag_names=[T1],
        squeeze=False,
    )
    absolute_path = tmp_path.as_posix()
    raw_result = stream.getvalue()
    assert json.loads(raw_result) == {
        "k1": {"T1": f"{absolute_path}/k1_t1"},
        "k2": {"T1": f"{absolute_path}/k2_t1"},
        "k3": {"T1": f"{absolute_path}/k3_t1"},
    }


def test_format_groups_with_single_tag_and_squeeze_and_no_keys(groups_with_single_tag, tmp_path):
    stream = io.StringIO()
    format_groups(
        groups=groups_with_single_tag,
        stream=stream,
        tag_names=[T1],
        with_keys=False,
    )
    absolute_path = tmp_path.as_posix()
    raw_result = stream.getvalue()
    assert json.loads(raw_result) == [
        f"{absolute_path}/k1_t1",
        f"{absolute_path}/k2_t1",
        f"{absolute_path}/k3_t1",
    ]


def test_format_groups_with_multiple_files_per_tag(groups_with_multiple_files, tmp_path):
    stream = io.StringIO()
    format_groups(
        groups=groups_with_multiple_files,
        stream=stream,
        tag_names=[T1, T2],
    )
    absolute_path = tmp_path.as_posix()
    raw_result = stream.getvalue()
    assert json.loads(raw_result) == {
        "k1": {"T1": f"{absolute_path}/k1_t1", "T2": [f"{absolute_path}/k1_t2", f"{absolute_path}/k1_t2_copy"]},
        "k2": {"T1": f"{absolute_path}/k2_t1", "T2": [f"{absolute_path}/k2_t2", f"{absolute_path}/k2_t2_copy"]},
        "k3": {"T1": f"{absolute_path}/k3_t1", "T2": [f"{absolute_path}/k3_t2", f"{absolute_path}/k3_t2_copy"]},
    }


def test_format_groups_with_jsonl(groups, tmp_path):
    stream = io.StringIO()
    format_groups(
        groups=groups,
        stream=stream,
        tag_names=[T1, T2],
        output_format="jsonl",
    )
    absolute_path = tmp_path.as_posix()
    raw_result = stream.getvalue()
    results = list(map(json.loads, raw_result.splitlines()))
    assert results == [
        {"key": "k1", "files": {"T1": f"{absolute_path}/k1_t1", "T2": f"{absolute_path}/k1_t2"}},
        {"key": "k2", "files": {"T1": f"{absolute_path}/k2_t1", "T2": f"{absolute_path}/k2_t2"}},
        {"key": "k3", "files": {"T1": f"{absolute_path}/k3_t1", "T2": f"{absolute_path}/k3_t2"}},
    ]


def test_format_groups_with_jsonl_and_no_keys(groups, tmp_path):
    stream = io.StringIO()
    format_groups(
        groups=groups,
        stream=stream,
        tag_names=[T1, T2],
        output_format="jsonl",
        with_keys=False,
    )
    absolute_path = tmp_path.as_posix()
    raw_result = stream.getvalue()
    results = list(map(json.loads, raw_result.splitlines()))
    assert results == [
        {"T1": f"{absolute_path}/k1_t1", "T2": f"{absolute_path}/k1_t2"},
        {"T1": f"{absolute_path}/k2_t1", "T2": f"{absolute_path}/k2_t2"},
        {"T1": f"{absolute_path}/k3_t1", "T2": f"{absolute_path}/k3_t2"},
    ]


def test_format_groups_with_jsonl_and_squeeze(groups_with_single_tag, tmp_path):
    stream = io.StringIO()
    format_groups(
        groups=groups_with_single_tag,
        stream=stream,
        tag_names=[T1],
        output_format="jsonl",
    )
    absolute_path = tmp_path.as_posix()
    raw_result = stream.getvalue()
    results = list(map(json.loads, raw_result.splitlines()))
    assert results == [
        {"key": "k1", "file": f"{absolute_path}/k1_t1"},
        {"key": "k2", "file": f"{absolute_path}/k2_t1"},
        {"key": "k3", "file": f"{absolute_path}/k3_t1"},
    ]


def test_format_groups_with_csv(groups, tmp_path):
    stream = io.StringIO()
    format_groups(
        groups=groups,
        stream=stream,
        tag_names=[T1, T2],
        output_format="csv",
    )
    absolute_path = tmp_path.as_posix()
    raw_result = stream.getvalue()
    assert raw_result == textwrap.dedent(
        f"""\
        key,T1,T2
        k1,{absolute_path}/k1_t1,{absolute_path}/k1_t2
        k2,{absolute_path}/k2_t1,{absolute_path}/k2_t2
        k3,{absolute_path}/k3_t1,{absolute_path}/k3_t2
        """
    )
