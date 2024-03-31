# `inputs_across_dirs`

In this example, we want to group images and labels together.
Corresponding files have the same stem, but have different extensions and are located in different directories.

File layout:

```
~ tree "examples/inputs_across_dirs/root"
examples/inputs_across_dirs/root
├── images
│   ├── fifi.gif
│   ├── loulou.png
│   └── riri.jpg
└── labels
    ├── fifi.json
    ├── loulou.json
    └── riri.json

2 directories, 6 files
```

Command:

```
grob "images=images/{person}.(gif|png|jpg),labels=labels/{person}.json" examples/inputs_across_dirs/root --relative
```

Result:

```json
{
  "fifi": {
    "images": "images/fifi.gif",
    "labels": "labels/fifi.json"
  },
  "loulou": {
    "images": "images/loulou.png",
    "labels": "labels/loulou.json"
  },
  "riri": {
    "images": "images/riri.jpg",
    "labels": "labels/riri.json"
  }
}
```
