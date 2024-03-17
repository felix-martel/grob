from typing import Any, Callable, Generic, NoReturn, TypeVar

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


def _not_available(name: str) -> Callable[..., NoReturn]:
    def method(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        raise NotImplementedError(name)

    return method


class frozendict(dict, Generic[_KT, _VT]):
    """A naive, minimal implementation of hashable unmutable mapping."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._ensure_hashable()

    def _ensure_hashable(self) -> None:
        for key, value in self.items():
            if not hasattr(value, "__hash__"):
                raise TypeError(  # noqa: TRY003
                    f"frozendict cannot contain non-hashable value '{value}' of type {type(value)} for key '{key}'"
                )

    def __hash__(self) -> int:  # type: ignore[override]
        return hash(tuple(sorted(self.items())))

    __delitem__ = _not_available("__delitem__")
    __setitem__ = _not_available("__setitem__")
