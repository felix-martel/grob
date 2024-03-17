from functools import partial

from .conftest import run_example

run = partial(run_example, example_name="different_variadicities_multiple_levels")


def test_example():
    result = run("toss={outcome}/toss-{run}.txt,labels={outcome}/labels.txt")
    assert result == {
        "heads_1": {"toss": "heads/toss-1.txt", "labels": "heads/labels.txt"},
        "heads_2": {"toss": "heads/toss-2.txt", "labels": "heads/labels.txt"},
        "heads_3": {"toss": "heads/toss-3.txt", "labels": "heads/labels.txt"},
        "heads_4": {"toss": "heads/toss-4.txt", "labels": "heads/labels.txt"},
        "tails_2": {"toss": "tails/toss-2.txt", "labels": "tails/labels.txt"},
        "tails_3": {"toss": "tails/toss-3.txt", "labels": "tails/labels.txt"},
        "tails_4": {"toss": "tails/toss-4.txt", "labels": "tails/labels.txt"},
        "tails_5": {"toss": "tails/toss-5.txt", "labels": "tails/labels.txt"},
    }


def test_with_multiple_files():
    result = run("toss={outcome}/toss-*.txt, labels={outcome}/labels.txt", options=["--multiple", "toss"])
    assert result == {
        "heads": {
            "toss": ["heads/toss-1.txt", "heads/toss-2.txt", "heads/toss-3.txt", "heads/toss-4.txt"],
            "labels": "heads/labels.txt",
        },
        "tails": {
            "toss": ["tails/toss-2.txt", "tails/toss-3.txt", "tails/toss-4.txt", "tails/toss-5.txt"],
            "labels": "tails/labels.txt",
        },
    }
