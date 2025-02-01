from dataclasses import asdict, dataclass, field
from typing import Literal

from dominate import tags as t  # type: ignore


@dataclass
class RemoteStyleSheet:
    """Represents a stylesheet at a remote CDN url
    that will be inclueded in the rendered page
    """

    TAG_TYPE = t.link
    id: str
    href: str
    integrity: str
    rel: Literal["stylesheet"] = field(default="stylesheet", init=False)
    crossorigin: Literal["anonymous"] = field(default="anonymous", init=False)

    def as_tag(self):
        return self.TAG_TYPE(**asdict(self))
