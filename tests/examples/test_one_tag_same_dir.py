from functools import partial

from .conftest import run_example

run = partial(run_example, example_name="one_tag_same_dir")

FILE_1 = "image_001.png"
FILE_2 = "image_002.jpg"
FILE_3 = "image_003.gif"


def test_wildcard():
    result = run("*")
    assert result == [FILE_1, FILE_2, FILE_3]


def test_double_wildcard():
    result = run("**/*")
    assert result == [FILE_1, FILE_2, FILE_3]


def test_with_name_as_key():
    result = run("{name}")
    assert result == {"image_001.png": FILE_1, "image_002.jpg": FILE_2, "image_003.gif": FILE_3}


def test_with_stem_as_key():
    result = run("{name}.*")
    assert result == {"image_001": FILE_1, "image_002": FILE_2, "image_003": FILE_3}


def test_with_specific_extensions():
    result = run("{name}.(png|gif)")
    assert result == {"image_001": FILE_1, "image_003": FILE_3}


def test_with_single_extension():
    result = run("{name}.png")
    assert result == {"image_001": FILE_1}


def test_with_hardcoded_prefix():
    result = run("image_{id}.(png|jpg)")
    assert result == {"001": FILE_1, "002": FILE_2}


def test_with_hardcoded_prefix_and_wildcard():
    result = run("image_*.(png|jpg)")
    assert result == [FILE_1, FILE_2]
