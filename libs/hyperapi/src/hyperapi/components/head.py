from dataclasses import dataclass, field

from dominate import tags as t  # type: ignore

from hyperapi.rest_schema import APIResource
from hyperapi.components.base import Component
from hyperapi.components.script import RemoteScript
from hyperapi.components.style import RemoteStyleSheet


@dataclass
class DocumentHead(Component):
    """The top-level <head> component of the page
    containing the title and other elements
    """

    resource: APIResource
    stylesheets: tuple[RemoteStyleSheet, ...] = (
        RemoteStyleSheet(
            id="bootstrap-stylesheet",
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
            integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH",
        ),
    )
    scripts: tuple[RemoteScript, ...] = (
        RemoteScript(
            id="bootstrap-js",
            src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js",
            integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz",
        ),
        RemoteScript(
            id="htmx-js",
            src="https://unpkg.com/htmx.org@2.0.4",
            integrity="sha384-HGfztofotfshcF7+8n44JQL2oJmowVChPTg48S+jvZoztPfvwD79OC/LTtG6dMp+",
        ),
    )
    children: list[Component] = field(default_factory=list, init=False)

    def build(self):
        for m in self.resource.meta:
            t.meta(m.model_dump())
        for item in self.scripts + self.stylesheets:
            item.as_tag()
