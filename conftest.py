from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import importlib_resources as resources
import pytest


@pytest.fixture()
def sample_proto_path() -> Iterator[Path]:
    with resources.as_file(resources.files(__name__).joinpath("sample.proto")) as path:
        yield path
