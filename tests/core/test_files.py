from pathlib import Path

import pytest

from grob.core.files import FileCollection, find_by_tag, group_by_key
from grob.core.frozendict import frozendict
from grob.core.key_formatters import FstringFormatter
from grob.core.parsers import CallableParser, PatternParser
from grob.core.tags import DistributableTag, MultiPartTag, SinglePartTag
from grob.types import GroupKey


def test_find_by_tag():
    (tag1,) = find_by_tag(
        ["1_2_3", "1_2_4", "1_2_5", "1_3", "1_2", "2_1"],
        [
            MultiPartTag(
                name="tag1",
                parser=PatternParser("{a}_{b}_{c}"),
            ),
        ],
    )
    assert tag1.files == {
        frozendict({"a": "1", "b": "2", "c": "3"}): "1_2_3",
        frozendict({"a": "1", "b": "2", "c": "4"}): "1_2_4",
        frozendict({"a": "1", "b": "2", "c": "5"}): "1_2_5",
    }


def test_find_by_tag_with_invalid_multiple():
    with pytest.raises(ValueError):
        find_by_tag(
            ["1/2_3", "1/2_4", "1/2_5", "1/3_4"],
            [
                MultiPartTag(
                    name="tag2",
                    parser=PatternParser("{a}/*_{b}"),
                )
            ],
        )


def test_find_by_tag_with_allowed_multiple():
    (tag1,) = find_by_tag(
        ["1/2_3", "1/2_4", "1/3_5", "1/3_4"],
        [MultiPartTag(name="tag2", parser=PatternParser("{a}/*_{b}"), allow_multiple=True)],
    )
    assert tag1.files == {
        frozendict({"a": "1", "b": "3"}): ["1/2_3"],
        frozendict({"a": "1", "b": "4"}): ["1/2_4", "1/3_4"],
        frozendict({"a": "1", "b": "5"}): ["1/3_5"],
    }


def test_group_by_key_with_single_collection():
    groups = group_by_key(
        [
            FileCollection(
                files={
                    frozendict({"a": "1", "b": "2"}): "1_2",
                    frozendict({"a": "1", "b": "3"}): "1_3",
                    frozendict({"a": "2", "b": "1"}): "2_1",
                },
                tag=MultiPartTag(name="tag", parser=PatternParser("{a}_{b}")),
            )
        ],
        key_formatter=FstringFormatter("{a}_{b}"),
    )
    assert groups == {
        "1_2": {"tag": "1_2"},
        "1_3": {"tag": "1_3"},
        "2_1": {"tag": "2_1"},
    }


def test_group_by_key_with_two_collections():
    groups = group_by_key(
        [
            FileCollection(
                files={
                    frozendict({"a": "1", "b": "2"}): Path("left/1_2"),
                    frozendict({"a": "1", "b": "3"}): Path("left/1_3"),
                    frozendict({"a": "2", "b": "1"}): Path("left/2_1"),
                },
                tag=MultiPartTag(name="left", parser=PatternParser("left/{a}_{b}")),
            ),
            FileCollection(
                files={
                    frozendict({"a": "1", "b": "3"}): Path("right/3_1"),
                    frozendict({"a": "2", "b": "1"}): Path("right/1_2"),
                    frozendict({"a": "1", "b": "2"}): Path("right/2_1"),
                },
                tag=MultiPartTag(name="right", parser=PatternParser("right/{b}_{1}")),
            ),
        ],
        key_formatter=FstringFormatter("{a}_{b}"),
    )
    assert groups == {
        "1_2": {"left": Path("left/1_2"), "right": Path("right/2_1")},
        "1_3": {"left": Path("left/1_3"), "right": Path("right/3_1")},
        "2_1": {"left": Path("left/2_1"), "right": Path("right/1_2")},
    }


def test_group_by_key_with_missing_tag():
    groups = group_by_key(
        [
            FileCollection(
                files={
                    frozendict({"a": "1", "b": "2"}): Path("left/1_2"),
                    frozendict({"a": "1", "b": "3"}): Path("left/1_3"),
                    frozendict({"a": "2", "b": "1"}): Path("left/2_1"),
                },
                tag=MultiPartTag(name="left", parser=PatternParser("left/{a}_{b}")),
            ),
            FileCollection(
                files={
                    frozendict({"a": "1", "b": "3"}): Path("right/3_1"),
                    frozendict({"a": "2", "b": "1"}): Path("right/1_2"),
                },
                tag=MultiPartTag(name="right", parser=PatternParser("right/{b}_{1}")),
            ),
        ],
        key_formatter=FstringFormatter("{a}_{b}"),
    )
    # group_by_key doesn't perform any validation, so this is valid
    assert groups == {
        "1_2": {"left": Path("left/1_2")},
        "1_3": {"left": Path("left/1_3"), "right": Path("right/3_1")},
        "2_1": {"left": Path("left/2_1"), "right": Path("right/1_2")},
    }


