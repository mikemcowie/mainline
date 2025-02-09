from dataclasses import dataclass
from functools import cached_property

from dominate import document  # type: ignore
from dominate import tags as t

from hyperapi.components.base import Component
from hyperapi.components.head import DocumentHead
from hyperapi.components.script import RemoteScript
from hyperapi.components.style import RemoteStyleSheet
from hyperapi.rest_schema import APIResource


@dataclass
class Page(Component):
    """Base class that renders HTML pages"""

    resource: APIResource
    children: list[Component]
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

    @cached_property
    def document(self) -> document:
        return document(title=self.resource.title)

    def render_head(self):
        return DocumentHead(
            self.doc,
            self.resource,
            self.stylesheets,
            self.scripts,
        ).build()

    def build(self):
        with self.document.head:
            for m in self.resource.meta:
                t.meta(m.model_dump())
            for item in self.scripts + self.stylesheets:
                item.as_tag()
            t.link(rel="icon", type="image/x-icon", href="/static/logo.svg")

        return self.document
