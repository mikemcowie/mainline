from dataclasses import dataclass

from dominate import tags as t  # type: ignore

from mainline_server.rest_schema import APIResource
from mainline_server.ui.components.base import Component
from mainline_server.ui.script import RemoteScript
from mainline_server.ui.style import RemoteStyleSheet


@dataclass
class DocumentHead(Component):
    """The top-level <head> component of the page
    containing the title and other elements
    """

    doc: t.dom_tag
    resource: APIResource
    stylesheets: list[RemoteStyleSheet]
    scripts: list[RemoteScript]

    def build(self):
        with self.doc.head:
            for m in self.resource.meta:
                t.meta(m.model_dump())
            for item in self.scripts + self.stylesheets:
                item.as_tag()
