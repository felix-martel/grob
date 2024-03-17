from functools import partial

from .conftest import run_example

run = partial(run_example, example_name="different_variadicities")


def test_example():
    result = run("image=img{index}.png,labels=labels.csv")
    assert result == {
        "1": {"image": "img1.png", "labels": "labels.csv"},
        "2": {"image": "img2.png", "labels": "labels.csv"},
        "3": {"image": "img3.png", "labels": "labels.csv"},
    }
