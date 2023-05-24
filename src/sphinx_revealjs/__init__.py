from typing import TYPE_CHECKING, Any
import importlib.metadata
from pathlib import Path
from sphinx.util.fileutil import copy_asset_file

from . import builder, overridenodes, directives

if TYPE_CHECKING:
    from sphinx.application import Sphinx

__name__ = "sphinx_revealjs"
__version__ = importlib.metadata.version(__name__)

THEMES_DIRECTORY = (Path(__file__).parent / "themes").resolve()
LIB_DIRECTORY = (Path(__file__).parent / ".." / "lib").resolve()
REVEALJS_DIST = LIB_DIRECTORY / "reveal.js" / "dist"


def init_builder(app: "Sphinx") -> None:
    if app.builder.name == "revealjs":
        add_revealjs_static_files(app)
        override_nodes(app)


def add_revealjs_static_files(app: "Sphinx") -> None:
    app.add_css_file("reset.css", priority=500)
    app.add_css_file("reveal.css", priority=500)
    app.add_js_file("reveal.js", priority=500)
    app.add_js_file("reveal.js.map", priority=500)
    app.add_css_file(app.config.revealjs_theme, priority=600)


def override_nodes(app: "Sphinx") -> None:
    overridenodes.setup(app)


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
    app.add_config_value("revealjs_theme", "white.css", "html")
    app.add_html_theme("revealjs", str(THEMES_DIRECTORY / "revealjs"))
    app.add_builder(builder.RevealjsBuilder)
    app.connect("builder-inited", init_builder)
    app.connect("build-finished", copy_revealjs_files)

    directives.incremental.setup(app)
    directives.speakernote.setup(app)
    directives.newslide.setup(app)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }