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
class Row(Component):
    """https://getbootstrap.com/docs/5.3/layout/grid/

    The 2nd layer of layout, rows are wrappers for columns
    """

    id: str
    children: list["Column"]
    cls: list[str] = field(default_factory=lambda: ["row"])

    def build(self):
        return t.div(cls=" ".join(self.cls), id=self.id)


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
        return t.div(cls=" ".join([*self.cls, f"col-{self.width}"]), id=self.id)
