# `multiple_over_multiple_tags`

In this case, each group has multiple images (possibly zero), as well as one or mutiple textual descriptions.

Here's how to achieve this:

File layout:

```
~ tree "examples/multiple_over_multiple_tags/root"
examples/multiple_over_multiple_tags/root
├── a_a
│   ├── img_1.png
│   ├── img_3.png
│   ├── img_7.png
│   └── left.txt
├── a_b
│   ├── bottom.txt
│   ├── img_1.png
│   ├── img_2.png
│   ├── img_4.png
│   ├── img_5.png
│   ├── right.txt
│   └── top.txt
└── c_b
    ├── left.txt
    └── right.txt

3 directories, 13 files
```

Command:

```
grob "image={group}/img_*.png,descr={group}/*.txt" examples/multiple_over_multiple_tags/root \
  --relative \
  --multiple all \
  --optional image
```

Result:

```json
{
  "a_a": {
    "image": ["a_a/img_1.png", "a_a/img_3.png", "a_a/img_7.png"],
    "descr": ["a_a/left.txt"]
  },
  "a_b": {
    "image": [
      "a_b/img_1.png",
      "a_b/img_2.png",
      "a_b/img_4.png",
      "a_b/img_5.png"
    ],
    "descr": ["a_b/bottom.txt", "a_b/right.txt", "a_b/top.txt"]
  },
  "c_b": {
    "image": [],
    "descr": ["c_b/left.txt", "c_b/right.txt"]
  }
}
```

`--multiple all` indicates that both tags `image` and `descr` accept multiple files. Without this option, the command
would fail, as the same key would be mapped to different files.

`--optional image` indicate that tag `image` is optional, allowing for group `c_b` to be kept even thoug it does not
have an image. Alternatively, one could use `--remove-on-missing` to remove groups without images from the final output.
Without any flag, the default is `--fail-on-missing all`, meaning that the command will fail if any of the tags is
absent.
