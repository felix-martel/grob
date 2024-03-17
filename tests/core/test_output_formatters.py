from pathlib import Path

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


def test_format_groups(groups, tmp_path):
    groups = format_groups(groups=groups, tag_names=[T1, T2])
    assert groups == {
        "k1": {"T1": (tmp_path / "k1_t1").absolute(), "T2": (tmp_path / "k1_t2").absolute()},
        "k2": {"T1": (tmp_path / "k2_t1").absolute(), "T2": (tmp_path / "k2_t2").absolute()},
        "k3": {"T1": (tmp_path / "k3_t1").absolute(), "T2": (tmp_path / "k3_t2").absolute()},
    }


def test_format_groups_with_relative_paths(groups, tmp_path):
    groups = format_groups(groups=groups, tag_names=[T1, T2], relative_to=tmp_path)
    assert groups == {
        "k1": {"T1": Path("k1_t1"), "T2": Path("k1_t2")},
        "k2": {"T1": Path("k2_t1"), "T2": Path("k2_t2")},
        "k3": {"T1": Path("k3_t1"), "T2": Path("k3_t2")},
    }


def test_format_groups_with_single_tag_and_squeeze(groups_with_single_tag, tmp_path):
    groups = format_groups(groups=groups_with_single_tag, tag_names=[T1])
    assert groups == {
        "k1": (tmp_path / "k1_t1").absolute(),
        "k2": (tmp_path / "k2_t1").absolute(),
        "k3": (tmp_path / "k3_t1").absolute(),
    }


def test_format_groups_with_single_tag_and_no_squeeze(groups_with_single_tag, tmp_path):
    groups = format_groups(groups=groups_with_single_tag, tag_names=[T1], squeeze=False)
    assert groups == {
        "k1": {"T1": (tmp_path / "k1_t1").absolute()},
        "k2": {"T1": (tmp_path / "k2_t1").absolute()},
        "k3": {"T1": (tmp_path / "k3_t1").absolute()},
    }


def test_format_groups_with_single_tag_and_squeeze_and_no_keys(groups_with_single_tag, tmp_path):
    groups = format_groups(groups=groups_with_single_tag, tag_names=[T1], with_keys=False)
    assert groups == [
        (tmp_path / "k1_t1").absolute(),
        (tmp_path / "k2_t1").absolute(),
        (tmp_path / "k3_t1").absolute(),
    ]


def test_format_groups_with_multiple_files_per_tag(groups_with_multiple_files, tmp_path):
    groups = format_groups(
        groups=groups_with_multiple_files,
        tag_names=[T1, T2],
    )
    assert groups == {
        "k1": {
            "T1": (tmp_path / "k1_t1").absolute(),
            "T2": [(tmp_path / "k1_t2").absolute(), (tmp_path / "k1_t2_copy").absolute()],
        },
        "k2": {
            "T1": (tmp_path / "k2_t1").absolute(),
            "T2": [(tmp_path / "k2_t2").absolute(), (tmp_path / "k2_t2_copy").absolute()],
        },
        "k3": {
            "T1": (tmp_path / "k3_t1").absolute(),
            "T2": [(tmp_path / "k3_t2").absolute(), (tmp_path / "k3_t2_copy").absolute()],
        },
    }
