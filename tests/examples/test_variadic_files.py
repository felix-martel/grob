from functools import partial

from .conftest import run_example

run = partial(run_example, example_name="variadic_files")


def test_example():
    result = run("image={group}/*.(png|jpg),labels={group}/labels.csv", options=["--multiple", "image"])
    assert result == {
        "bellatores": {
            "image": [
                "bellatores/2024-01.png",
                "bellatores/2024-02.png",
                "bellatores/2024-03.png",
                "bellatores/2024-04.png",
                "bellatores/2024-05.png",
            ],
            "labels": "bellatores/labels.csv",
        },
        "laboratores": {
            "image": [
                "laboratores/2023-09.jpg",
                "laboratores/2023-10.jpg",
                "laboratores/2023-11.jpg",
                "laboratores/2023-12.jpg",
            ],
            "labels": "laboratores/labels.csv",
        },
        "oratores": {
            "image": [
                "oratores/2024-01.png",
                "oratores/2024-02.png",
                "oratores/2024-03.jpg",
                "oratores/2024-04.png",
                "oratores/2024-05.png",
            ],
            "labels": "oratores/labels.csv",
        },
    }
