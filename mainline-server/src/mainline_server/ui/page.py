from functools import cache

from dominate import document  # type: ignore

from mainline_server.rest_schema import APIResource
from mainline_server.ui.components.head import DocumentHead
from mainline_server.ui.script import RemoteScript
from mainline_server.ui.style import RemoteStyleSheet


class Page:
    """Base class that renders HTML pages"""

    STYLESHEETS: tuple[RemoteStyleSheet, ...] = (
        RemoteStyleSheet(
            id="bootstrap-stylesheet",
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
            integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH",
        ),
    )
    SCRIPTS: tuple[RemoteScript, ...] = (
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

    def __init__(self, resource: APIResource):
        self.resource = resource
        self.doc = document(title=resource.title)
        self.build()

    def render_head(self):
        head = DocumentHead(
            self.doc,
            self.resource,
            self.STYLESHEETS,
            self.SCRIPTS,
        )
        with self.doc.head:
            head.build()
        with self.body:
            pass

    @property
    def body(self):
        return self.doc

    @cache
    def build(self):
        with self.doc.head:
            self.render_head()

    def __str__(self):
        return str(self.doc)
