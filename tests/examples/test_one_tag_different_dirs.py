from functools import partial

from .conftest import run_example

run = partial(run_example, example_name="one_tag_different_dirs")

FILES = [
    "a/img_001.png",
    "a/b/image_002.gif",
    "a/b/img_003.png",
    "a/b/c/img_004.png",
    "d/img_005.jpg",
    "d/img_006.jpg",
    "d/img_007.jpg",
    "d/e/picture_resized_008.jpg",
    "f/img_009.small.png",
    "f/img_010.png",
]


def test_wildcard():
    result = run("*")
    assert result == sorted(FILES)


def test_double_wildcard():
    result = run("**/*")
    assert result == sorted(FILES)


def test_with_stem_as_key():
    result = run("*_{name}.*")
    assert result == {
        "001": FILES[0],
        "002": FILES[1],
        "003": FILES[2],
        "004": FILES[3],
        "005": FILES[4],
        "006": FILES[5],
        "007": FILES[6],
        "008": FILES[7],
        "009": FILES[8],
        "010": FILES[9],
    }


def test_with_specific_extensions():
    result = run("{name}.(jpg|gif)")
    assert result == {
        "image_002": FILES[1],
        "img_005": FILES[4],
        "img_006": FILES[5],
        "picture_resized_008": FILES[7],
        "img_007": FILES[6],
    }


def test_with_single_extension():
    result = run("*_{name}.png")
    assert result == {"001": FILES[0], "003": FILES[2], "004": FILES[3], "009.small": FILES[8], "010": FILES[9]}


def test_with_specific_directory():
    result = run("a/**/*_{index}.(png|jpg)")
    assert result == {"001": FILES[0], "003": FILES[2], "004": FILES[3]}


def test_with_specific_directory_and_fixed_nesting_level():
    result = run("a/*/*_{index}.*")
    assert result == {"002": FILES[1], "003": FILES[2]}
