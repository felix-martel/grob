from functools import partial

import pytest

from grob.core.errors import MissingTagError

from .conftest import run_example

run = partial(run_example, example_name="multiple_over_multiple_tags")


def test_example_with_optional():
    result = run("image={group}/img_*.png,descr={group}/*.txt", options=["--multiple", "all", "--optional", "image"])
    assert result == {
        "a_a": {
            "image": ["a_a/img_1.png", "a_a/img_3.png", "a_a/img_7.png"],
            "descr": ["a_a/left.txt"],
        },
        "a_b": {
            "image": ["a_b/img_1.png", "a_b/img_2.png", "a_b/img_4.png", "a_b/img_5.png"],
            "descr": ["a_b/bottom.txt", "a_b/right.txt", "a_b/top.txt"],
        },
        "c_b": {
            "image": [],
            "descr": ["c_b/left.txt", "c_b/right.txt"],
        },
    }


def test_example_without_optional():
    with pytest.raises(MissingTagError):
        run("image={group}/img_*.png,descr={group}/*.txt", options=["--multiple", "all"])
