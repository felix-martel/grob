from functools import partial

import pytest

from grob.core.errors import MissingTagError

from .conftest import run_example

run = partial(run_example, example_name="inputs_across_dirs")


def test_with_wildcard_extension():
    result = run("image=images/{name}.*,labels={name}.json")
    assert result == {
        "riri": {"image": "images/riri.jpg", "labels": "labels/riri.json"},
        "fifi": {"image": "images/fifi.gif", "labels": "labels/fifi.json"},
        "loulou": {"image": "images/loulou.png", "labels": "labels/loulou.json"},
    }


def test_with_ignore_incomplete():
    result = run("image=images/{name}.(gif|jpg),labels={name}.json", options=["--remove-on-missing"])
    assert result == {
        "riri": {"image": "images/riri.jpg", "labels": "labels/riri.json"},
        "fifi": {"image": "images/fifi.gif", "labels": "labels/fifi.json"},
    }


def test_with_fail_on_incomplete():
    with pytest.raises(MissingTagError):
        run("image=images/{name}.(gif|jpg),labels={name}.json", options=["--fail-on-missing"])


def test_fail_on_incomplete_by_default():
    with pytest.raises(MissingTagError):
        run("image=images/{name}.(gif|jpg),labels={name}.json")


def test_with_specific_extensions():
    result = run("image=images/{name}.(gif|jpg),labels={name}.json", options=["--optional", "image"])
    assert result == {
        "riri": {"image": "images/riri.jpg", "labels": "labels/riri.json"},
        "fifi": {"image": "images/fifi.gif", "labels": "labels/fifi.json"},
        "loulou": {"image": None, "labels": "labels/loulou.json"},
    }
