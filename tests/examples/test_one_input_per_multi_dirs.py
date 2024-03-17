from functools import partial

from .conftest import run_example

run = partial(run_example, example_name="one_input_per_multi_dirs")


def test_with_default_key():
    result = run("image={name}/{year}/image.png,labels={name}/{year}/labels.json")
    assert result == {
        "riri_2021": {"image": "riri/2021/image.png", "labels": "riri/2021/labels.json"},
        "riri_2022": {"image": "riri/2022/image.png", "labels": "riri/2022/labels.json"},
        "riri_2023": {"image": "riri/2023/image.png", "labels": "riri/2023/labels.json"},
        "fifi_2021": {"image": "fifi/2021/image.png", "labels": "fifi/2021/labels.json"},
        "fifi_2022": {"image": "fifi/2022/image.png", "labels": "fifi/2022/labels.json"},
        "fifi_2023": {"image": "fifi/2023/image.png", "labels": "fifi/2023/labels.json"},
        "loulou_2021": {"image": "loulou/2021/image.png", "labels": "loulou/2021/labels.json"},
        "loulou_2022": {"image": "loulou/2022/image.png", "labels": "loulou/2022/labels.json"},
        "loulou_2023": {"image": "loulou/2023/image.png", "labels": "loulou/2023/labels.json"},
    }


def test_with_custom_key():
    result = run(
        "image={name}/{year}/image.png,labels={name}/{year}/labels.json", options=["--key", "group {name}/{year}"]
    )
    assert result == {
        "group riri/2021": {"image": "riri/2021/image.png", "labels": "riri/2021/labels.json"},
        "group riri/2022": {"image": "riri/2022/image.png", "labels": "riri/2022/labels.json"},
        "group riri/2023": {"image": "riri/2023/image.png", "labels": "riri/2023/labels.json"},
        "group fifi/2021": {"image": "fifi/2021/image.png", "labels": "fifi/2021/labels.json"},
        "group fifi/2022": {"image": "fifi/2022/image.png", "labels": "fifi/2022/labels.json"},
        "group fifi/2023": {"image": "fifi/2023/image.png", "labels": "fifi/2023/labels.json"},
        "group loulou/2021": {"image": "loulou/2021/image.png", "labels": "loulou/2021/labels.json"},
        "group loulou/2022": {"image": "loulou/2022/image.png", "labels": "loulou/2022/labels.json"},
        "group loulou/2023": {"image": "loulou/2023/image.png", "labels": "loulou/2023/labels.json"},
    }
