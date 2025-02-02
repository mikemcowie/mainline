"""base protocols for components

May be inherited from or used as a duck-type
"""

from abc import abstractmethod
from typing import Protocol

from dominate import dom_tag  # type: ignore


class Component(Protocol):
    """A reusable unit of a UI

    components are compiled together to build
    a page
    """

    children: list["Component"]

    @abstractmethod
    def build(self) -> dom_tag:
        """returns the dominate dom_tag object
        that can be rendered into a page

        per dominate behaviour, if called
        within a context manager of a dom_tag
        object, it will be appended to that
        data structure
        """