def test_group_by_key_with_tag_distribution():
    groups = group_by_key(
        [
            FileCollection(
                files={
                    frozendict({"album": "Rain Dogs", "index": "01"}): Path("Rain Dogs/track-01.mp3"),
                    frozendict({"album": "Rain Dogs", "index": "02"}): Path("Rain Dogs/track-02.mp3"),
                    frozendict({"album": "Rain Dogs", "index": "03"}): Path("Rain Dogs/track-03.mp3"),
                    frozendict({"album": "Blue Valentine", "index": "02"}): Path("Blue Valentine/track-02.mp3"),
                    frozendict({"album": "Blue Valentine", "index": "03"}): Path("Blue Valentine/track-03.mp3"),
                    frozendict({"album": "Blue Valentine", "index": "04"}): Path("Blue Valentine/track-04.mp3"),
                },
                tag=MultiPartTag(name="track", parser=PatternParser("{album}/track-{index}.mp3")),
            ),
            FileCollection(
                files={
                    frozendict({"album": "Rain Dogs"}): Path("Rain Dogs/cover.jpg"),
                    frozendict({"album": "Blue Valentine"}): Path("Blue Valentine/blue_valentine.png"),
                },
                tag=DistributableTag(
                    name="cover", parser=PatternParser("{album}/*.(png|jpg)"), distribute_over=["index"]
                ),
            ),
        ],
        key_formatter=FstringFormatter("{album}_track-{index}"),
    )
    assert groups == {
        "Rain Dogs_track-01": {"track": Path("Rain Dogs/track-01.mp3"), "cover": Path("Rain Dogs/cover.jpg")},
        "Rain Dogs_track-02": {"track": Path("Rain Dogs/track-02.mp3"), "cover": Path("Rain Dogs/cover.jpg")},
        "Rain Dogs_track-03": {"track": Path("Rain Dogs/track-03.mp3"), "cover": Path("Rain Dogs/cover.jpg")},
        "Blue Valentine_track-02": {
            "track": Path("Blue Valentine/track-02.mp3"),
            "cover": Path("Blue Valentine/blue_valentine.png"),
        },
        "Blue Valentine_track-03": {
            "track": Path("Blue Valentine/track-03.mp3"),
            "cover": Path("Blue Valentine/blue_valentine.png"),
        },
        "Blue Valentine_track-04": {
            "track": Path("Blue Valentine/track-04.mp3"),
            "cover": Path("Blue Valentine/blue_valentine.png"),
        },
    }


