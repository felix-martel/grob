from functools import partial

from .conftest import run_example

run = partial(run_example, example_name="two_tags_same_dir")


def test_example():
    result = run("image=image_{id}.png,labels=labels_{id}.json")
    assert result == {
        "1": {"image": "image_1.png", "labels": "labels_1.json"},
        "2": {"image": "image_2.png", "labels": "labels_2.json"},
        "3": {"image": "image_3.png", "labels": "labels_3.json"},
    }
