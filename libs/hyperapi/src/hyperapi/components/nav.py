from dataclasses import dataclass, field

from dominate import tags as t  # type: ignore

from hyperapi.components.base import Component


@dataclass
class Container(Component):
    """https://getbootstrap.com/docs/5.3/layout/containers/

    The highest organizational layer of the layout
    """

    id: str
    children: list["Row"]
    cls: list[str] = field(default_factory=lambda: ["container-fluid"])

    def build(self):
        return t.div(cls=" ".join(self.cls), id=self.id)


@dataclass
class Nav(Component):
    id: str
    children: list["Column"]

    def build(self):
        with t.div(id=self.id, cls="d-flex justify-content-center") as div:
            with t.nav(cls="navbar navbar-light bg-light"):
                with t.a(cls="navbar-brand", href="/"):
                    t.img(
                        src="/static/logo.svg",
                        width="200",
                        height="200",
                        cls="d-inline-block align-top",
                        alt="",
                    )
        return div
