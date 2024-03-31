# `one_input_per_multi_dirs`

File layout:

```
~ tree "examples/one_input_per_multi_dirs/root"
examples/one_input_per_multi_dirs/root
├── fifi
│   ├── 2021
│   │   ├── image.png
│   │   └── labels.json
│   ├── 2022
│   │   ├── image.png
│   │   └── labels.json
│   └── 2023
│       ├── image.png
│       └── labels.json
├── loulou
│   ├── 2021
│   │   ├── image.png
│   │   └── labels.json
│   ├── 2022
│   │   ├── image.png
│   │   └── labels.json
│   └── 2023
│       ├── image.png
│       └── labels.json
└── riri
    ├── 2021
    │   ├── image.png
    │   └── labels.json
    ├── 2022
    │   ├── image.png
    │   └── labels.json
    └── 2023
        ├── image.png
        └── labels.json

12 directories, 18 files
```

Command:

```
grob "image={name}/{year}/*.png,labels={name}/{year}/labels.json" examples/one_input_per_multi_dirs/root
```

Result:

```json
{
  "fifi_2021": {
    "image": "fifi/2021/image.png",
    "labels": "fifi/2021/labels.json"
  },
  "fifi_2022": {
    "image": "fifi/2022/image.png",
    "labels": "fifi/2022/labels.json"
  },
  "fifi_2023": {
    "image": "fifi/2023/image.png",
    "labels": "fifi/2023/labels.json"
  },
  "loulou_2021": {
    "image": "loulou/2021/image.png",
    "labels": "loulou/2021/labels.json"
  },
  "loulou_2022": {
    "image": "loulou/2022/image.png",
    "labels": "loulou/2022/labels.json"
  },
  "loulou_2023": {
    "image": "loulou/2023/image.png",
    "labels": "loulou/2023/labels.json"
  },
  "riri_2021": {
    "image": "riri/2021/image.png",
    "labels": "riri/2021/labels.json"
  },
  "riri_2022": {
    "image": "riri/2022/image.png",
    "labels": "riri/2022/labels.json"
  },
  "riri_2023": {
    "image": "riri/2023/image.png",
    "labels": "riri/2023/labels.json"
  }
}
```
