from unittest import TestCase

from bs4 import BeautifulSoup
from dominate import document

from mainline_server.ui.components.head import (
    DocumentHead,
)
from tests import factories as f


class DocumentHeadComponentTest(TestCase):
    def setUp(self):
        self.doc = document()
        self.resource = f.APIResourceFactory.build(
            meta=[
                f.MetaNameContentFactory.build(),
                f.MetaCharsetFactory.build(),
                f.MetaHTMLEquivContentFactory.build(),
            ]
        )
        self.stylesheets = [f.RemoteStyleSheetFactory.build() for _ in range(4)]
        self.scripts = [f.RemoteScriptFactory.build() for _ in range(5)]
        with self.doc:
            DocumentHead(
                doc=self.doc,
                resource=self.resource,
                stylesheets=self.stylesheets,
                scripts=self.scripts,
            ).build()
        self.doc_soup = BeautifulSoup(str(self.doc), "html.parser")
        self.head_soup = self.doc_soup.find_all("head")
        self.meta_soup = self.doc_soup.find("head").find_all("meta")
        self.link_soup = self.doc_soup.find("head").find_all("link", rel="stylesheet")

    def test_one_head_tag(self):
        assert len(self.doc_soup.find_all("head")) == 1

    def test_stylesheets_all_rendered_in_head(self):
        links = [
            link
            for link in self.doc_soup.find_all("link")
            if link.get("rel")[0] == "stylesheet"
        ]
        assert len(links) == len(self.stylesheets)

    def test_scripts_all_rendered_in_head(self):
        scripts = [script for script in self.doc_soup.find_all("script")]
        assert len(scripts) == len(self.scripts)
