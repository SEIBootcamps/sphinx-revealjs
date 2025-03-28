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


def get_registered_plugins(app: "Sphinx") -> dict[str, str]:
    """Merge built-in plugins with user-defined plugins from app.conf.revealjs_plugins."""

    return {**REVEALJS_PLUGINS, **app.config.revealjs_plugins}


def get_path_to_plugin_entrypoint(plugins: dict[str, str], plugin_name: str) -> Path:
    """Get the path to the plugin entrypoint."""

    # Get the path to the plugin entrypoint
    if plugin_name not in plugins:
        raise ValueError(f"Plugin {plugin_name} not found in registered plugins.")

    plugin_dir, plugin_entrypoint = (
        plugins[plugin_name]["plugin_dir"],
        plugins[plugin_name]["plugin_entrypoint"],
    )

    return Path(plugin_dir) / plugin_entrypoint


def validate_revealjs_load_plugins(app: "Sphinx") -> None:
    """Warn user if a plugin is not found in REVEALJS_PLUGINS or user-defined plugins."""

    if app.builder.name != "revealjs":
        return

    for plugin_name in app.config.revealjs_load_plugins:
        if plugin_name not in get_registered_plugins(app):
            app.warn(
                f"[revealjs] Plugin {plugin_name} is not a registered plugin. Have you added it to the revealjs_plugins configuration value?"  # pylint: disable=line-too-long
            )


def add_revealjs_plugin_files(app: "Sphinx") -> None:
    """Register plugin files with builder."""

    if app.builder.name != "revealjs":
        return

    validate_revealjs_load_plugins(app)

    plugins = get_registered_plugins(app)
    for plugin_name in app.config.revealjs_load_plugins:
        if plugin_name in plugins:
            script_path = get_path_to_plugin_entrypoint(plugins, plugin_name)
            logger.debug(f"[revealjs] loading plugin {plugin_name} from {script_path}")
            app.add_js_file(str(script_path), priority=510)


def copy_plugin_files(app: "Sphinx", exc) -> None:
    """Copy plugin files to the _static/plugin directory."""

    if app.builder.name != "revealjs" or exc:
        return

    plugins = REVEALJS_PLUGINS  # don't use user-defined plugins here

    def _copy_revealjs_plugin(plugin_name: str) -> None:
        if plugin_name not in plugins:
            return

        plugin_dir = plugins[plugin_name]["plugin_dir"]
        plugin_src_dir = get_revealjs_source_dir() / plugin_dir
        plugin_dest_dir = Path(app.builder.outdir) / "_static" / plugin_dir
        ensuredir(plugin_dest_dir)
        try:
            for f in plugin_src_dir.glob("**/*"):
                copyfile(f, plugin_dest_dir / f.name)
                logger.debug(
                    f"[revealjs] copied static file: {(plugin_dest_dir / f.name).relative_to(Path(app.builder.outdir) / '_static')}"  # pylint: disable=line-too-long
                )
        except OSError:
            logger.warning(f"Cannot copy file {f} to {plugin_dest_dir / f.name}")

    with progress_message("[revealjs] copying plugin files"):
        for plugin_name in app.config.revealjs_load_plugins:
            _copy_revealjs_plugin(plugin_name)


def add_revealjs_plugins_to_html_context(
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
    plugin_exports = [
        plugins[plugin_name]["plugin_export"]
        for plugin_name in app.config.revealjs_load_plugins
        if plugin_name in plugins
    ]
    plugin_window_exports = [f"window.{name}" for name in plugin_exports]

    # This is a terrible, hacky way of doing things but it'll work for now...
    enabled_plugins_js = (
        f"window.SphinxRevealjsPlugins = {', '.join(plugin_window_exports)};"
    )

    # Update context
    context["revealjs_enabled_plugin_exports"] = enabled_plugins_js


def setup(app: "Sphinx") -> None:
    """Setup Reveal.js plugin loading feature."""

    # Allow users to register additional plugins by
    # adding an entry to the revealjs_plugins config value.
    # See REVEALJS_PLUGINS for format.
    app.add_config_value("revealjs_plugins", {}, "html")

    app.add_config_value("revealjs_load_plugins", DEFAULT_LOAD_PLUGINS, "html")

    app.connect("builder-inited", add_revealjs_plugin_files)
    app.connect("build-finished", copy_plugin_files)

    # On html-page-context, add the plugin entry points to the page.
    # html-page-context(app, pagename, templatename, context, doctree)
    app.connect("html-page-context", add_revealjs_plugins_to_html_context)
