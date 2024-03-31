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

## Kaggle examples

Here are some examples of applying `grob` to Kaggle datasets.
If you find more compelling examples, don't hesitate to add them here.

[Rider Safety & Compliance](https://www.kaggle.com/datasets/aneesarom/rider-with-helmet-without-helmet-number-plate/data)

```shell
grob "image={subset}/images/new{id:d}.jpg,labels={subset}/images/new{id:d}.txt" . --optional labels --remove-on-missing image
```

```json
{
  "train_1": {
    "image": "train/images/new1.jpg",
    "labels": "train/labels/new1.txt"
  }
}
```

[VehicleDetection-YOLOv8](https://www.kaggle.com/datasets/alkanerturan/vehicledetection)

```shell
grob "image={subset}/images/{name}.jpg, labels={subset}/labels/{name}.txt" .
```

```json
{
  "test_00dea1edf14f09ab_jpg.rf.3f17c8790a68659d03b1939a59ccda80": {
    "image": "test/images/00dea1edf14f09ab_jpg.rf.3f17c8790a68659d03b1939a59ccda80.jpg",
    "labels": "test/labels/00dea1edf14f09ab_jpg.rf.3f17c8790a68659d03b1939a59ccda80.txt"
  }
}
```

[B200 LEGO Detection Dataset](https://www.kaggle.com/datasets/ronanpickell/b100-lego-detection-dataset)

```shell
grob "image={subset}/images/{name:d}.png, labels={subset}/annotations/{name:d}.png" .
```

```json
{
  "0": {
    "image": "images/0.png",
    "labels": "annotations/0.xml"
  }
}
```

[Aero-engine defect](https://www.kaggle.com/datasets/wolfmedal/aero-engine-defect-new)

```shell
grob "image=images/{subset}/images/{name}.jpg, labels=labels/{subset}/{name}.txt" .
# Alternatively, group all the different augmentations of a single image together
grob "image=images/{subset}/images/{id:d}*.jpg, labels=labels/{subset}/{id:d}*.txt" . --multiple --optional
```

[Car Parts - Image Classification](https://www.kaggle.com/datasets/gpiosenka/car-parts-40-classes)

```shell
grob "image={subset}/{part_name}/*.jpg" . --multiple --key "{part_name} - {subset}"
```

[ASL Alphabet](https://www.kaggle.com/datasets/grassknoted/asl-alphabet)

```shell
grob "image=asl_alphabet_train/{part_name}/*.jpg" . --multiple
```

[Fruit Images for Object Detection](https://www.kaggle.com/datasets/mbkinaci/fruit-images-for-object-detection)

```shell
grob "image={subset}/{name}.jpg, labels={subset}/{name}.xml" .
```

[Cat Dataset](https://www.kaggle.com/datasets/crawford/cat-dataset)

```shell
grob "image=*/{name}.jpg, labels=*/{name}.jpg.cat" .
```

[DeepGlobe Road Extraction Dataset](https://www.kaggle.com/datasets/balraj98/deepglobe-road-extraction-dataset)

```shell
grob "image={subset}/{name}_sat.jpg, mask={subset}/{name}_mask.png" .
```
