import copy
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Iterable, Optional

from grob.cli import app

EXAMPLE_DIR = (Path(__file__).parent / "../../examples").resolve()


def get_example_dir(example_name: str) -> Path:
    return EXAMPLE_DIR / example_name / "root"


def run_example(
    spec: str,
    example_name: str,
    *,
    example_dir: Optional[Path] = None,
    options: Iterable[str] = (),
    parse_json: bool = True,
) -> str:
    if example_dir is None:
        example_dir = get_example_dir(example_name)
    argv = copy.deepcopy(sys.argv)
    try:
        sys.argv = [
            "app.py",
            spec,
            example_dir.as_posix(),
            "--relative",
            *options,
        ]
        output_stream = io.StringIO()
        with redirect_stdout(output_stream):
            app.main()
        output = output_stream.getvalue()
        if parse_json:
            return json.loads(output)
        return output
    finally:
        sys.argv = argv
