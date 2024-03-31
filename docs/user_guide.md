# User Guide

`grob` creates groups of files that belong together. Each group has a unique _key_ ; within a group, files can be organized into _tags_.

Let's take for example the [Rider Safety & Compliance](https://www.kaggle.com/datasets/aneesarom/rider-with-helmet-without-helmet-number-plate) dataset on Kaggle: for a given subset, it contains pairs of images and labels:

```
├── images
│   ├── new1.jpg
│   ├── new2.jpg
│   └── ...
└── labels
    ├── new1.txt
    ├── new2.txt
    └── ...
```

To use it, we need to join images with their corresponding label files:

```json
{
  "1": {"image":  "images/new1.jpg", "labels":  "labels/new1.jpg"},
  "2": {"image":  "images/new2.jpg", "labels":  "labels/new2.jpg"},
  ...
}
```

Each group has a unique _key_: `1`, `2` and so on. Within a group, files are organized into _tags_: `image` and `labels` in the above example.

## Basics

Let's start by getting the image files:

```shell
~ grob "images/new*.jpg" train
[
  "images/new1.jpg",
  "images/new2.jpg",
   ...
]
```

We specified a glob pattern `images/*.jpg`, and `grob` returned all matching files. Now we can specify which part of the path we want to use as key, by declaring a _placeholder_ with braces:

```shell
~ grob "images/new{id}.jpg" train
{
  "1": "images/new1.jpg",
  "2": "images/new2.jpg",
  ...
}
```

`images/new{id}.jpg` will match the same files as `images/new*.jpg`, but it will tell `grob` to extract the matched value and use it as the `id` part of the key. We can now declare how to find the labels:

```shell
~ grob "image=images/new{id}.jpg, labels=labels/new{id}.txt" train
{
  "1": {
    "image": "images/new1.jpg",
    "labels": "labels/new1.txt"
  },
  "2": {
    "image": "images/new2.jpg",
    "labels": "labels/new2.txt"
  },
  ...
}
```

For each tag `image` and `labels`, `grob` will find the files matching the pattern, extract any named placeholder and join them into a single key.
It will then match together files that have the same key.

## Working with incomplete groups

In practice, the command above would fail if one of the groups is missing any of the tags. You can change this behavior by passing:

- `--optional` will make all tags optional. The tag will contain `null` instead of an actual file.
- `--remove-on-missing` will remove all incomplete groups from the final outputs.

These two options accept a list of tags: for example, using `--optional labels --remove-on-missing image` would keep images without labels but remove labels without images.

## More complex keys

You're not limited to a single placeholder per pattern. Our example dataset has two subsets, `train` and `val`. We want to get files from both subset, but we don't want to group an image from the training set with a label from the validation set. We can use:

```shell
~ grob "image={subset}/images/new{id}.jpg, labels={subset}/labels/new{id}.txt" .
{
  "train_1": {
    "image": "train/images/new1.jpg",
    "labels": "train/labels/new1.txt"
  },
  ...
  "val_1": {
    "image": "val/images/new1.jpg",
    "labels": "val/labels/new1.txt"
  }
}
```

Here, placeholders `{subset}` and `{id}` are concatenated to build the final key. A custom formatter can be passed with the `--key` option, using standard Python f-strings:

```shell
~ grob "image={subset}/images/new{id}.jpg, labels={subset}/labels/new{id}.txt" . --key "{subset}-{id:0>3}"
{
  "train-001": {
    "image": "train/images/new1.jpg",
    "labels": "train/labels/new1.txt"
  },
  "train-002": {
    "image": "train/images/new2.jpg",
    "labels": "train/labels/new2.txt"
  },
}
```

If you're not interested in the keys, but only in the files themselves, you can use `--without-keys` or `-K`:

```shell
~ grob "image={subset}/images/new{id}.jpg, labels={subset}/labels/new{id}.txt" . --without-keys
[
  {
    "image": "train/images/new1.jpg",
    "labels": "train/labels/new1.txt"
  },
  ...
]
```

## More complex patterns

Patterns also support:

- `**` for matching zero or more directories
- option groups `(a|b|c)` to match several options. Typically, use `*.(jpg|png|gif)` to match any of these extensions. Option groups cannot contain wildcards or placeholders.
- placeholder flags to restrict what a placeholder can match

