"""sphinx_revealjs_slides.builder"""

from typing import TYPE_CHECKING

from sphinx.builders.html import StandaloneHTMLBuilder

if TYPE_CHECKING:
    from typing import Any, Optional


class RevealjsBuilder(StandaloneHTMLBuilder):
    name = "revealjs"
    search = False

    def get_theme_config(self) -> tuple[str, dict]:
        return self.config.revealjs_html_theme, self.config.revealjs_html_theme_options

    def handle_page(
        self,
        pagename: str,
        addctx: dict,
        templatename: str = "slides.html",
        outfilename: "Optional[str]" = None,
        event_arg: "Any" = None,
    ) -> None:
        super().handle_page(pagename, addctx, templatename, outfilename, event_arg)
