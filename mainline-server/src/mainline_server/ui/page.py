from functools import cache

from dominate import document  # type: ignore

from mainline_server.rest_schema import APIResource
from mainline_server.ui.components.head import DocumentHead
from mainline_server.ui.components.home import Home
from mainline_server.ui.components.layout import Column, Container, Row
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
        return DocumentHead(
            self.doc,
            self.resource,
            self.STYLESHEETS,
            self.SCRIPTS,
        ).build()

    @property
    def body(self):
        return self.doc

    @cache
    def build(self):
        with self.doc.head:
            self.render_head()
        with self.body:
            self.body.container = Container(
                id="root-container",
                rows=[
                    Row(
                        id="head-row",
                        columns=[Column(id="head-col-1", width=12, children=[])],
                    ),
                    Row(
                        id="body-row",
                        columns=[
                            Column(id="body-col-1", width=4, children=[]),
                            Column(
                                id="body-col-2", width=4, children=[self.main_resource]
                            ),
                            Column(id="body-col-3", width=4, children=[]),
                        ],
                    ),
                    Row(
                        id="footer-row",
                        columns=[Column(id="footer-col-1", width=12, children=[])],
                    ),
                ],
            ).build()

    @property
    def main_resource(self):
        """Represents the main resource of the page"""
        return Home(id="home")

    def __str__(self):
        return str(self.doc)
