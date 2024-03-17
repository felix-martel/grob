from functools import partial

from .conftest import run_example

run = partial(run_example, example_name="optional_tags")


def test_example():
    result = run("image={card}/img.png,meta={card}/*.json,legend={card}/legend.txt", options=["--optional", "all"])
    assert result == {
        "clubs": {"image": "clubs/img.png", "meta": None, "legend": "clubs/legend.txt"},
        "diamonds": {"image": "diamonds/img.png", "meta": "diamonds/metadata.json", "legend": None},
        "hearts": {"image": None, "meta": "hearts/metadata.json", "legend": "hearts/legend.txt"},
        "spades": {"image": "spades/img.png", "meta": None, "legend": "spades/legend.txt"},
    }
