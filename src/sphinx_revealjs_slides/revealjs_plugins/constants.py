"""sphinx_revealjs_slides.revealjs_plugins.constants"""

# Name of plugin and path to the plugin entrypoint, relative
# to the static/plugin directory.
REVEALJS_PLUGINS = {
    "highlight": "highlight/highlight.esm.js",  # might exclude this one
    "markdown": "markdown/markdown.esm.js",
    "math": "math/math.esm.js",  # might exclude this one
    "notes": "notes/notes.esm.js",
    "search": "search/search.esm.js",
    "zoom": "zoom/zoom.esm.js",
}

DEFAULT_LOAD_PLUGINS = ["notes"]
