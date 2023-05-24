"""sphinx_revealjs.builder"""

from sphinx.builders.html import StandaloneHTMLBuilder


class RevealjsBuilder(StandaloneHTMLBuilder):
    name = "revealjs"
    search = False
