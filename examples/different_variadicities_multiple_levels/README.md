# `different_variadicities_multiple_levels`

Here, we want to map each `toss-*.txt` file to the corresponding label file: if toss was a `head`, we want to group it
with `heads/labels.txt`, otherwise with `tails/labels.txt`.

This can be achieved with the following command:

File layout:

```
~ tree "examples/different_variadicities_multiple_levels/root"
examples/different_variadicities_multiple_levels/root
├── heads
│   ├── labels.txt
│   ├── toss-1.txt
│   ├── toss-2.txt
│   ├── toss-3.txt
│   └── toss-4.txt
└── tails
    ├── labels.txt
    ├── toss-2.txt
    ├── toss-3.txt
    ├── toss-4.txt
    └── toss-5.txt

2 directories, 10 files
```

Command:

```
grob "toss={outcome}/toss-{index}.txt, labels={outcome}/labels.txt" examples/different_variadicities_multiple_levels/root
```

Result:

```json
{
  "heads_1": {
    "toss": "heads/toss-1.txt",
    "labels": "heads/labels.txt"
  },
  "heads_2": {
    "toss": "heads/toss-2.txt",
    "labels": "heads/labels.txt"
  },
  "heads_3": {
    "toss": "heads/toss-3.txt",
    "labels": "heads/labels.txt"
  },
  "heads_4": {
    "toss": "heads/toss-4.txt",
    "labels": "heads/labels.txt"
  },
  "tails_2": {
    "toss": "tails/toss-2.txt",
    "labels": "tails/labels.txt"
  },
  "tails_3": {
    "toss": "tails/toss-3.txt",
    "labels": "tails/labels.txt"
  },
  "tails_4": {
    "toss": "tails/toss-4.txt",
    "labels": "tails/labels.txt"
  },
  "tails_5": {
    "toss": "tails/toss-5.txt",
    "labels": "tails/labels.txt"
  }
}
```

Notice how we don't specify any custom flag to achieve this grouping.

To understand how it works, consider what happens during the research step, when `grob` looks for files matching the
image pattern `{outcome}/toss-{index}.txt`:

| `outcome` | `index` | path               |
| :-------- | :------ | :----------------- |
| heads     | 1       | `heads/toss-1.txt` |
| heads     | 2       | `heads/toss-2.txt` |
| ...       | ...     | ...                |
| tails     | 2       | `tails/toss-2.txt` |

Similarly, this is what we get for `{outcome}/labels.txt`:

| `outcome` | path               |
| :-------- | :----------------- |
| heads     | `heads/labels.txt` |
| tails     | `tails/labels.txt` |

Next, during the grouping step, `grob` will match image and label files by **performing an outer join on the common key
parts**, i.e. on the `outcome` column in this case. After the join, we'll end up with:

| `outcome` | `index` | tag `image`        | tag `labels`       |
| :-------- | :------ | :----------------- | :----------------- |
| heads     | 1       | `heads/toss-1.txt` | `heads/labels.txt` |
| heads     | 2       | `heads/toss-2.txt` | `heads/labels.txt` |
| ...       | ...     | ...                | ...                |
| tails     | 2       | `tails/toss-2.txt` | `tails/labels.txt` |

There's no way to disable this behavior from the command-line, besides making sure that all the provided patterns use
the same named placeholders.

Alternatively, in the same situation, you could group toss files together by using `--multiple`:

```shell
~ grob "toss={outcome}/toss-*.txt, labels={outcome}/labels.txt" examples/different_variadicities_multiple_levels/root --multiple toss
{
  "heads": {
    "toss": [
      "heads/toss-1.txt",
      "heads/toss-2.txt",
      "heads/toss-3.txt",
      "heads/toss-4.txt"
    ],
    "labels": "heads/labels.txt"
  },
  "tails": {
    "toss": [
      "tails/toss-2.txt",
      "tails/toss-3.txt",
      "tails/toss-4.txt",
      "tails/toss-5.txt"
    ],
    "labels": "tails/labels.txt"
  }
}
```
