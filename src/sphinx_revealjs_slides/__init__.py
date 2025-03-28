import importlib.metadata
from pathlib import Path
from typing import TYPE_CHECKING, Any

from sphinx.util.osutil import copyfile, ensuredir
from sphinx.util import logging

from . import builder, directives, overridenodes, revealjs_plugins
from ._utils import get_revealjs_source_dir

if TYPE_CHECKING:
    from sphinx.application import Sphinx

__name__ = "sphinx_revealjs_slides"  # pylint: disable=redefined-builtin
__version__ = importlib.metadata.version(__name__)

logger = logging.getLogger(__name__)

revealjs_dir = get_revealjs_source_dir()


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


def copy_revealjs_files(app: "Sphinx", exc) -> None:
    """Called on builder-finished: copy Reveal.js files to the static directory."""

    if app.builder.name == "revealjs" and not exc:

        def _copy_to_staticdir(source: Path, dest: Path) -> None:
            # dest should be relative to staticdir
            staticdir = (Path(app.builder.outdir) / "_static").resolve()
            static_dest = staticdir / dest
            ensuredir(static_dest.parent)
            try:
                copyfile(str(source), str(static_dest))
            except OSError:
                logger.warning(f"Cannot copy file {source} to {dest}")

        # Collect required Revealjs files. Each tuple in revealjs_files is (source, dest)
        revealjs_dist_dir = revealjs_dir / "dist"
        revealjs_files = [
            (revealjs_dist_dir / "reset.css", "reset.css"),
            (revealjs_dist_dir / "reveal.css", "reveal.css"),
            (revealjs_dist_dir / "reveal.esm.js", "reveal.esm.js"),
            (revealjs_dist_dir / "reveal.js", "reveal.js"),
            (revealjs_dist_dir / "reveal.esm.js.map", "reveal.esm.js.map"),
            (
                revealjs_dist_dir / "theme" / app.config.revealjs_theme,
                app.config.revealjs_theme,
            ),
        ]

        for source, dest in revealjs_files:
            _copy_to_staticdir(source, dest)


def setup(app: "Sphinx") -> dict[str, Any]:
    """Setup the extension."""

    app.add_builder(builder.RevealjsBuilder)
    app.connect("builder-inited", init_builder)
    app.connect("build-finished", copy_revealjs_files)

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
            revealjs_dir.parent.parent
            / "revealjs"  # sphinx_revealjs_slides/themes/revealjs
        ),
    )

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
