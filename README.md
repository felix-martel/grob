# grob

[![Release](https://img.shields.io/github/v/release/felix-martel/grob)](https://img.shields.io/github/v/release/felix-martel/grob)
[![Build status](https://img.shields.io/github/actions/workflow/status/felix-martel/grob/main.yml?branch=main)](https://github.com/felix-martel/grob/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/felix-martel/grob)](https://img.shields.io/github/commit-activity/m/felix-martel/grob)
[![License](https://img.shields.io/github/license/felix-martel/grob)](https://img.shields.io/github/license/felix-martel/grob)

Group files together in a flexible way using glob-like patterns.

```shell
pip install grob
```

In its simplest form, `grob` simply lists all files in a directory:

```shell
~ grob "*" .
[
  "examples/one_tag_same_dir/root/image_001.png",
  "examples/one_tag_same_dir/root/image_002.jpg",
  "examples/one_tag_same_dir/root/image_003.gif"
]
```

given the following directory content:

```shell
root
├── image_001.png
├── image_002.jpg
└── image_003.gif
```

However, `grob` is mainly useful to group different files together. Let's say you have images and corresponding JSON description for each image:

```shell
root
├── image_1.png
├── image_2.png
├── image_3.png
├── labels_1.json
├── labels_2.json
└── labels_3.json
```

```shell
~ grob "image=image_{id}.png,labels=labels_{id}.json" .
{
    "1": {"image": "image_1.png", "labels": "labels_1.json"},
    "2": {"image": "image_2.png", "labels": "labels_2.json"},
    "3": {"image": "image_3.png", "labels": "labels_3.json"}
}
```

Now imagine each group of inputs is stored in the same subdirectory:

```shell
root
├── group_a
│   ├── image.png
│   └── labels.json
├── group_b
│   ├── image.png
│   └── labels.json
├── group_c
│   ├── image.png
│   └── labels.json
└── group_d
    ├── image.png
    └── labels.json
```

We just need to update our pattern:

```shell
~ grob "image=group_{name}/*.png,labels=group_{name}/*.json" .
{
    "a": {"image": "group_a/image.png", "labels": "group_a/labels.json"},
    "b": {"image": "group_b/image.png", "labels": "group_b/labels.json"},
    "c": {"image": "group_c/image.png", "labels": "group_c/labels.json"},
    "d": {"image": "group_d/image.png", "labels": "group_d/labels.json"}
}
```

What if each type of file lives in its own directory?

```shell
root
├── images
│   ├── fifi.gif
│   ├── loulou.png
│   └── riri.jpg
└── labels
    ├── fifi.json
    ├── loulou.json
    └── riri.json
```

```shell
~ grob "image=images/{name}.*,labels={name}.json" .
{
    "riri": {"image": "images/riri.jpg", "labels": "labels/riri.json"},
    "fifi": {"image": "images/fifi.gif", "labels": "labels/fifi.json"},
    "loulou": {"image": "images/loulou.png", "labels": "labels/loulou.json"}
}
```

See more in the [Examples](./examples/README.md) section, or check `tests/examples/`.

## Contribute

Install the environment and the pre-commit hooks with

```bash
make install
```

Run tests:

```shell
make tests
# Alternatively, you can directly run `pytest`
```

Run code quality tools:

```shell
make check
```

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