def test_group_by_key_with_tag_distribution_over_multiple_levels():
    groups = group_by_key(
        [
            FileCollection(
                tag=MultiPartTag(name="track", parser=PatternParser("{artist}/{album}/{{index}.mp3")),
                files={
                    frozendict({"artist": "Rose", "album": "Best-of", "index": "01"}): Path("Rose/Best-of/01.mp3"),
                    frozendict({"artist": "Rose", "album": "Best-of", "index": "02"}): Path("Rose/Best-of/02.mp3"),
                    frozendict({"artist": "Rose", "album": "Roses", "index": "01"}): Path("Rose/Roses/01.mp3"),
                    frozendict({"artist": "Rose", "album": "Roses", "index": "02"}): Path("Rose/Roses/02.mp3"),
                    frozendict({"artist": "Rose", "album": "Roses", "index": "03"}): Path("Rose/Roses/03.mp3"),
                    frozendict({"artist": "Joe", "album": "Best-of", "index": "01"}): Path("Joe/Best-of/01.mp3"),
                    frozendict({"artist": "Joe", "album": "Best-of", "index": "02"}): Path("Joe/Best-of/02.mp3"),
                },
            ),
            FileCollection(
                tag=DistributableTag(
                    name="cover", parser=PatternParser("{artist}/{album}/*.(png|jpg)"), distribute_over=["index"]
                ),
                files={
                    frozendict({"artist": "Rose", "album": "Best-of"}): Path("Rose/Best-of/cover.png"),
                    frozendict({"artist": "Rose", "album": "Roses"}): Path("Rose/Roses/roses.jpg"),
                    frozendict({"artist": "Joe", "album": "Best-of"}): Path("Joe/Best-of/cover.png"),
                },
            ),
            FileCollection(
                tag=DistributableTag(
                    name="artist", parser=PatternParser("{artist}.metadata.xml"), distribute_over=["album", "index"]
                ),
                files={
                    frozendict({"artist": "Rose"}): Path("Rose.metadata.xml"),
                    frozendict({"artist": "Joe"}): Path("Joe.metadata.xml"),
                },
            ),
        ],
        key_formatter=FstringFormatter("{artist} - {album} - {index}"),
    )
    assert groups == {
        "Rose - Best-of - 01": {
            "track": Path("Rose/Best-of/01.mp3"),
            "cover": Path("Rose/Best-of/cover.png"),
            "artist": Path("Rose.metadata.xml"),
        },
        "Rose - Best-of - 02": {
            "track": Path("Rose/Best-of/02.mp3"),
            "cover": Path("Rose/Best-of/cover.png"),
            "artist": Path("Rose.metadata.xml"),
        },
        "Rose - Roses - 01": {
            "track": Path("Rose/Roses/01.mp3"),
            "cover": Path("Rose/Roses/roses.jpg"),
            "artist": Path("Rose.metadata.xml"),
        },
        "Rose - Roses - 02": {
            "track": Path("Rose/Roses/02.mp3"),
            "cover": Path("Rose/Roses/roses.jpg"),
            "artist": Path("Rose.metadata.xml"),
        },
        "Rose - Roses - 03": {
            "track": Path("Rose/Roses/03.mp3"),
            "cover": Path("Rose/Roses/roses.jpg"),
            "artist": Path("Rose.metadata.xml"),
        },
        "Joe - Best-of - 01": {
            "track": Path("Joe/Best-of/01.mp3"),
            "cover": Path("Joe/Best-of/cover.png"),
            "artist": Path("Joe.metadata.xml"),
        },
        "Joe - Best-of - 02": {
            "track": Path("Joe/Best-of/02.mp3"),
            "cover": Path("Joe/Best-of/cover.png"),
            "artist": Path("Joe.metadata.xml"),
        },
    }


def test_group_by_key_with_single_part_tag():
    groups = group_by_key(
        [
            FileCollection(
                files={
                    frozendict({"a": "1", "b": "2"}): Path("left/1_2.zip"),
                    frozendict({"a": "1", "b": "3"}): Path("left/1_3.zip"),
                    frozendict({"a": "2", "b": "1"}): Path("left/2_1.zip"),
                },
                tag=MultiPartTag(name="zip", parser=PatternParser("left/{a}_{b}.zip")),
            ),
            FileCollection(
                files={
                    GroupKey("2_1"): Path("right/here/2_1.xml"),
                    GroupKey("1_2"): Path("right/here/1_2.xml"),
                    GroupKey("1_3"): Path("right/here/1_3.xml"),
                },
                tag=SinglePartTag(
                    name="xml", parser=CallableParser(lambda p: p.stem if p.relative_to("right") else None)
                ),
            ),
        ],
        key_formatter=FstringFormatter("{a}_{b}"),
    )
    assert groups == {
        "1_2": {"zip": Path("left/1_2.zip"), "xml": Path("right/here/1_2.xml")},
        "1_3": {"zip": Path("left/1_3.zip"), "xml": Path("right/here/1_3.xml")},
        "2_1": {"zip": Path("left/2_1.zip"), "xml": Path("right/here/2_1.xml")},
    }


def test_group_by_key_with_only_single_part_tags():
    groups = group_by_key(
        [
            FileCollection(
                files={
                    GroupKey("1_2"): Path("left/1_2.zip"),
                    GroupKey("1_3"): Path("left/1_3.zip"),
                    GroupKey("2_1"): Path("left/2_1.zip"),
                },
                tag=SinglePartTag(name="zip", parser=str),
            ),
            FileCollection(
                files={
                    GroupKey("2_1"): Path("right/here/2_1.xml"),
                    GroupKey("1_2"): Path("right/here/1_2.xml"),
                    GroupKey("1_3"): Path("right/here/1_3.xml"),
                },
                tag=SinglePartTag(name="xml", parser=str),
            ),
        ],
        key_formatter=FstringFormatter("{a}_{b}"),
    )
    assert groups == {
        "1_2": {"zip": Path("left/1_2.zip"), "xml": Path("right/here/1_2.xml")},
        "1_3": {"zip": Path("left/1_3.zip"), "xml": Path("right/here/1_3.xml")},
        "2_1": {"zip": Path("left/2_1.zip"), "xml": Path("right/here/2_1.xml")},
    }


# TODO: test failure paths
