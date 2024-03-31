# `one_input_per_dir`

In this example, each group of inputs is placed into its own subdirectory.

File layout:

```
~ tree "examples/one_input_per_dir/root"
examples/one_input_per_dir/root
├── group_a
│   ├── image.png
│   └── labels.json
├── group_b
│   ├── image.png
│   └── labels.json
├── group_c
│   ├── image.png
│   └── labels.json
└── group_d
    ├── image.png
    └── labels.json

4 directories, 8 files
```

Command:

```
grob "image=group_{name}/image.png,labels=group_{name}/labels.json" examples/one_input_per_dir/root
```

Result:

```json
{
  "a": {
    "image": "group_a/image.png",
    "labels": "group_a/labels.json"
  },
  "b": {
    "image": "group_b/image.png",
    "labels": "group_b/labels.json"
  },
  "c": {
    "image": "group_c/image.png",
    "labels": "group_c/labels.json"
  },
  "d": {
    "image": "group_d/image.png",
    "labels": "group_d/labels.json"
  }
}
```
