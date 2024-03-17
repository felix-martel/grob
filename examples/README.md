# Examples

- [`one_tag_different_dirs`](./one_tag_different_dirs/README.md): all files have the same tag, but they are located in different sub-directories
- [`one_tag_same_dir`](./one_tag_same_dir/README.md): all files have the same tag (_type_) and are located in the same directory
- [`two_tags_same_dir`](./two_tags_same_dir/README.md): two different types of files `image` and `label` (two _tags_), located in the same directory and matched by a fragment of their filenames
- [`inputs_across_dirs`](./inputs_across_dirs/README.md): once again, there are two file tags. Each is located in its own directory, and files are matched by their filename
- [`one_input_per_dir`](./one_input_per_dir/README.md): files that must be grouped together are located in the same subdirectory
- [`one_input_per_multi_dirs`](./one_input_per_multi_dirs/README.md): same as before, but subdirectories are no longer in the root directory
- [`different_nesting_levels`](./different_nesting_levels/README.md):
- [`different_variadicities`](./different_variadicities/README.md): the same label file is re-used in different input groups
- [`different_variadicities_multiple_levels`](./different_variadicities_multiple_levels/README.md): same as previous, with a more complex layout
- [`multiple_over_multiple_tags`](./multiple_over_multiple_tags/README.md): all tags are multiple (i.e. for a given key, each tag is a list of file rather than a single file)
- [`optional_tags`](./optional_tags/README.md): all tags are optional (i.e. an input group can have some of its tags to None)
- [`variadic_files`](./variadic_files/README.md): a single label file and multiple image files for a given key
