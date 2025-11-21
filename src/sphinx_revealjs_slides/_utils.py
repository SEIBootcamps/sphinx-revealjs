"""sphinx_revealjs_slides._utils"""

from functools import cache
from pathlib import Path


@cache
def get_revealjs_static_dir() -> "Path":
    """Get path to Reveal.js static directory (contains dist files)."""

    package_dir = Path(__file__).parent.resolve()
    return package_dir / "theme" / "revealjs" / "static"


@cache
def get_revealjs_plugin_dir() -> "Path":
    """Get path to Reveal.js plugin directory."""

    package_dir = Path(__file__).parent.resolve()
    return package_dir / "theme" / "revealjs" / "plugin"


@cache
def get_revealjs_source_dir() -> "Path":
    """Get path to Reveal.js source directory (deprecated, use get_revealjs_static_dir or get_revealjs_plugin_dir)."""

    # For backward compatibility, return static dir
    # This is used by revealjs_plugins for plugins, so we should use plugin_dir
    # But to maintain compatibility, we'll check where it's used
    return get_revealjs_plugin_dir()
