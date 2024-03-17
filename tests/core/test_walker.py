import pytest

from grob.core.walker import walk


@pytest.fixture
def populated_directory(tmp_path):
    for file in [
        "a/b/c/e.txt",
        "a/b/c/f.txt",
        "a/b/e.txt",
        "a.txt",
        "a/b.txt",
        "a/b/c.txt",
    ]:
        path = tmp_path / file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
    yield tmp_path


def test_walk(populated_directory):
    files = list(walk(populated_directory))
    assert all(file.is_absolute() for file in files)
    assert sorted(files) == sorted(
        [
            populated_directory / "a/b/c/e.txt",
            populated_directory / "a/b/c/f.txt",
            populated_directory / "a/b/e.txt",
            populated_directory / "a.txt",
            populated_directory / "a/b.txt",
            populated_directory / "a/b/c.txt",
        ]
    )
