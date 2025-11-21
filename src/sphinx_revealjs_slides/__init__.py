import importlib.metadata
from pathlib import Path
from typing import TYPE_CHECKING, Any

from sphinx.util import logging

from . import builder, directives, overridenodes, revealjs_plugins
from ._utils import get_revealjs_static_dir

if TYPE_CHECKING:
    from sphinx.application import Sphinx

__name__ = "sphinx_revealjs_slides"  # pylint: disable=redefined-builtin
__version__ = importlib.metadata.version(__name__)

logger = logging.getLogger(__name__)

revealjs_static_dir = get_revealjs_static_dir()


def init_builder(app: "Sphinx") -> None:
    """Called on builder-inited: setup builder and add static files."""

    if app.builder.name == "revealjs":
        add_revealjs_static_files(app)
        overridenodes.setup(app)


def add_revealjs_static_files(app: "Sphinx") -> None:
    """Register Reveal.js static files with builder."""

    app.add_css_file("reset.css", priority=500)
    app.add_css_file("reveal.css", priority=500)
    app.add_js_file("reveal.js", priority=500)
    # app.add_js_file("reveal.esm.js", priority=500)
    app.add_css_file(app.config.revealjs_theme, priority=600)


def setup(app: "Sphinx") -> dict[str, Any]:
    """Setup the extension."""

    app.add_builder(builder.RevealjsBuilder)
    app.connect("builder-inited", init_builder)

    app.add_config_value("revealjs_theme", "white.css", "html")
    app.add_config_value("revealjs_html_theme", "revealjs", "html")
    app.add_config_value("revealjs_html_theme_options", {}, "html")

    directives.incremental.setup(app)
    directives.speakernote.setup(app)
    directives.newslide.setup(app)
    directives.interslide.setup(app)

    revealjs_plugins.setup(app)

    app.add_html_theme(
        "revealjs",
        str(
            revealjs_static_dir.parent
            / "revealjs"  # sphinx_revealjs_slides/theme/revealjs
        ),
    )

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
