import dataclasses
import re
from typing import Any, Dict, Iterable, List, Union

from grob.core import parsers
from grob.core.errors import InvalidParserSpecificationError, InvalidTagSpecificationError
from grob.types import KeyPart, OnMissing, TagName, TagSpec

DEFAULT_TAG_NAME = TagName("default")


@dataclasses.dataclass
class Tag:
    name: TagName
    parser: parsers.Parser
    on_missing: OnMissing = OnMissing.fail
    allow_multiple: bool = False


@dataclasses.dataclass
class MultiPartTag(Tag):
    parser: parsers.MultiPartParserProtocol = None  # type: ignore[assignment]

    # This is an awful hack to allow default values on the parent class `Tag`. This won't be needed once we stop
    # supporting Python <3.10, since 3.10 introduces a `kw_only` argument
    def __post_init__(self) -> None:
        if self.parser is None:
            raise TypeError("__init__() missing 1 required positional argument: 'parser'")  # noqa: TRY003


@dataclasses.dataclass
class DistributableTag(MultiPartTag):
    distribute_over: List[KeyPart] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.distribute_over is None:
            raise TypeError("__init__() missing 1 required positional argument: 'distribute_over'")  # noqa: TRY003


@dataclasses.dataclass
class SinglePartTag(Tag):
    parser: parsers.SinglePartParserProtocol = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.parser is None:
            raise TypeError("__init__() missing 1 required positional argument: 'parser'")  # noqa: TRY003


def create_tags(raw_specs: Union[TagSpec, Dict[str, TagSpec]]) -> List[Tag]:
    specs = _normalize_spec(raw_specs)
    # Use a dict to preserve insertion order
    all_key_parts = list(
        {key_part: None for spec in specs.values() for key_part in getattr(spec["parser"], "key_parts", [])}
    )
    tags = [create_tag(name, **spec, all_key_parts=all_key_parts) for name, spec in specs.items()]
    return tags


def create_tag(
    name: str,
    parser: parsers.Parser,
    all_key_parts: List[KeyPart],
    allow_multiple: bool = False,
    on_missing: OnMissing = OnMissing.fail,
    distribute: bool = False,
    distribute_over: Iterable[str] = (),
) -> Tag:
    common_arguments = {
        "name": TagName(name),
        "parser": parser,
        "on_missing": on_missing,
        "allow_multiple": allow_multiple,
    }
    if isinstance(parser, parsers.CallableParser) or not hasattr(parser, "key_parts"):
        return SinglePartTag(**common_arguments)  # type: ignore[arg-type]
    elif (missing_key_parts := set(all_key_parts) - set(parser.key_parts)) or distribute:
        if not distribute_over:
            # Distribute over all keys that are not present in the pattern
            distribute_over = missing_key_parts
        return DistributableTag(
            **common_arguments,  # type: ignore[arg-type]
            distribute_over=[KeyPart(key_part) for key_part in distribute_over],
        )
    else:
        return MultiPartTag(**common_arguments)  # type: ignore[arg-type]


def _normalize_spec(spec: Union[TagSpec, Dict[str, TagSpec]]) -> Dict[TagName, Dict[str, Any]]:
    # Any is not actually Any, it's a TypedDict with a mandatory parser and optional keys
    if isinstance(spec, (str, re.Pattern)) or callable(spec):
        spec = {DEFAULT_TAG_NAME: spec}
    normalized_spec = {}
    for raw_tag_name, raw_tag_spec in spec.items():
        tag_spec = _convert_raw_spec_to_dict(raw_tag_spec)
        parser = _create_parser_from_spec(tag_spec)
        if isinstance(parser, parsers.PatternParser) and len(parser.key_parts) == 0 and len(spec) == 1:
            # This is a very special case: when a single tag is declared, and this tag uses pattern, and this pattern
            # has no named part, we convert it to a special callable parser that uses the full path as pattern. This
            # allows simple, single-tag specs with only wildcards and no placeholders
            parser = parsers.AnonymousParser(regex=parser.regex)
        if "on_missing" in tag_spec:
            tag_spec["on_missing"] = OnMissing(tag_spec["on_missing"])
        normalized_spec[TagName(raw_tag_name)] = {"parser": parser, **tag_spec}
    return normalized_spec


def _create_parser_from_spec(raw_tag_spec: Dict[str, Any]) -> parsers.Parser:
    parser_spec = raw_tag_spec.pop("spec")
    if isinstance(parser_spec, (str, re.Pattern)):
        return parsers.PatternParser(parser_spec)
    elif not callable(parser_spec):
        raise InvalidParserSpecificationError(parser_spec)
    elif (key_parts := raw_tag_spec.pop("key_parts", None)) is not None:
        return parsers.CallableMultiPartParser(parser_spec, key_parts=key_parts)
    else:
        return parsers.CallableParser(parser_spec)


def _convert_raw_spec_to_dict(raw_tag_spec: TagSpec) -> Dict[str, Any]:
    if isinstance(raw_tag_spec, (str, re.Pattern)) or callable(raw_tag_spec):
        return {"spec": raw_tag_spec}
    elif not isinstance(raw_tag_spec, dict) or "spec" not in raw_tag_spec:
        raise InvalidTagSpecificationError(raw_tag_spec)
    else:
        return raw_tag_spec
