"""sphinx_revealjs_slides.revealjs_plugins.constants"""

# <name of plugin>: (name of js export, path to js file)
REVEALJS_PLUGINS = {
    "highlight": {
        "plugin_export": "RevealHighlight",
        "plugin_dir": "plugin/highlight",
        "plugin_entrypoint": "highlight.js",
    },  # might exclude this one
    "markdown": {
        "plugin_export": "RevealMarkdown",
        "plugin_dir": "plugin/markdown",
        "plugin_entrypoing": "markdown.js",
    },
    "math": {
        "plugin_export": "RevealMath",
        "plugin_dir": "plugin/math",
        "plugin_entrypoint": "math.js",
    },  # might exclude this one
    "notes": {
        "plugin_export": "RevealNotes",
        "plugin_dir": "plugin/notes",
        "plugin_entrypoint": "notes.js",
    },
    "search": {
        "plugin_export": "RevealSearch",
        "plugin_dir": "plugin/search",
        "plugin_entrypoint": "search.js",
    },
    "zoom": {
        "plugin_export": "RevealZoom",
        "plugin_dir": "plugin/zoom",
        "plugin_entrypoint": "zoom.js",
    },
}

DEFAULT_LOAD_PLUGINS = ["notes"]
