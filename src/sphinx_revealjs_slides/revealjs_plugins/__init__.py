"""sphinx_revealjs_slides.revealjs_plugins

Reveal.js plugins.
"""

from typing import TYPE_CHECKING
from functools import cache
from pathlib import Path

from sphinx.util.fileutil import ensuredir, copyfile
from sphinx.util.display import progress_message
from sphinx.util import logging

from .constants import REVEALJS_PLUGINS, DEFAULT_LOAD_PLUGINS
from .._utils import get_revealjs_source_dir

if TYPE_CHECKING:
    from typing import Any
    from sphinx.application import Sphinx

logger = logging.getLogger(__name__)


@cache
def get_registered_plugins(app: "Sphinx") -> dict[str, str]:
    """Merge built-in plugins with user-defined plugins from app.conf.revealjs_plugins."""

    return {**REVEALJS_PLUGINS, **app.config.revealjs_plugins}


def validate_revealjs_load_plugins(app: "Sphinx") -> None:
    """Warn user if a plugin is not found in REVEALJS_PLUGINS or user-defined plugins."""

    if app.builder.name != "revealjs":
        return

    for plugin_name in app.config.revealjs_load_plugins:
        if plugin_name not in get_registered_plugins(app):
            app.warn(
                f"[revealjs] Plugin {plugin_name} is not a registered plugin. Have you added it to the revealjs_plugins configuration value?"  # pylint: disable=line-too-long
            )


def _copy_revealjs_plugin(plugin_name: str, app: "Sphinx") -> None:
    # Gather plugin files
    plugin_source_dir = get_revealjs_source_dir() / "plugin" / plugin_name
    plugin_files = list(plugin_source_dir.glob("**/*"))

    logger.debug(f"""\
[revealjs] discovered plugin {plugin_name}. Prepared to copy the following to static directory:
{"\n".join('* ' + str(f) for f in plugin_files)}
    """)

    # Copy to static/plugin directory
    static_dir = Path(app.builder.outdir) / "_static"
    dest_dir = static_dir / "plugin" / plugin_name
    ensuredir(dest_dir)
    try:
        for f in plugin_files:
            source, dest = f, dest_dir / f.name
            copyfile(source, dest)
            logger.debug(
                f"[revealjs] copied static file: {dest.relative_to(static_dir)}"
            )
    except OSError:
        logger.warning(f"Cannot copy file {source} to {dest}")


def copy_plugin_files(app: "Sphinx", exc) -> None:
    """Copy plugin files to the _static/plugin directory."""

    if app.builder.name != "revealjs" or exc:
        return

    with progress_message("[revealjs] copying plugin files"):
        for plugin_name in app.config.revealjs_load_plugins:
            _copy_revealjs_plugin(plugin_name, app)


def add_revealjs_initiation_script(
    app: "Sphinx",
    pagename: str,
    _,
    context: dict[str, "Any"],
    __,
) -> None:
    """Generate script to init Reveal.js and add to context."""

    if (
        app.builder.name != "revealjs" or pagename != app.config.root_doc
    ):  # only add init script to root_doc
        return

    plugins = get_registered_plugins(app)
    dynamic_imports = [
        f"import('./_static/plugin/{plugins[plugin_name]}')"
        for plugin_name in app.config.revealjs_load_plugins
        if plugin_name in plugins
    ]

    script = f"""\
<script type="module">
  import Reveal from './_static/reveal.esm.js';

  Promise.all([{",".join(dynamic_imports)}])
    .then((modules) => {"{"}
      Reveal.initialize({"{"}
        slideNumber: "c/t",
        showSlideNumber: "print",
        hashOneBasedIndex: true,
        hash: true,
        plugins: modules.map((m) => m.default),
      {"}"});
    {"}"});
</script>
    """

    # Update context
    context["revealjs_init_script"] = script


def setup(app: "Sphinx") -> None:
    """Setup Reveal.js plugin loading feature."""

    # Allow users to register additional plugins by
    # adding an entry to the revealjs_plugins config value.
    # See REVEALJS_PLUGINS for format.
    app.add_config_value("revealjs_plugins", {}, "html")

    app.add_config_value("revealjs_load_plugins", DEFAULT_LOAD_PLUGINS, "html")

    app.connect("build-finished", copy_plugin_files)

    # On html-page-context, add the plugin entry points to the page.
    # html-page-context(app, pagename, templatename, context, doctree)
    app.connect("html-page-context", add_revealjs_initiation_script)
