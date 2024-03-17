import copy
from functools import partial
from pathlib import Path

import pytest

from grob.core.errors import MissingTagError
from grob.core.group_validation import filter_and_validate_groups
from grob.core.tags import Tag
from grob.types import OnMissing

# Reduce boilerplate, we're not interested in paths and parsers here
p = Path()
T = partial(Tag, parser=str)


def test_filter_and_validate_groups_no_missing_tag():
    raw_groups = {
        "k1": {"t1": p, "t2": p, "t3": p},
        "k2": {"t1": p, "t2": p, "t3": p},
        "k3": {"t1": p, "t2": p, "t3": p},
        "k4": {"t1": p, "t2": p, "t3": p},
    }
    groups = filter_and_validate_groups(copy.deepcopy(raw_groups), [T(name="t1"), T(name="t2"), T(name="t3")])
    assert groups == raw_groups


def test_filter_and_validate_groups_with_missing_optional_tags():
    groups = filter_and_validate_groups(
        {
            "k1": {"t1": p, "t2": p, "t3": p},
            "k2": {"t1": p, "t3": p},
            "k3": {"t1": p, "t2": p},
            "k4": {"t1": p},
        },
        [T(name="t1"), T(name="t2", on_missing=OnMissing.ignore), T(name="t3", on_missing=OnMissing.ignore)],
    )
    assert groups == {
        "k1": {"t1": p, "t2": p, "t3": p},
        "k2": {"t1": p, "t2": None, "t3": p},
        "k3": {"t1": p, "t2": p, "t3": None},
        "k4": {"t1": p, "t2": None, "t3": None},
    }


def test_filter_and_validate_groups_with_missing_mandatory_tags():
    groups = filter_and_validate_groups(
        {
            "k1": {"t1": p, "t2": p, "t3": p},
            "k2": {"t1": p, "t3": p},
            "k3": {"t1": p, "t2": p},
            "k4": {"t1": p},
        },
        [T(name="t1"), T(name="t2", on_missing=OnMissing.ignore), T(name="t3", on_missing=OnMissing.skip)],
    )
    assert groups == {
        "k1": {"t1": p, "t2": p, "t3": p},
        "k2": {"t1": p, "t2": None, "t3": p},
    }


def test_filter_and_validate_groups_with_missing_strictly_mandatory_tags():
    with pytest.raises(MissingTagError):
        filter_and_validate_groups(
            {
                "k1": {"t1": p, "t2": p, "t3": p},
                "k2": {"t1": p, "t3": p},
                "k3": {"t1": p, "t2": p},
                "k4": {"t1": p},
            },
            [T(name="t1"), T(name="t2", on_missing=OnMissing.skip), T(name="t3", on_missing=OnMissing.fail)],
        )
