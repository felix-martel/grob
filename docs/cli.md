# CLI Reference

```shell
usage: grob [--multiple [TAG [TAG ...]]] [--optional [TAG [TAG ...]]]
            [--remove-on-missing [TAG [TAG ...]]]
            [--fail-on-missing [TAG [TAG ...]]] [--key PATTERN]
            [--output OUTPUT]
            [--output-format {json,jsonl,human,csv,tsv} | --json | --jsonl | --human | --csv | --tsv]
            [--no-squeeze] [--no-list] [--relative | --absolute]
            [--with-keys | --without-keys] [--help]
            PATTERN [ROOT_DIR]
```

Group different files together by extracting keys from their names and
matching those keys together. The simplest `PATTERN` is `*`, which will match
all files in `ROOT_DIR`. In that case, each "group" of files will comprise a
single file. A more useful `PATTERN` is `a=A/{name}.*,b=B/{name}.*`, which will
match files from different directories A and B based on their stems. The
output could look like this:

```shell
{
    "file_1": {"a": "A/file_1.txt", "b": "B/file_1.log"},
    "file_2": {"a": "A/file_2.txt", "b": "B/file_2.log"},
    ...
}
```

Here, `file_1` and `file_2` are the _keys_, while `a` and `b` are the _tags_.
More generally, `PATTERN` is a comma-separated list of `<tag>=<pattern>` pairs,
where `<tag>` is the name of the tag (e.g. `a` or `b`) and `<pattern>` describes
where to find the files and how to extract a key from their paths.

```shell
positional arguments:
  PATTERN               Pattern describing which tags are present and how to
                        extract their keys.
  ROOT_DIR              Root directory where files are located.

optional arguments:
  --multiple [TAG [TAG ...]]
                        List of tags that accept multiple files. By default,
                        tags expect a single matching file for any given key.
                        When `--multiple` is passed, the tag will contain a
                        list of paths, instead of a single path.
  --optional [TAG [TAG ...]]
                        List of optional tags. If a group doesn't have one of
                        these tags, the tag will be present with null value.
                        By default, all tags are mandatory.
  --remove-on-missing [TAG [TAG ...]]
                        List of strictly mandatory tags. If a group doesn't
                        have one of these tags, it will be removed from the
                        output.
  --fail-on-missing [TAG [TAG ...]]
                        List of mandatory tags. If a group doesn't have one of
                        these tags, grob will fail with exit code 1. This is
                        the default for all tags.
  --key PATTERN         Provide a custom pattern to build the group keys. It
                        can (and should) use any of the placeholders contained
                        in PATTERN: for example, if PATTERN is
                        '**/{parent}/{name}.{ext}', --key could be
                        '{parent}-{name}-{ext}'.
  --output OUTPUT, -o OUTPUT
                        Where to write the output. Default to stdout.
  --help                Show this help message and exit

Output format:
  Controls how the output is formatted.

  --output-format {json,jsonl,human,csv,tsv}, -f {json,jsonl,human,csv,tsv}
                        Specify the output format. Default to 'json'.
  --json, -j            Output a JSON string.
  --jsonl, -l           Output a JSON Line string, i.e. each line is a valid
                        JSON record.
  --human, -h           Output a human readable table.
  --csv                 Output a CSV file, with one group per line and one tag
                        per column. This format isn't recommended when using
                        --multiple.
  --tsv                 Output a TSV file, with one group per line and one tag
                        per column. This format isn't recommended when using
                        --multiple.
  --no-squeeze          Never squeeze file groups, even if no named tag were
                        provided. By default, when all groups only contain one
                        file and no named tag were provided, the output is
                        squeezed into a list of paths.
  --no-list             Always return a dictionary, even if no key was
                        provided. By default, if no named placeholder is used,
                        assume the user isn't interested in the key, but only
                        in the group themselves.
  --relative            Output paths relative to ROOT_DIR.
  --absolute            Output absolute paths.
  --with-keys, -k       Return group keys alongside the group themselves. This
                        is the default.
  --without-keys, -K    Return only the file groups, not their keys.
```
