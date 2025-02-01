from dataclasses import dataclass, field

from dominate import tags as t  # type: ignore

from mainline_server.ui.components.base import Component


@dataclass
class Container(Component):
    """https://getbootstrap.com/docs/5.3/layout/containers/

    The highest organizational layer of the layout
    """

    id: str
    rows: list["Row"]
    cls: list[str] = field(default_factory=lambda: ["container-fluid"])

    def build(self):
        with t.div(cls=" ".join(self.cls), id=self.id) as c:
            for row in self.rows:
                row.build()
            return c


@dataclass
class Row(Component):
    """https://getbootstrap.com/docs/5.3/layout/grid/

    The 2nd layer of layout, rows are wrappers for columns
    """

    id: str
    columns: list["Column"]
    cls: list[str] = field(default_factory=lambda: ["row"])

    def build(self):
        with t.div(cls=" ".join(self.cls), id=self.id) as r:
            for c in self.columns:
                c.build()
            return r


@dataclass
class Column(Component):
    """https://getbootstrap.com/docs/5.3/layout/grid/

    The 2nd layer of layout, rows are wrappers for columns
    """

    id: str
    width: int  # all columns in a row add to 12
    children: list[Component]
    cls: list[str] = field(default_factory=lambda: ["col"])

    def build(self):
        c = t.div(cls=" ".join([*self.cls, f"col-{self.width}"]), id=self.id)
        with c:
            for child in self.children:
                child.build()
