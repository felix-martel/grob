# `one_tag_same_dir`

All files are located in the same directory.

File layout:

```
~ tree "examples/one_tag_same_dir/root"
examples/one_tag_same_dir/root
├── image_001.png
├── image_002.jpg
└── image_003.gif

0 directories, 3 files
```

Command:

```
grob "*" examples/one_tag_same_dir/root --relative
```

Result:

```json
[
  "/home/felix/dev/grob/examples/one_tag_same_dir/root/image_001.png",
  "/home/felix/dev/grob/examples/one_tag_same_dir/root/image_002.jpg",
  "/home/felix/dev/grob/examples/one_tag_same_dir/root/image_003.gif"
]
```

Additional things to note:

- since the pattern doesn't contain any named placehoder such as `{name}`, `grob` assumes the caller isn't interested in
  the _keys_ of each group, and thus returns a list. This could be disabled by passing `--with-keys`.
- since the caller did not provide a tag, `grob` returns directly the path of the files, instead of wrapping them into
  a dictionary. This could be disabled by passing `--no-squeeze`.
