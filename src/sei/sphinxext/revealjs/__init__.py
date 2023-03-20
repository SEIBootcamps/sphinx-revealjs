from typing import TYPE_CHECKING, Any, List
import importlib.metadata
from pathlib import Path
from glob import glob
from sphinx.util.fileutil import copy_asset_file

from sei.sphinxext.revealjs import builder, overridenodes

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.config import Config

__name__ = "sei.sphinxext.revealjs"
__version__ = importlib.metadata.version(__name__)

THEMES_DIRECTORY = (Path(__file__).parent / "themes").resolve()
LIB_DIRECTORY = (Path(__file__).parent / ".." / ".." / ".." / ".." / "lib").resolve()
REVEALJS_DIST = LIB_DIRECTORY / "reveal.js" / "dist"


def builder_inited(app: "Sphinx") -> None:
    # app.config.html_theme_options["revealjs_theme"] = "solarized.css"
    pass


def exclude_unused_theme_files(theme_name: str) -> List[str]:
    """Exclude theme files that don't match the configured theme."""

    return [
        str(p)
        for p in glob("theme/*.css", root_dir=REVEALJS_DIST)
        if Path(p).name != theme_name
    ]


def add_theme(app: "Sphinx") -> None:
    if app.builder.name == "revealjs":
        app.add_css_file(app.config.revealjs_theme, priority=600)


def copy_revealjs_files(app: "Sphinx", exc) -> None:
    if app.builder.name == "revealjs" and not exc:
        staticdir = (Path(app.builder.outdir) / "_static").resolve()
        revealjs_files = [
            "reset.css",
            "reveal.css",
            "reveal.js",
            "reveal.js.map",
            Path("theme") / app.config.revealjs_theme,
        ]

        for f in revealjs_files:
            copy_asset_file(str(REVEALJS_DIST / f), str(staticdir))


def setup(app: "Sphinx") -> dict[str, Any]:
    builder.setup(app)
    overridenodes.setup(app)

    app.add_config_value("revealjs_theme", "white.css", "revealjs")

    app.connect("builder-inited", add_theme)
    app.connect("build-finished", copy_revealjs_files)

    app.add_html_theme("revealjs", str(THEMES_DIRECTORY / "revealjs"))
    app.add_css_file("reset.css", priority=500)
    app.add_css_file("reveal.css", priority=500)
    app.add_js_file("reveal.js", priority=500)
    app.add_js_file("reveal.js.map", priority=500)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