For complete control, a regular expression can be passed instead of a glob-like pattern.

### Placeholder flags

As explained above, a placeholder will match the same as `*` (i.e. any character but a slash). We can add _placeholder flags_ to restrict which characters can be matched by a placeholder:

- `d` will only match digits
- `a` will only match alphanumeric characters
- `>3` will match three characters or more
- `<3` will match three characters or fewer
- `3` will match exactly three characters
- `3-9` will match three to nine characters

Placeholder flags must be indicated within the placeholder, after a colon `:`, e.g. `{name:a>3}`. Multiple flags can be combined.

### Regular expressions

For even more control, one can use _regular expressions_ instead of glob-like patterns. Regular expressions must use the [regular Python syntax](https://docs.python.org/3/library/re.html#module-re). Placeholders must be indicated with _named capturing groups_ `(?P<placeholder_name>...)`.
To indicate that a pattern must be intepreted as a regular expression, it must end with a `:r` flag.

For example, this will only match images whose id contains a three:

```shell
~ grob "image=images/new(?P<id>\d*3|3\d*)[.]jpg:r, labels=labels/new{id}.txt:r" . --remove-on-missing
```

## Multiple files per tag

By default, `grob` expects exactly one file per group and per tag, and will fail if multiple files match a given pattern for a group.
This behavior can be turned off with the `--multiple`:

- `--multiple TAG1 TAG2 ...` will make `TAG1` and `TAG2` contain a _list_ of files
- `--multiple` will make all tags contain a list of files

## Distribute file over groups

Sometimes, you'll want the same file to be included in multiple groups. For example, let's say we have tracks and covers from different albums:

```shell
├── Miles Ahead
│   ├── cover.jpg
│   ├── 01 - Springsville.mp3
│   ├── 02 - The Maids of Cadiz.mp3
│   └── ...
└── Kind of Blue
    ├── cover.jpg
    ├── 01 - So What.mp3
    ├── 02 - Freddie Freeloader.mp3
    └── ...
```

Each cover must be associated to all tracks from the album.
Tags can be described as usual:

```shell
~ grob "track={album}/{track:d2}*.mp3, cover={album}/cover.jpg" .
```

`grob` will detect that tag `cover` is missing the `{track}` placeholder, and will automatically distribute covers over the common placeholders, achieving the desired behavior.

??? note "Deep Dive"

    To better understand what's going on in this case, consider the files after the search step and before the join step.

    For tag `track`:

    | `{album}` | `{track}` | File |
    |:--------|:--------|:----------|
    | Miles Ahead | 01 | `Miles Ahead/01 - Springsville.mp3 |
    | Miles Ahead | 02 | `Miles Ahead/01 - Springsville.mp3 |
    | ... | ... | ... |

    For tag `cover`:

    | `{album}` | File |
    |:----------------|:----------|
    | Miles Ahead | `Miles Ahead/cover.jpg` |
    | Kind of Blue | `Kind of Blue/cover.jpg` |

    `grob` will perform **an outer join over the common keys**, in that case `{album}`, thus giving the following result:

    | `{album}` | `{track}` | `track` | `cover` |
    |:--------|:--------|:----------|:-----|
    | Miles Ahead | 01 | `Miles Ahead/01 - Springsville.mp3` | `Miles Ahead/cover.jpg` |
    | Miles Ahead | 02 | `Miles Ahead/01 - Springsville.mp3` | `Miles Ahead/cover.jpg` |
    | ... | ... | ... | ... |

## Output format

`grob` supports the following formats, controlled by the `--output-format, -f` option:

| Format  | Description                                   | Shortcut      |
| :------ | :-------------------------------------------- | :------------ |
| `json`  | JSON mapping from keys to groups              | `--json, -j`  |
| `jsonl` | one JSON record per group                     | `--jsonl, -l` |
| `human` | human readable table (not implemented yet)    | `--human, -h` |
| `csv`   | comma-separated file, with one tag per column | `--csv`       |
| `tsv`   | tab-separated file, same format               | `--tsv`       |

`--output, -o` allows you to choose where to write the output (default to `stdout`).

`--absolute` will return absolute file paths, instead of paths relative to the root directory.
