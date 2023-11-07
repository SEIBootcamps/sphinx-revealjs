"""sphinx_revealjs_slides.directives.interslide"""

from typing import TYPE_CHECKING
from docutils import nodes
from ._base_slide import BaseSlide

if TYPE_CHECKING:
    from typing import List
    from sphinx.application import Sphinx


class interslide(nodes.General, nodes.Element):
    pass


class Interslide(BaseSlide):
    """Interslide directive."""

    has_content = True

    def run(self) -> "List[nodes.Element]":
        node = interslide("\n".join(self.content))
        self.add_name(node)
        self.attach_options(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def visit_interslide(self, node: interslide) -> None:
    self.body.append("</section>")
    self.body.append(
        self.starttag(
            node,
            "section",
            **{att: val for att, val in node.attributes.items() if val is not None},
        )
    )


def depart_interslide(self, node: interslide) -> None:
    self.body.append("</section>")
    self.body.append("<section>")

    if node.parent:
        title = node.parent.next_node(nodes.title).astext().strip()
        self.body.append(f"<h{self.section_level}>{title}</h{self.section_level}>")


def ignore_interslide(self, node: interslide) -> None:
    raise nodes.SkipNode


def setup(app: "Sphinx") -> None:
    app.add_node(
        interslide,
        revealjs=(visit_interslide, depart_interslide),
        html=(ignore_interslide, None),
    )
    app.add_directive("interslide", Interslide)
