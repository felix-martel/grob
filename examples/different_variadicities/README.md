# `different_variadicities`

Here, each image is associated with the same file `labels.csv`. We can _distribute_ this file over multiple keys, so
that the file is replicated into multiple groups.

File layout:

```
~ tree "examples/different_variadicities/root"
examples/different_variadicities/root
├── img1.png
├── img2.png
├── img3.png
└── labels.csv

0 directories, 4 files
```

Command:

```
grob "image=img{index}.png,labels=labels.csv" examples/different_variadicities/root
```

Result:

```json
{
  "1": {
    "image": "img1.png",
    "labels": "labels.csv"
  },
  "2": {
    "image": "img2.png",
    "labels": "labels.csv"
  },
  "3": {
    "image": "img3.png",
    "labels": "labels.csv"
  }
}
```

Note that we don't have to specify any custom option to `grob`: when parsing the patterns, `grob` understand that tag
`labels` has no `{index}` part, and will thus match image and label files on all parts except `index`. To better
understand this, head to the [next example](./different_variadicities_multiple_levels/README.md).
