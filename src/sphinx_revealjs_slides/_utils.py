"""sphinx_revealjs_slides._utils"""

from functools import cache
from pathlib import Path


@cache
def get_revealjs_source_dir() -> "Path":
    """Get path to Reveal.js source directory."""

    package_dir = Path(__file__).parent.resolve()
    return package_dir / "themes" / "lib" / "reveal.js"
