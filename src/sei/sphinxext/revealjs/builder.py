from typing import TYPE_CHECKING

from sphinx.builders.html import StandaloneHTMLBuilder

if TYPE_CHECKING:
    from sphinx.application import Sphinx


class RevealjsBuilder(StandaloneHTMLBuilder):
    name = "revealjs"
    search = False


def setup(app: "Sphinx") -> None:
    app.add_builder(RevealjsBuilder)
