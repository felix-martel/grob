import shutil
from functools import partial

import pytest

from grob.core.errors import AmbiguousTagError

from .conftest import get_example_dir, run_example

run = partial(run_example, example_name="one_input_per_dir")


def test_with_wildcard_extension():
    result = run("image=group_{name}/*.png,labels=group_{name}/*.json")
    assert result == {
        "a": {"image": "group_a/image.png", "labels": "group_a/labels.json"},
        "b": {"image": "group_b/image.png", "labels": "group_b/labels.json"},
        "c": {"image": "group_c/image.png", "labels": "group_c/labels.json"},
        "d": {"image": "group_d/image.png", "labels": "group_d/labels.json"},
    }


@pytest.fixture
def cloned_example_dir(tmp_path):
    cloned_dir = tmp_path / "root"
    shutil.copytree(get_example_dir("one_input_per_dir"), cloned_dir)
    return cloned_dir


def test_with_ambiguous_pattern(cloned_example_dir):
    (cloned_example_dir / "group_a" / "metadata.json").touch()

    with pytest.raises(AmbiguousTagError):
        run("image=group_{name}/*.png,labels=group_{name}/*.json", example_dir=cloned_example_dir)


def test_with_ambiguous_pattern_and_multiple_files_allowed(cloned_example_dir):
    (cloned_example_dir / "group_a" / "metadata.json").touch()

    run(
        "image=group_{name}/*.png,labels=group_{name}/*.json",
        options=["--multiple", "labels"],
        example_dir=cloned_example_dir,
    )


def test_with_narrower_pattern(cloned_example_dir):
    (cloned_example_dir / "group_a" / "metadata.json").touch()
    results = run("image=group_{name}/*.png,labels=group_{name}/labels.json", example_dir=cloned_example_dir)
    assert results["a"]["labels"] == "group_a/labels.json"
