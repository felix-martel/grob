# `one_tag_different_dirs`

In this example, we're only interested into a single type of files (images), but they are scattered into multiple subdirectories.

File layout:

```
~ tree "examples/one_tag_different_dirs/root"
examples/one_tag_different_dirs/root
├── a
│   ├── b
│   │   ├── c
│   │   │   └── img_004.png
│   │   ├── image_002.gif
│   │   └── img_003.png
│   └── img_001.png
├── d
│   ├── e
│   │   └── picture_resized_008.jpg
│   ├── img_005.jpg
│   ├── img_006.jpg
│   └── img_007.jpg
└── f
    ├── img_009.small.png
    └── img_010.png

6 directories, 10 files
```

Command:

```
grob "*" examples/one_tag_different_dirs/root --relative
```

Result:

```json
[
  "a/b/c/img_004.png",
  "a/b/image_002.gif",
  "a/b/img_003.png",
  "a/img_001.png",
  "d/e/picture_resized_008.jpg",
  "d/img_005.jpg",
  "d/img_006.jpg",
  "d/img_007.jpg",
  "f/img_009.small.png",
  "f/img_010.png"
]
```
