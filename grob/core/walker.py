from pathlib import Path
from typing import Iterable


def walk(root_dir: Path) -> Iterable[Path]:
    """Iterate over all files in `root_dir`."""
    # TODO: parse tag patterns to restrict which subdirectories are searched. This is a brute-force implementation
    #  in order to have a MVP soon enough, but there's got to be a better way. Typically we want to analyze parsers
    #   in order to identify:
    #   - fixed suffix path (to directly search in the most precise directories as possible)
    #   - double wildcards (if there are none, we can stop once the maximum nesting level is reached
    for path in root_dir.rglob("*"):
        if path.is_dir():
            continue
        yield path
