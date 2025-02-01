from dataclasses import dataclass, field

from dominate import tags as t  # type: ignore

from mainline_server.ui.components.base import Component


@dataclass
class Home(Component):
    """The homepage"""

    id: str
    cls: list[str] = field(default_factory=lambda: [])

    def build(self):
        with t.main(cls=" ".join(self.cls), id=self.id) as c:
            t.h1("Page Title")
            t.p("Hello world")
            return c
