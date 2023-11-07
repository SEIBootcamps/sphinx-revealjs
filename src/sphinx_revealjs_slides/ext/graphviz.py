"""sphinx_revealjs_slides.ext.graphviz"""

from typing import TYPE_CHECKING
from sphinx.ext.graphviz import render_dot_html, setup as setup_graphviz

if TYPE_CHECKING:
    from sphinx.application import Sphinx


def setup(app: "Sphinx") -> None:
    setup_graphviz(app)
    app.add_node(revealjs=(render_dot_html, None))
